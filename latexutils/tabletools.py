# -*- coding: utf-8 -*-

import pandas as pd

# =============================================================================
#
# =============================================================================
def tabular(path, sheet=0, columns=None, formats=None, tablestart=0, headerend=None,
            dcwrapper='',
            linesepadd = None,
            save=False,
            **kwargs):
    """
    Construct a string of text for LaTeX tables out of an excel file to copy/paste
    into your LaTeX document.
    The resulting string is printed and can be optionally saved to a text file.

    Recommended packages include 'booktabs' and 'siunitx' with column
    type 'S' to center on decimal point where desired. Only one is needed,
    but both work together.

    The header output here usually requires some cleanup within LaTeX, but the
    initial creation of the table and subsequent updates to values are readily
    done with this tool.

    Parameters
    ----------
    path : str
        Path to excel file.

    Optional Parameters
    -------------------
    sheet : int or str
        Sheet index or name in spreadsheet. Default first sheet.

    columns : list
        Column indices to import. Default import all columns.

    formats : multiple options:
        None: Automatically format output.
        int: Row index to use for importing format of each column.
        list: Definition of each column format e.g. ['%s', '%.2e'].
        If decimal centering is desired, add an 'S' to the format string
        (e.g. '%.2fS')*.

    tablestart : int
        Row index to start table at. Make sure to move this if a formatting
        row is called.

    headerend : int
        If multiple header lines are used, such as having units on a second
        line, then the end line of the header section must be defined. The default
        is to assume single-line header.

    dcwrapper : str
        Command name used to wrap header contents if decimal point centering format
        is used ("S" defined columns)*. If left empty string (''), braces will be
        added to protect header contents.

    save : str
        Export text to file as specified.

    [extra kwargs]
        These will be passed to the pandas read_excel when importing the table.
        May be necessary if needing to use skipfooter, etc.

    *See more info on this in this package's decimal centering tips in the README.

    Returns
    -------
    str : The generated table string output.
    """

    dataset = pd.read_excel(path, sheet_name=sheet, skiprows=tablestart,
                            usecols=columns, **kwargs)

    # deal with extra header lines
    if headerend is not None:
        extraheader = dataset[:headerend-tablestart]
        # chop out extra header lines and then re-infer dtypes of data
        dataset = dataset[headerend-tablestart:].convert_dtypes()
    else:
        extraheader = None

    # set the format types if not provided by a list
    if formats is None:  # auto-select output formatting based on dtypes
        formats = []
        for dt in dataset.dtypes:
            if 'int' in str(dt):
                formats.append('%i')
            elif 'float' in str(dt):
                formats.append('%.2f')
            else:
                formats.append('%s')
    elif type(formats) is int:
        # formats are specified within the excel sheet (above each column)
        # defined by formats position
        formats = pd.read_excel(path, sheet_name=sheet,
                                header=None, usecols=columns,
                                skiprows=formats, nrows=1).values.flatten()

    # determine if any column headers need wrappers for decimal centering
    dcenter = []
    for i, f in enumerate(formats):
        if 'S' in f:
            dcenter.append(True)
            formats[i] = f.replace('S', '')  # drop the extra 'S'
        else:
            dcenter.append(False)

    linelist = []
    # build the header
    def _headline(obj):
        line = ''
        for i, name in enumerate(obj):
            if pd.isna(name) is False:
                # skip if nan
                if dcenter[i]:
                    line += dcwrapper + '{' + name + '}'
                else:
                    line += name

            if i < len(obj)-1:  # not last item
                line += ' & '
        line += r' \\'
        return line

    linelist.append(_headline(dataset.keys()))
    if extraheader is not None:
        for i in range(len(extraheader)):
            linelist.append(_headline(extraheader.iloc[i]))

    # build the data table
    for i in range(dataset.shape[0]):
        line = ''
        for j in range(dataset.shape[1]):
            try:
                text = formats[j] % dataset.iloc[i,j]
                if 'e' in formats[j]:  # insert sci notation command
                    text = '\\num{' + text + '}'
            except (TypeError, NameError, UnicodeEncodeError):
                # if non-numeric values present, or no coltype defined
                text = dataset.iloc[i,j]
            if u'\xb1' in text:  # replace with plusminus inside math mode
                text = '$' + text.replace(u'\xb1', '\pm') + '$'
#                text = '$\mathsf{' + text.replace(u'\xb1', '\pm') + '}$'  # sans font
            line += text
            if j < dataset.shape[1]-1:  # not last item
                line += ' & '
        line = line.replace('nan', '')
        line += r' \\'
        if linesepadd:
            line += f' {linesepadd}'
        linelist.append(line)

    # combine lines
    table = ''
    for item in linelist:
        table += '%s\n' % item
    table = table[:-1]  # strip off last break

    # reduce to ascii format for latex scripts (ignore non-ascii characters)
    table = table.encode('ascii', 'ignore').decode('ascii')

    print(79*'-')
    print(table)
    print(79*'-')

#    print(table.rsplit('\n', 1))

    if save:  # export strings to file
        with open(save, 'w') as f:
            f.write(table)

    return table



# =============================================================================
# testing
# =============================================================================
if __name__ == '__main__':

    path = '../examples/python/tables.xlsx'

    # standard example
    t = tabular(path,
                sheet=0,
                formats=0,
                tablestart=1)

    # multi-line header example with S wrappers
    t = tabular(path,
                sheet=1,
                formats=0,
                tablestart=1,
                headerend=3)




