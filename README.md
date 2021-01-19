# LaTeX Utilities
This project provides Python tools for working with LaTeX document scripts.

## Functions
### tabular
Quickly convert Excel spreadsheet tables into LaTeX script for insertion into a working document. Creating large tables and tedious updating of values after changes in the data are easy to handle using this function call. Simply copy the text from the python console into your LaTeX editor, or use the output text file (optional).

## Tips
### Centering Table Columns on Decimal Point
This trick helps readers when they are pouring over tables of values. Orders of magnitude are easy to pick out if data is centered on the decimal point.

#### Setup
First make sure you add this package to your preamble: `\usepackage{siunitx}`. Also, a new command is helpful to define:
```
\newcommand{\dechead}[1]{\multicolumn{1}{c}{\text{#1}}}  % center align and protect header cell contents when using "S" mode
```
As the comment indicates, this will be used to protect text in a column that shouldn't be aligned by the decimal centering and instead just center the text as typical.

#### Use
When a particular column should be centered on the decimal point, specify it's type/formatting as "S" like `\begin{tabular}{cSS}`. When using the "S", any header text or other non-numeric items should be protected using the `\dechead{}` wrapper defined above as in the following example of a simple table using this method. The second and third columns are centered on decimal, whereas the first column is simply aligned on center.
```
\begin{table}
\begin{tabular}{cSS}  % "S" = align values by decimal place
Run & \dechead{Temperature (C)} & \dechead{Time (s)} \\
1 & 50.0 & 25.0 \\
2 & 2.50 & 320 \\
\end{tabular}
\end{table}
```
