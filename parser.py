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

DAYS = u'Дни'
HOURS = u'Часы'

class Schedule:
  def __init__(self):
    pass

  def Parse(self, file):
    self.workbook = xlrd.open_workbook(file, formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

    self.ParseWeekdays()
    self.ParseDepartments()
    self.ParseGroups()

  def ParseWeekdays(self):
    self.weekday_ranges = []
    weekdays = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY]
    for day in weekdays:
      ranges = []
      for (rb, re, cb, ce) in self.worksheet.merged_cells:
        if self.worksheet.cell_value(rb, cb) == day:
          ranges.append((rb, re))
      assert len(ranges) > 0
      for i in xrange(len(ranges) - 1):
        assert ranges[i] == ranges[i + 1]
      self.weekday_ranges.append(ranges[0])

  def ParseDepartments(self):
    self.department_ranges = []
    days_cols = []
    hours_cols = []
    rows = []
    for row in xrange(self.worksheet.nrows):
      for col in xrange(self.worksheet.ncols):
        if self.worksheet.cell_value(row, col) == DAYS:
          days_cols.append(col)
          rows.append(row)
        if self.worksheet.cell_value(row, col) == HOURS:
          hours_cols.append(col)
          rows.append(row)
    assert len(days_cols) == len(hours_cols)
    for k in xrange(len(days_cols)):
      beg = hours_cols[k] + 1
      end = days_cols[k + 1] if (k + 1 < len(days_cols)) else self.worksheet.ncols
      self.department_ranges.append((beg, end))
    assert len(rows) > 0
    for k in xrange(len(rows) - 1):
      assert rows[k] == rows[k + 1]
    self.departments_row = rows[0]

  def ParseGroups(self):
    self.groups = []
    self.group_ranges = []
    for department in xrange(self.GetDepartmentCount()):
      dep_groups = []
      dep_group_ranges = []
      dep_range = self.department_ranges[department]
      dep_row = self.departments_row
      for column in xrange(dep_range[0], dep_range[1]):
        beg, end = 0, 0
        group = self.worksheet.cell_value(dep_row, column).encode('ascii')
        if group != '':
          dep_groups.append(group)
          beg, end = column, column + 1
          while end < self.worksheet.ncols and len(self.worksheet.cell_value(dep_row, end)) == 0:
            end += 1
          dep_group_ranges.append((beg, end))
      self.groups.append(dep_groups)
      self.group_ranges.append(dep_group_ranges)

  def GetWeekdayRange(self, weekday_index):
    return self.weekday_ranges[weekday_index]

  def GetDepartmentCount(self):
    return len(self.department_ranges)

  def GetDepartmentRange(self, department_index):
    return self.department_ranges[department_index]

  def GetDepartmentsRow(self):
    return self.departments_row

  def GetGroupCount(self, department_index):
    return len(self.groups[department_index])

  def GetGroupList(self, department_index):
    return self.groups[department_index]

  def GetGroupRange(self, department_index, group_index):
    return self.group_ranges[department_index][group_index]
