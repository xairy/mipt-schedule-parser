#!/usr/bin/python
#coding: utf-8

import unittest
import xlrd

import parser

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

if __name__ == '__main__':
   unittest.main()
