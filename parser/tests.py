#!/usr/bin/python
#coding: utf-8

import unittest
import xlrd

import parser

class WeekdayRangeTest(unittest.TestCase):
  def setUp(self):
    self.workbook = xlrd.open_workbook('2013_fall/4kurs.xls', formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

  def runTest(self):
     self.assertEqual(parser.weekday_range(self.worksheet, parser.MONDAY), (4, 11))
     self.assertEqual(parser.weekday_range(self.worksheet, parser.TUESDAY), (12, 19))
     self.assertEqual(parser.weekday_range(self.worksheet, parser.WEDNESDAY), (20, 27))
     self.assertEqual(parser.weekday_range(self.worksheet, parser.THURSDAY), (28, 37))
     self.assertEqual(parser.weekday_range(self.worksheet, parser.FRIDAY), (38, 47))
     self.assertEqual(parser.weekday_range(self.worksheet, parser.SATURDAY), (48, 57))

if __name__ == '__main__':
   unittest.main()
