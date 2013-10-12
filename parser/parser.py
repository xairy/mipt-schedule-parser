#!/usr/bin/python
#coding: utf-8

import sys
import xlrd

#TODO: check time schedule.

MONDAY = u'Понедельник'
TUESDAY = u'Вторник'
WEDNESDAY = u'Среда'
THURSDAY = u'Четверг'
FRIDAY = u'Пятница'
SATURDAY = u'Суббота'

def weekday_range(worksheet, weekday):
  ranges = []
  for (rb, re, cb, ce) in worksheet.merged_cells:
    if worksheet.cell_value(rb, cb) == weekday:
      ranges.append((rb, re))
  assert len(ranges) != 0
  for i in xrange(len(ranges) - 1):
    assert ranges[i] == ranges[i + 1]
  return ranges[0]

if __name__ == '__main__':
  print 'MONDAY: ' + str(weekday_range(worksheet, MONDAY))
