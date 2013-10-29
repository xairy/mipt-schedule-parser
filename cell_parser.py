#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import regex
import sets
import sys
import xlrd

#TODO: четные недели
#TODO: альтернативныe курс.

# ['ii', 'ee'] -> ['ii ee', 'ii ee.', 'ii. ee', 'ii. ee.',
#                  'Ii ee', 'Ii ee.', 'Ii. ee', 'Ii. ee.',
#                  'ii Ee', 'ii Ee.', 'ii. Ee', 'ii. Ee.',
#                  'Ii Ee', 'Ii Ee.', 'Ii. Ee', 'Ii. Ee.']
def DotCapitalJoin(list):
  if list == []:
    return ['']
  result = []
  head_lower = list[0]
  head_upper = list[0][0].upper() + list[0][1:]
  tail_list = DotCapitalJoin(list[1:])
  for elem in tail_list:
    result.append((head_upper + '. ' + elem).rstrip())
    result.append((head_upper + ' ' + elem).rstrip())
    result.append((head_lower + '. ' + elem).rstrip())
    result.append((head_lower + ' ' + elem).rstrip())
  return result

# 'ieg' -> ['ieg', 'Ieg', 'iEg', 'IEg', 'ieG', 'IeG', 'iEG', 'IEG']
def CapitalVary(string):
  if string == '':
    return ['']
  result = []
  head_lower = string[0].lower()
  head_upper = string[0].upper()
  tail_list = CapitalVary(string[1:])
  for elem in tail_list:
    result.append(head_lower + elem)
    result.append(head_upper + elem)
  return result

gk = ['ГК'] + CapitalVary('ГК')
lk = ['ЛК'] + CapitalVary('ЛК')
nk = ['НК'] + CapitalVary('НК')
kpm = ['КПМ'] + CapitalVary('КПМ')
rtk = ['РТК'] + CapitalVary('РТК')
buildings = gk + lk + nk + kpm + rtk

bh = ['Б. Хим.'] + DotCapitalJoin(['б', 'хим'])
bf = ['Б. Физ.'] + DotCapitalJoin(['б', 'физ'])
gf = ['Гл. Физ.'] + DotCapitalJoin(['гл', 'физ'])
az = ['Акт. Зал'] + DotCapitalJoin(['акт', 'зал'])
cz = ['Чит. Зал'] + DotCapitalJoin(['чит', 'зал'])
lecture_rooms = bh + bf + gf + az + cz

first_teacher_re = regex.compile(
  '(?P<teacher>' + \
    '(?P<surname>[А-ЯЁ][а-яА-ЯёЁ-]+)' + ' ' + \
    '(?P<first_initial>[А-ЯЁ])\.?' + ' ' + \
    '(?P<second_initial>[А-ЯЁ])\.?' + \
  ')' + \
  '(?:[^а-яА-ЯёЁ]|$)'
)

second_teacher_re = regex.compile(
  '/' + \
  '(?:[^/]*? |)' + \
  '(?P<teacher>' + \
    '(?P<surname>[А-ЯЁ][а-яА-ЯёЁ-]+)' + \
    '(?:' + ' ' + \
      '(?P<first_initial>[А-Я])\.?' + ' ' + \
      '(?P<second_initial>[А-Я])\.?' + \
    ')?' + \
  ')' + \
  ' ?/'
)

building_room_re = regex.compile(
  '(?P<location>' + \
    '(?P<room>[0-9]+а?)' + ' ?' + \
    '(?P<building>' + '|'.join(buildings) + ')' + \
  ')' + \
  '(?:[^а-яА-ЯёЁ]|$)'
)

lecture_room_re = regex.compile(
  '(?P<location>' + \
    '(?P<room>' + '|'.join(lecture_rooms) + ')' + \
  ')' + \
  '(?:[^а-яА-ЯёЁ]|$)'
)

# Removes consecutive whitespaces, adds a space after each dot,
# makes the first letter of a word after a dot capital.
def Normalize(string):
  string = string.replace('.', '. ')
  string = ' '.join(string.split())
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
    surname = m.group('surname')
    first_initial = m.group('first_initial')
    second_initial = m.group('second_initial')
    if len(surname) >= 3:
      teachers.append((surname, first_initial, second_initial))
    value = value[:m.start('teacher')] + value[m.end('teacher'):]
  if len(teachers) == 0:
    m = second_teacher_re.search(value)
    if m != None:
      surname = m.group('surname')
      first_initial = m.group('first_initial')
      second_initial = m.group('second_initial')
      if len(surname) >= 3:
        teachers.append((surname, first_initial, second_initial))
      value = value[:m.start('teacher')] + value[m.end('teacher'):]
  return teachers

def GetLocations(value):
  locations = []
  while True:
    m = building_room_re.search(value)
    if m == None:
      break
    room = m.group('room')
    building = m.group('building')
    if building in gk:
      building = gk[0]
    if building in lk:
      building = lk[0]
    if building in nk:
      building = nk[0]
    if building in kpm:
      building = kpm[0]
    if building in rtk:
      building = rtk[0]
    location = (room, building)
    if location not in locations:
      locations.append(location)
    value = value[:m.start('location')] + value[m.end('location'):]
  while True:
    m = lecture_room_re.search(value)
    if m == None:
      break
    room = m.group('room')
    if room in bh:
      room = bh[0]
    if room in bf:
      room = bf[0]
    if room in gf:
      room = gf[0]
    if room in az:
      room = az[0]
    if room in cz:
      room = cz[0]
    location = (room, None)
    if location not in locations:
      locations.append(location)
    value = value[:m.start('location')] + value[m.end('location'):]
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

  for value in values0:
    value = Normalize(value)
    locations = GetLocations(value)
    teachers = GetTeachers(value)
    print value.encode('utf-8')
    for location in locations:
      print '<l'.encode('utf-8'),
      if location[0] != None:
        print location[0].encode('utf-8'),
      if location[1] != None:
        print location[1].encode('utf-8'),
      print '>'.encode('utf-8')
    for teacher in teachers:
      print '<t'.encode('utf-8'),
      if teacher[0] != None:
        print teacher[0].encode('utf-8'),
      if teacher[1] != None:
        print teacher[1].encode('utf-8'),
      if teacher[2] != None:
        print teacher[2].encode('utf-8'),
      print '>'.encode('utf-8')
    print
