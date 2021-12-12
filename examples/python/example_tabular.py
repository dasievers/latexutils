#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examples of using tabular
"""

from latexutils import tabular

# =============================================================================
#
# =============================================================================

path = 'tables.xlsx'

# standard example
tabular(path,
        sheet=0,
        formats=0,
        tablestart=1,
        save='tabular_output.txt')

# multi-line header example with S wrappers
tabular(path,
        sheet=1,
        formats=0,
        tablestart=1,
        headerend=3,
        save='tabular_output_multiheader.txt')
