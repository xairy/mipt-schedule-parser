#!/usr/bin/env python
#coding: utf-8

from __future__ import unicode_literals, division, print_function

import sys

import schedule_parser
import cell_parser

__author__ = "Alexander Konovalov"
__copyright__ = "Copyright (C) 2014 Alexander Konovalov"
__license__ = "MIT"
__version__ = "0.1"

def ParseCell(value):
  subjects = cell_parser.GetSubjects(value)
  locations = cell_parser.GetLocations(value)
  teachers = cell_parser.GetTeachers(value)

  # Subjects are strings as they are.
  locations = [cell_parser.LocationToStr(location) for location in locations]
  teachers = [cell_parser.TeacherToStr(teacher) for teacher in teachers]

  return ('$'.join(subjects), '$'.join(locations), '$'.join(teachers))

def LoadScheduleToDb(file, conn):
  schedule = schedule_parser.Schedule()
  schedule.Parse(file)

  for department_index in xrange(schedule.GetDepartmentCount()):
    schedule_tables = []

    for weekday_index in xrange(6):
      schedule_tables.append(schedule.GetScheduleTable(department_index, weekday_index))

    group_count = schedule.GetGroupCount(department_index)

    for group_index in xrange(group_count):
      group = schedule.GetGroup(department_index, group_index)

      for weekday_index in xrange(6):
        classes = schedule_tables[weekday_index][group_index]
        class_count = len(classes)

        for class_number in xrange(class_count):
          for subgroup in xrange(2):
            for class_half in xrange(2):
              raw_data = classes[class_number][subgroup][class_half][0]
              class_type = classes[class_number][subgroup][class_half][1]

              subjects, locations, teachers = ParseCell(raw_data)

              conn.execute("insert into classes values (" +
                             ":group," +
                             ":subgroup," +
                             ":week_day," +
                             ":class_number," +
                             ":class_half," +
                             ":subjects," +
                             ":locations," +
                             ":teachers," +
                             ":type," +
                             ":raw_data)",
                {"group": group,
                 "subgroup": subgroup,
                 "week_day": weekday_index,
                 "class_number": class_number,
                 "class_half": class_half,
                 "subjects": subjects,
                 "locations": locations,
                 "teachers": teachers,
                 "type": class_type,
                 "raw_data": raw_data})

  conn.commit()

if __name__ == '__main__':
  args = sys.argv[1:]
  assert len(args) >= 2

  path = args[0]
  conn = None

  if args[1] == "sqlite3":
    assert len(args) == 3

    import sqlite3
    conn = sqlite3.connect(args[2])

  elif args[1] == "mysql":
    assert len(args) == 6

    import MySQLdb
    conn = MySQLdb.connect(
      host=args[2],
      user=args[3],
      passwd=args[4],
      db=args[5])

  else:
    assert False

  LoadScheduleToDb(path, conn)