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

class DepartmentRangeTest(unittest.TestCase):
  def setUp(self):
    self.workbook = xlrd.open_workbook('2013_fall/4kurs.xls', formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

  def runTest(self):
    self.assertEqual(parser.department_count(self.worksheet), 9)
    self.assertEqual(parser.department_range(self.worksheet, 0), (2, 11))
    self.assertEqual(parser.department_range(self.worksheet, 1), (13, 20))
    self.assertEqual(parser.department_range(self.worksheet, 2), (22, 30))
    self.assertEqual(parser.department_range(self.worksheet, 3), (32, 34))
    self.assertEqual(parser.department_range(self.worksheet, 4), (36, 41))
    self.assertEqual(parser.department_range(self.worksheet, 5), (43, 51))
    self.assertEqual(parser.department_range(self.worksheet, 6), (53, 60))
    self.assertEqual(parser.department_range(self.worksheet, 7), (62, 69))
    self.assertEqual(parser.department_range(self.worksheet, 8), (71, 75))

if __name__ == '__main__':
   unittest.main()
