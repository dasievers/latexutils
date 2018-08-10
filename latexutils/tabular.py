# -*- coding: utf-8 -*-

import pandas as pd

def tabular(path, sheet=0, columns=None, formats=None, startrow=0, endskip=0, export=False):
    """
    Construct a string of text for LaTeX tables out of an excel file to copy/paste
    into your LaTeX document.
    The resulting string is printed and can be optionally saved to a text file.
    
    The header output here usually requires some clean up within LaTeX, but the
    initial creation of the table and subsequent updates to values is where
    this tool really shines.
    
    Parameters
    ----------
    path : str
        Path to excel file.
    
    Optional Parameters
    -------------------
    sheet : int or str
        Sheet index or name in spreadsheet.
    columns : array
        Column indices to import. If None, import all columns.
    formats : multiple options:
        None: Automatically format output (default for floats is sci).
        int: Row number to use for importing definition of each column format.
        list: Definition of each column format e.g. ['%s', '%.2e'].
    startrow : int
        Row to start table at.
    endskip : int
        Lines to omit at end of sheet.
    export : bool
        Export text to file.
    """
    if formats==None:  # auto-select output formatting based on dtypes
        probe = pd.read_excel(path, sheet_name=sheet, usecols=columns, skiprows=startrow, skipfooter=endskip)
        formats = []
        for dt in probe.dtypes:
            if 'int' in str(dt):
                formats.append('%i')
            elif 'float' in str(dt):
                formats.append('%.3e')
            else:
                formats.append('%s')
    elif type(formats) is int:  # formats are specified within the excel sheet (above each column)
        probe = pd.read_excel(path, sheet_name=sheet, header=None, usecols=columns, skiprows=formats, nrows=1)
        formats = [x for x in probe.as_matrix().flatten()]
    
    dataset = pd.read_excel(path, sheet_name=sheet, skiprows=startrow, skipfooter=endskip, usecols=columns)
    linelist = []
    
    # build the header
    line = ''
    for i, name in enumerate(dataset.keys()):
        line += name
        if i < len(dataset.keys())-1:  # not last item
            line += ' & '
    line += ' \\\\'
    linelist.append(line)
    
    # build the data table
    for i in range(dataset.shape[0]):
        line = ''
        for j in range(dataset.shape[1]):
            try:
                text = formats[j] % dataset.iloc[i,j]
                if 'e' in formats[j]:  # insert sci notation command
                    text = '\\num{' + text + '}'
            except (TypeError, NameError, UnicodeEncodeError):  # if non-numeric values present, or no coltype defined
                text = dataset.iloc[i,j]
            if u'\xb1' in text:  # replace with plusminus inside math mode
                text = '$' + text.replace(u'\xb1', '\pm') + '$'  
#                text = '$\mathsf{' + text.replace(u'\xb1', '\pm') + '}$'  # sans font
            line += text
            if j < dataset.shape[1]-1:  # not last item
                line += ' & '
        line = line.replace('nan', '')
        line += ' \\\\'
        linelist.append(line)
            
    # combine lines
    table = ''
    for item in linelist:
        table += '%s\n' % item
    table = table[:-1]  # strip off last break

    # reduce to ascii format for latex scripts (ignore non-ascii characters)
    table = table.encode('ascii', 'ignore').decode('ascii')
    
    print(40*'-')
    print(table)
    print(40*'-')
    
    print(table.rsplit('\n', 1))
    
    if export:  # export strings
        with open('tabular_output.txt', 'w') as f:
            f.write(table)



# =============================================================================
# execution
# =============================================================================
if __name__ == '__main__':

    path = 'tables.xlsx'
    formats = 0
    startrow = 1
    tabular(path, formats=formats, startrow=startrow, export=True)




