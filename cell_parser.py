#!/usr/bin/python
#coding: utf-8

import math
import regex
import sets
import sys
import xlrd

#TODO: import from future.
#TODO: 'Б. Хим' -> 'Б. Хим.' etc.

def DotCapitalJoin(list):
  if list == []:
    return [u'']
  result = []
  tail = DotCapitalJoin(list[1:])
  head_lower = list[0]
  head_upper = list[0][0].upper() + list[0][1:]
  for elem in tail:
    result.append((head_upper + u'. ' + elem).rstrip())
    result.append((head_upper + u' ' + elem).rstrip())
    result.append((head_lower + u'. ' + elem).rstrip())
    result.append((head_lower + u' ' + elem).rstrip())
  return result

buildings = [u'ГК', u'ЛК', u'НК', u'КПМ', u'РТК']
bh = DotCapitalJoin([u'б', u'хим'])
bf = DotCapitalJoin([u'б', u'физ'])
gf = DotCapitalJoin([u'гл', u'физ'])
az = DotCapitalJoin([u'акт', u'зал'])
lecture_rooms = bh + bf + gf + az

first_teacher_re = regex.compile(
  u'(?P<teacher>' + \
    u'(?P<surname>[А-ЯЁ][а-яА-ЯёЁ-]+)' + ' ' + \
    u'(?P<first_initial>[А-ЯЁ])\.?' + ' ' + \
    u'(?P<second_initial>[А-ЯЁ])\.?' + \
  u')' + \
  u'(?:[^а-яА-ЯёЁ]|$)'
)

second_teacher_re = regex.compile(
  u'/(?P<teacher>' + \
    u'(?:[^/]*? |)' + \
    u'(?P<surname>[А-ЯЁ][а-яА-ЯёЁ-]+)' + \
    u'(?:' + ' ' + \
      u'(?P<first_initial>[А-Я])\.?' + ' ' + \
      u'(?P<second_initial>[А-Я])\.?' + \
    u')?' + ' ?' + \
  u')/'
)

first_location_re = regex.compile(
  u'(?P<location>' + \
    u'(?P<room>[0-9]+а?)' + u' ?' + \
    u'(?P<building>' + u'|'.join(buildings) + u')' + \
  u')' + \
  u'(?:[^а-яА-ЯёЁ]|$)'
)

second_location_re = regex.compile(
  u'(?P<location>' + \
    u'(?P<room>' + u'|'.join(lecture_rooms) + u')' + \
  u')' + \
  u'(?:[^а-яА-ЯёЁ]|$)'
)

# Removes consecutive whitespaces, adds a space after each dot,
# makes the first letter of a word after a dot capital.
def Normalize(string):
  string = string.replace(u'.', u'. ')
  string = u' '.join(string.split())
  return string

def GetValues(file):
  workbook = xlrd.open_workbook(file, formatting_info=True)
  worksheet = workbook.sheet_by_index(0)

  values = sets.Set()
  for (rb, re, cb, ce) in worksheet.merged_cells:
    for row in xrange(worksheet.nrows):
      for col in xrange(worksheet.ncols):
        value = worksheet.cell_value(row, col)
        if len(value) >= 4:
          #value = value.encode('utf-8')
          values.add(value)
  return values

def GetTeachers(value):
  teachers = []
  while True:
    m = first_teacher_re.search(value)
    if m == None:
      break
    surname = m.group(u'surname')
    first_initial = m.group(u'first_initial')
    second_initial = m.group(u'second_initial')
    if len(surname) >= 3:
      teachers.append((surname, first_initial, second_initial))
    value = value[:m.start(u'teacher')] + value[m.end(u'teacher'):]
  if len(teachers) == 0:
    m = second_teacher_re.search(value)
    if m != None:
      surname = m.group(u'surname')
      first_initial = m.group(u'first_initial')
      second_initial = m.group(u'second_initial')
      if len(surname) >= 3:
        teachers.append((surname, first_initial, second_initial))
  return teachers

def GetLocations(value):
  locations = []
  while True:
    m = first_location_re.search(value)
    if m == None:
      break
    room = m.group(u'room')
    building = m.group(u'building')
    locations.append((room, building))
    value = value[:m.start(u'location')] + value[m.end(u'location'):]
  while True:
    m = second_location_re.search(value)
    if m == None:
      break
    room = m.group(u'room')
    locations.append((room, None))
    value = value[:m.start(u'location')] + value[m.end(u'location'):]
  return locations

if __name__ == '__main__':
  values = \
    GetValues('2013_fall/1kurs.xls').union( \
    GetValues('2013_fall/2kurs.xls')).union( \
    GetValues('2013_fall/3kurs.xls')).union( \
    GetValues('2013_fall/4kurs.xls')).union( \
    GetValues('2013_fall/5kurs.xls')).union( \
    GetValues('2013_fall/6kurs.xls') \
  )

  for value in values:
    value = Normalize(value)
    locations = GetLocations(value)
    teachers = GetTeachers(value)
    print value.encode('utf-8')
    for location in locations:
      print u'<l'.encode('utf-8'),
      if location[0] != None:
        print location[0].encode('utf-8'),
      if location[1] != None:
        print location[1].encode('utf-8'),
      print u'>'.encode('utf-8')
    for teacher in teachers:
      print u'<t'.encode('utf-8'),
      if teacher[0] != None:
        print teacher[0].encode('utf-8'),
      if teacher[1] != None:
        print teacher[1].encode('utf-8'),
      if teacher[2] != None:
        print teacher[2].encode('utf-8'),
      print u'>'.encode('utf-8')
    print
