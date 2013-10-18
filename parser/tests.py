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
    self.assertEqual(parser.department_range(self.worksheet, 2), (22, 32))
    self.assertEqual(parser.department_range(self.worksheet, 3), (34, 36))
    self.assertEqual(parser.department_range(self.worksheet, 4), (38, 43))
    self.assertEqual(parser.department_range(self.worksheet, 5), (45, 53))
    self.assertEqual(parser.department_range(self.worksheet, 6), (55, 62))
    self.assertEqual(parser.department_range(self.worksheet, 7), (64, 71))
    self.assertEqual(parser.department_range(self.worksheet, 8), (73, 77))

class DepartmentsRowTest(unittest.TestCase):
  def setUp(self):
    self.workbook = xlrd.open_workbook('2013_fall/4kurs.xls', formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

  def runTest(self):
    self.assertEqual(parser.departments_row(self.worksheet), 3)

class GroupCountTest(unittest.TestCase):
  def setUp(self):
    self.workbook = xlrd.open_workbook('2013_fall/4kurs.xls', formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

  def runTest(self):
    self.assertEqual(parser.group_count(self.worksheet, 0), 9)
    self.assertEqual(parser.group_count(self.worksheet, 1), 7)
    self.assertEqual(parser.group_count(self.worksheet, 2), 8)
    self.assertEqual(parser.group_count(self.worksheet, 3), 2)
    self.assertEqual(parser.group_count(self.worksheet, 4), 5)
    self.assertEqual(parser.group_count(self.worksheet, 5), 8)
    self.assertEqual(parser.group_count(self.worksheet, 6), 7)
    self.assertEqual(parser.group_count(self.worksheet, 7), 7)
    self.assertEqual(parser.group_count(self.worksheet, 8), 4)

class GroupRangeTest(unittest.TestCase):
  def setUp(self):
    self.workbook = xlrd.open_workbook('2013_fall/4kurs.xls', formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

  def runTest(self):
    self.assertEqual(parser.group_range(self.worksheet, 0, 0), (2, 3))
    self.assertEqual(parser.group_range(self.worksheet, 0, 1), (3, 4))
    self.assertEqual(parser.group_range(self.worksheet, 2, 1), (23, 25))
    self.assertEqual(parser.group_range(self.worksheet, 2, 2), (25, 26))
    self.assertEqual(parser.group_range(self.worksheet, 2, 3), (26, 28))
    self.assertEqual(parser.group_range(self.worksheet, 5, 3), (48, 49))
    self.assertEqual(parser.group_range(self.worksheet, 8, 0), (73, 74))
    self.assertEqual(parser.group_range(self.worksheet, 8, 3), (76, 77))

class GroupListTest(unittest.TestCase):
  def setUp(self):
    self.workbook = xlrd.open_workbook('2013_fall/4kurs.xls', formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

  def runTest(self):
    self.assertEqual(parser.group_list(self.worksheet, 0), ['011', '012', '013', '014', '015', '016', '017', '018', '019'])
    self.assertEqual(parser.group_list(self.worksheet, 1), ['021', '022', '023', '024', '025', '026', '028'])
    self.assertEqual(parser.group_list(self.worksheet, 3), ['041', '042'])
    self.assertEqual(parser.group_list(self.worksheet, 8), ['0111', '0112', '0113', '0114'])

if __name__ == '__main__':
   unittest.main()
