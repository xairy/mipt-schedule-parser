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

def weekday_range(worksheet, weekday):
  ranges = []
  for (rb, re, cb, ce) in worksheet.merged_cells:
    if worksheet.cell_value(rb, cb) == weekday:
      ranges.append((rb, re))
  assert len(ranges) != 0
  for i in xrange(len(ranges) - 1):
    assert ranges[i] == ranges[i + 1]
  return ranges[0]

def department_count(worksheet):
  days = 0
  hours = 0
  for row in xrange(worksheet.nrows):
    for col in xrange(worksheet.ncols):
      if worksheet.cell_value(row, col) == DAYS:
        days += 1
      if worksheet.cell_value(row, col) == HOURS:
        hours += 1
  assert days == hours
  return days

def department_range(worksheet, index):
  days = []
  hours = []
  for row in xrange(worksheet.nrows):
    for col in xrange(worksheet.ncols):
      if worksheet.cell_value(row, col) == DAYS:
        days.append(col)
      if worksheet.cell_value(row, col) == HOURS:
        hours.append(col)
  days.sort()
  hours.sort()
  assert len(days) == len(hours)
  assert index < len(days)
  beg = hours[index] + 1
  end = days[index + 1] if (index + 1 < len(days)) else worksheet.ncols
  return (beg, end)

def departments_row(worksheet):
  rows = []
  for row in xrange(worksheet.nrows):
    for col in xrange(worksheet.ncols):
      if worksheet.cell_value(row, col) == DAYS:
        rows.append(row)
      if worksheet.cell_value(row, col) == HOURS:
        rows.append(row)
  rows.sort()
  assert len(rows) > 0
  for i in xrange(len(rows) - 1):
    assert rows[i] == rows[i + 1]
  return rows[0]

def group_list(worksheet, department_index):
  dep_range = department_range(worksheet, department_index)
  dep_row = departments_row(worksheet)
  groups = []
  for column in xrange(dep_range[0], dep_range[1]):
    group = worksheet.cell_value(dep_row, column).encode('ascii')
    if group != '':
      groups.append(group)
  return groups

def group_count(worksheet, department_index):
  return len(group_list(worksheet, department_index))

def group_range(worksheet, department_index, group_index):
  dep_range = department_range(worksheet, department_index)
  dep_row = departments_row(worksheet)
  groups = group_list(worksheet, department_index)
  group = groups[group_index]
  beg, end = 0, 0
  for column in xrange(dep_range[0], dep_range[1]):
    if worksheet.cell_value(dep_row, column).encode('ascii') == group:
      beg = column
  end = beg + 1
  while end < worksheet.ncols and len(worksheet.cell_value(dep_row, end)) == 0:
    end += 1
  return (beg, end)

