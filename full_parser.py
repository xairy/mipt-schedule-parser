#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import sets
import sys
import xlrd

import schedule_parser
import cell_parser

__author__ = "Andrey Konovalov"
__copyright__ = "Copyright (C) 2014 Andrey Konovalov"
__license__ = "MIT"
__version__ = "0.1"

def PrintFullSchedule(file):
  schedule = schedule_parser.Schedule()
  schedule.Parse(file)
  for department_index in xrange(schedule.GetDepartmentCount()):
    schedule_tables = []
    for weekday_index in xrange(6):
      schedule_tables.append(schedule.GetScheduleTable(department_index, weekday_index))
    group_count = schedule.GetGroupCount(department_index)
    for group_index in xrange(group_count):
      print schedule.GetGroup(department_index, group_index)
      for weekday_index in xrange(6):
        for values in schedule_tables[weekday_index][group_index]:
          print ('%d\t%s' % (values[0][0][1], values[0][0][0])).encode('utf-8')
          cell_parser.PrintValueInfo(values[0][0][0])
          print ('%d\t%s' % (values[1][0][1], values[1][0][0])).encode('utf-8')
          cell_parser.PrintValueInfo(values[1][0][0])
          print ('%d\t%s' % (values[0][1][1], values[0][1][0])).encode('utf-8')
          cell_parser.PrintValueInfo(values[0][1][0])
          print ('%d\t%s' % (values[1][1][1], values[1][1][0])).encode('utf-8')
          cell_parser.PrintValueInfo(values[1][1][0])

if __name__ == '__main__':
  assert len(sys.argv) == 2
  PrintFullSchedule(sys.argv[1])
