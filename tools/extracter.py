#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import sets
import sys
import xlrd

from cell_parser import *

__author__ = "Andrey Konovalov"
__copyright__ = "Copyright (C) 2014 Andrey Konovalov"
__license__ = "MIT"
__version__ = "0.1"

files = [
  '2014_spring/1.xls',
  '2014_spring/2.xls',
  '2014_spring/3.xls',
  '2014_spring/4.xls',
  '2014_spring/5.xls'
] 

def GetValues(file):
  workbook = xlrd.open_workbook(file, formatting_info=True)
  worksheet = workbook.sheet_by_index(0)

  values = sets.Set()
  for (rb, re, cb, ce) in worksheet.merged_cells:
    for row in xrange(worksheet.nrows):
      for col in xrange(worksheet.ncols):
        value = worksheet.cell_value(row, col)
        if len(value) >= 4:
          #value = value.encode('utf-8')
          values.add(value)
  return values

def StripValues(values):
  stripped_values = sets.Set()

all_values = sets.Set()

for file in files:
  all_values.update(GetValues(file))

for value in sorted(all_values):
  print value.encode('utf-8')
