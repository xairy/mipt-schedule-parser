#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import unittest
import xlrd

import parser

__author__ = "Andrey Konovalov"
__copyright__ = "Copyright (C) 2013 Andrey Konovalov"
__license__ = "MIT"
__version__ = "0.1"

class WeekdayRangeTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetWeekdayRange(0), (4, 11))
    self.assertEqual(self.schedule.GetWeekdayRange(1), (12, 19))
    self.assertEqual(self.schedule.GetWeekdayRange(2), (20, 27))
    self.assertEqual(self.schedule.GetWeekdayRange(3), (28, 37))
    self.assertEqual(self.schedule.GetWeekdayRange(4), (38, 47))
    self.assertEqual(self.schedule.GetWeekdayRange(5), (48, 57))

class DepartmentCountTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetDepartmentCount(), 9)

class DepartmentRangeTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetDepartmentRange(0), (2, 11))
    self.assertEqual(self.schedule.GetDepartmentRange(1), (13, 20))
    self.assertEqual(self.schedule.GetDepartmentRange(2), (22, 32))
    self.assertEqual(self.schedule.GetDepartmentRange(3), (34, 36))
    self.assertEqual(self.schedule.GetDepartmentRange(4), (38, 43))
    self.assertEqual(self.schedule.GetDepartmentRange(5), (45, 53))
    self.assertEqual(self.schedule.GetDepartmentRange(6), (55, 62))
    self.assertEqual(self.schedule.GetDepartmentRange(7), (64, 71))
    self.assertEqual(self.schedule.GetDepartmentRange(8), (73, 77))

class DepartmentsRowTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetDepartmentsRow(), 3)

class HoursColumnTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetHoursColumn(), 1)

class HoursRangesTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetHoursRanges(0), [(4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11)])
    self.assertEqual(self.schedule.GetHoursRanges(3), [(28, 30), (30, 31), (31, 32), (32, 34), (34, 35), (35, 36), (36, 37)])
    self.assertEqual(self.schedule.GetHoursRanges(5), [(48, 49), (49, 50), (50, 52), (52, 53), (53, 54), (54, 56), (56, 57)])

class GroupCountTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetGroupCount(0), 9)
    self.assertEqual(self.schedule.GetGroupCount(1), 7)
    self.assertEqual(self.schedule.GetGroupCount(2), 8)
    self.assertEqual(self.schedule.GetGroupCount(3), 2)
    self.assertEqual(self.schedule.GetGroupCount(4), 5)
    self.assertEqual(self.schedule.GetGroupCount(5), 8)
    self.assertEqual(self.schedule.GetGroupCount(6), 7)
    self.assertEqual(self.schedule.GetGroupCount(7), 7)
    self.assertEqual(self.schedule.GetGroupCount(8), 4)

class GroupListTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetGroupList(0), ['011', '012', '013', '014', '015', '016', '017', '018', '019'])
    self.assertEqual(self.schedule.GetGroupList(1), ['021', '022', '023', '024', '025', '026', '028'])
    self.assertEqual(self.schedule.GetGroupList(3), ['041', '042'])
    self.assertEqual(self.schedule.GetGroupList(8), ['0111', '0112', '0113', '0114'])


class GroupRangeTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetGroupRange(0, 0), (2, 3))
    self.assertEqual(self.schedule.GetGroupRange(0, 1), (3, 4))
    self.assertEqual(self.schedule.GetGroupRange(2, 1), (23, 25))
    self.assertEqual(self.schedule.GetGroupRange(2, 2), (25, 26))
    self.assertEqual(self.schedule.GetGroupRange(2, 3), (26, 28))
    self.assertEqual(self.schedule.GetGroupRange(5, 3), (48, 49))
    self.assertEqual(self.schedule.GetGroupRange(8, 0), (73, 74))
    self.assertEqual(self.schedule.GetGroupRange(8, 3), (76, 77))

class WeekdayByRowTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetWeekdayByRow(4), 0)
    self.assertEqual(self.schedule.GetWeekdayByRow(5), 0)
    self.assertEqual(self.schedule.GetWeekdayByRow(10), 0)
    self.assertEqual(self.schedule.GetWeekdayByRow(13), 1)
    self.assertEqual(self.schedule.GetWeekdayByRow(25), 2)
    self.assertEqual(self.schedule.GetWeekdayByRow(26), 2)
    self.assertEqual(self.schedule.GetWeekdayByRow(28), 3)
    self.assertEqual(self.schedule.GetWeekdayByRow(44), 4)
    self.assertEqual(self.schedule.GetWeekdayByRow(48), 5)
    self.assertEqual(self.schedule.GetWeekdayByRow(56), 5)

class PairByRowTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetPairByRow(4), (0, 0))
    self.assertEqual(self.schedule.GetPairByRow(5), (1, 0))
    self.assertEqual(self.schedule.GetPairByRow(10), (6, 0))
    self.assertEqual(self.schedule.GetPairByRow(12), (0, 0))
    self.assertEqual(self.schedule.GetPairByRow(28), (0, 0))
    self.assertEqual(self.schedule.GetPairByRow(29), (0, 1))
    self.assertEqual(self.schedule.GetPairByRow(30), (1, 0))
    self.assertEqual(self.schedule.GetPairByRow(33), (3, 1))
    self.assertEqual(self.schedule.GetPairByRow(56), (6, 0))

class DepartmentByColumnTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetDepartmentByColumn(2), 0)
    self.assertEqual(self.schedule.GetDepartmentByColumn(3), 0)
    self.assertEqual(self.schedule.GetDepartmentByColumn(10), 0)
    self.assertEqual(self.schedule.GetDepartmentByColumn(13), 1)
    self.assertEqual(self.schedule.GetDepartmentByColumn(18), 1)
    self.assertEqual(self.schedule.GetDepartmentByColumn(19), 1)
    self.assertEqual(self.schedule.GetDepartmentByColumn(22), 2)
    self.assertEqual(self.schedule.GetDepartmentByColumn(24), 2)
    self.assertEqual(self.schedule.GetDepartmentByColumn(31), 2)
    self.assertEqual(self.schedule.GetDepartmentByColumn(39), 4)
    self.assertEqual(self.schedule.GetDepartmentByColumn(64), 7)
    self.assertEqual(self.schedule.GetDepartmentByColumn(70), 7)
    self.assertEqual(self.schedule.GetDepartmentByColumn(73), 8)
    self.assertEqual(self.schedule.GetDepartmentByColumn(76), 8)

class GroupByColumnTest(unittest.TestCase):
  def setUp(self):
    self.schedule = parser.Schedule()
    self.schedule.Parse('2013_fall/4kurs.xls')

  def runTest(self):
    self.assertEqual(self.schedule.GetGroupByColumn(2), (0, 0))
    self.assertEqual(self.schedule.GetGroupByColumn(3), (1, 0))
    self.assertEqual(self.schedule.GetGroupByColumn(10), (8, 0))
    self.assertEqual(self.schedule.GetGroupByColumn(23), (1, 0))
    self.assertEqual(self.schedule.GetGroupByColumn(24), (1, 1))
    self.assertEqual(self.schedule.GetGroupByColumn(25), (2, 0))
    self.assertEqual(self.schedule.GetGroupByColumn(26), (3, 0))
    self.assertEqual(self.schedule.GetGroupByColumn(27), (3, 1))
    self.assertEqual(self.schedule.GetGroupByColumn(76), (3, 0))

if __name__ == '__main__':
   unittest.main()
