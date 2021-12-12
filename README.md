# LaTeX Utilities

This project provides Python tools for working with LaTeX document scripts.

## Contents

### tabular

Quickly convert Excel spreadsheet tables into LaTeX script for insertion into a working document. Creating large tables and tedious updating of values after changes in the data are easy to handle using this function call. Simply copy the text from the python console into your LaTeX editor, or use the output text file (optional).

## Installation

Use the following to install.

    pip install git+https://github.com/dasievers/latexutils

## Examples

See the provided python script and LaTeX examples to quickly get started.

## Tips

### Centering Table Columns on Decimal Point

This trick helps readers when they are pouring over tables of values. Orders of magnitude are easy to visually distinguish if data is centered on the decimal point.

#### Setup

Make sure you add this package to your preamble: `\usepackage{siunitx}`.

#### Use

When a particular column should be centered on the decimal point, specify it's type/formatting as "S" like `\begin{tabular}{cSS}`. When using the "S", any header text or other items you don't want treated as a float to center on decimal, place the item in braces. In the example, the second and third columns are centered on decimal, whereas the first column is simply aligned on center.
```
\begin{table}
\begin{tabular}{cSS}  % "S" = align values by decimal place
Run & {Temperature (C)} & {Time (s)} \\
1 & 50.0 & 25.0 \\
2 & 2.50 & 320 \\
\end{tabular}
\end{table}
```
