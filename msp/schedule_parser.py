#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import sys
import xlrd

__author__ = "Andrey Konovalov"
__copyright__ = "Copyright (C) 2014 Andrey Konovalov"
__license__ = "MIT"
__version__ = "0.1"

DAYS = 'Дни'
HOURS = 'Часы'

MONDAY = 'Понедельник'
TUESDAY = 'Вторник'
WEDNESDAY = 'Среда'
THURSDAY = 'Четверг'
FRIDAY = 'Пятница'
SATURDAY = 'Суббота'

WEEKDAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY]

PAIRS_PER_DAY = 7

class Schedule:
  def __init__(self):
    pass

  def Parse(self, file):
    self.workbook = xlrd.open_workbook(file, formatting_info=True)
    self.worksheet = self.workbook.sheet_by_index(0)

    self.ParseWeekdays()
    self.ParseDepartments()
    self.ParseHours()
    self.ParseGroups()

  def ParseWeekdays(self):
    self.weekday_ranges = []
    for day in WEEKDAYS:
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
    self.hours_column = hours_cols[0]

  def ParseHours(self):
    self.hours_ranges = []
    for weekday_range in self.weekday_ranges:
      weekday_hours_ranges = []
      last = weekday_range[0]
      for row in xrange(weekday_range[0] + 1, weekday_range[1]):
        value = self.worksheet.cell_value(row, self.hours_column)
        if value != '':
          weekday_hours_ranges.append((last, row))
          last = row
      weekday_hours_ranges.append((last, weekday_range[1]))
      self.hours_ranges.append(weekday_hours_ranges)

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
        group = self.worksheet.cell_value(dep_row, column)
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

  def GetHoursColumn(self):
    return self.hours_column

  def GetHoursRanges(self, weekday_index):
    return self.hours_ranges[weekday_index]

  def GetGroupCount(self, department_index):
    return len(self.groups[department_index])

  def GetGroupList(self, department_index):
    return self.groups[department_index]

  def GetGroup(self, department_index, group_index):
    return self.groups[department_index][group_index]

  def GetGroupRange(self, department_index, group_index):
    return self.group_ranges[department_index][group_index]

  def GetWeekdayByRow(self, row):
    for index in xrange(len(self.weekday_ranges)):
      wr = self.weekday_ranges[index]
      if wr[0] <= row and row < wr[1]:
        return index
    assert False

  def GetPairByRow(self, row):
    weekday_index = self.GetWeekdayByRow(row)
    hours_ranges = self.hours_ranges[weekday_index]
    for index in xrange(len(hours_ranges)):
      hr = hours_ranges[index]
      if hr[0] <= row and row < hr[1]:
        return (index, row - hr[0])
    assert False

  def GetDepartmentIndexByColumn(self, column):
    for index in xrange(len(self.department_ranges)):
      dr = self.department_ranges[index]
      if dr[0] <= column and column < dr[1]:
        return index
    assert False

  def GetGroupIndexByColumn(self, column):
    department_index = self.GetDepartmentIndexByColumn(column)
    group_ranges = self.group_ranges[department_index]
    for index in xrange(len(group_ranges)):
      gr = group_ranges[index]
      if gr[0] <= column and column < gr[1]:
        return (index, column - gr[0])
    assert False

  def GetCellColor(self, row, column):
    cell = self.worksheet.cell(row, column)
    xfx = self.worksheet.cell_xf_index(row, column)
    xf = self.workbook.xf_list[xfx]
    bgx = xf.background.pattern_colour_index
    rgb = self.workbook.colour_map[bgx]
    # (204, 255, 204) -> 0 : empty, (204, 255, 255) -> 1 : seminar,
    # (255, 153, 204) -> 2 : lecture, (255, 255, 153) -> 3 : other
    if rgb == (204, 255, 204):
      return 0
    elif rgb == (204, 255, 255):
      return 1
    elif rgb == (255, 153, 204):
      return 2
    elif rgb == (255, 255, 153):
      return 3
    return -1

  def GetScheduleTable(self, department_index, weekday_index):
    dr = self.department_ranges[department_index]
    wr = self.weekday_ranges[weekday_index]

    groups_count = len(self.groups[department_index])
    schedule_table = [[[[('', 0), ('', 0)], [('', 0), ('', 0)]]
      for i in xrange(PAIRS_PER_DAY)] for i in xrange(groups_count)]

    for (rb, re, cb, ce) in self.worksheet.merged_cells:
      if wr[0] <= rb and re <= wr[1] and dr[0] <= cb and ce <= dr[1]:
        value = self.worksheet.cell_value(rb, cb)
        color = self.GetCellColor(rb, cb)
        if value == '':
          continue
        for row in xrange(rb, re):
          for column in xrange(cb, ce):
            p1, p2 = self.GetPairByRow(row)
            g1, g2 = self.GetGroupIndexByColumn(column)
            schedule_table[g1][p1][g2][p2] = (value, color)

            hr = self.hours_ranges[weekday_index][p1]
            gr = self.group_ranges[department_index][g1]

            if p2 == 0 and hr[1] - hr[0] == 1:
              schedule_table[g1][p1][g2][1] = (value, color)
            if g2 == 0 and gr[1] - gr[0] == 1:
              schedule_table[g1][p1][1][p2] = (value, color)
            if p2 == 0 and hr[1] - hr[0] == 1 and g2 == 0 and gr[1] - gr[0] == 1:
              schedule_table[g1][p1][1][1] = (value, color)

    for row in xrange(wr[0], wr[1]):
      for column in xrange(dr[0], dr[1]):
        value = self.worksheet.cell_value(row, column)
        color = self.GetCellColor(row, column)
        if value == '':
          continue

        p1, p2 = self.GetPairByRow(row)
        g1, g2 = self.GetGroupIndexByColumn(column)
        schedule_table[g1][p1][g2][p2] = (value, color)

        hr = self.hours_ranges[weekday_index][p1]
        gr = self.group_ranges[department_index][g1]

        if p2 == 0 and hr[1] - hr[0] == 1:
          schedule_table[g1][p1][g2][1] = (value, color)
        if g2 == 0 and gr[1] - gr[0] == 1:
          schedule_table[g1][p1][1][p2] = (value, color)
        if p2 == 0 and hr[1] - hr[0] == 1 and g2 == 0 and gr[1] - gr[0] == 1:
          schedule_table[g1][p1][1][1] = (value, color)

    return schedule_table

  # Events

  # XXX(xairy): returns list of groups, not subgroups.
  def GetGroupsByColumnRange(self, rng):
    d1 = self.GetDepartmentIndexByColumn(rng[0])
    d2 = self.GetDepartmentIndexByColumn(rng[1] - 1)
    assert d1 == d2
    groups = []
    for column in xrange(rng[0], rng[1]):
      g1, g2 = self.GetGroupIndexByColumn(column)
      group = self.GetGroup(d1, g1)
      if group not in groups:
        groups.append(group)
    return groups

  # FIXME(xairy): naive implementation, sometimes doesn't work correctly.
  def GetPairRangeByRowRange(self, rng):
    start = self.GetPairByRow(rng[0])
    end = self.GetPairByRow(rng[1] - 1)
    return start[0], end[0]

  # FIXME(xairy): naive implementation, sometimes doesn't work correctly.
  def GetEvents(self, department_index, weekday_index):
    dr = self.department_ranges[department_index]
    wr = self.weekday_ranges[weekday_index]

    # event = {'start': ..., 'end': ..., 'groups': [...], 'value': ...}
    events = []
    merged_cells = []

    for (rb, re, cb, ce) in self.worksheet.merged_cells:
      if wr[0] <= rb and re <= wr[1] and dr[0] <= cb and ce <= dr[1]:
        merged_cells.append((rb, re, cb, ce))
        value = self.worksheet.cell_value(rb, cb)

        if value == '':
          continue
        color = self.GetCellColor(rb, cb)
        groups = self.GetGroupsByColumnRange((cb, ce))
        start, end = self.GetPairRangeByRowRange((rb, re))
        events.append({})
        events[-1]['value'] = value
        events[-1]['start'] = start
        events[-1]['end'] = end
        events[-1]['groups'] = groups
        events[-1]['color'] = color

    for row in xrange(wr[0], wr[1]):
      for column in xrange(dr[0], dr[1]):
        in_merged = False
        for (rb, re, cb, ce) in merged_cells:
          if rb <= row < re and cb <= column < ce:
            in_merged = True
            break
        if in_merged:
          continue
        value = self.worksheet.cell_value(row, column)

        if value == '':
          continue
        color = self.GetCellColor(row, column)
        groups = self.GetGroupsByColumnRange((column, column + 1))
        start, end = self.GetPairRangeByRowRange((row, row + 1))
        events.append({})
        events[-1]['value'] = value
        events[-1]['start'] = start
        events[-1]['end'] = end
        events[-1]['groups'] = groups
        events[-1]['color'] = color

    return events

def PrintEvents(file):
  schedule = Schedule()
  schedule.Parse(file)
  events = schedule.GetEvents(7, 0)
  for event in events:
    print event['start'], event['end'], event['groups'], event['value']

def PrintSchedule(file):
  schedule = Schedule()
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
          print ('%d\t%s' % (values[1][0][1], values[1][0][0])).encode('utf-8')
          print ('%d\t%s' % (values[0][1][1], values[0][1][0])).encode('utf-8')
          print ('%d\t%s' % (values[1][1][1], values[1][1][0])).encode('utf-8')

if __name__ == '__main__':
  assert len(sys.argv) == 2
  PrintSchedule(sys.argv[1])
