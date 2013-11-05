#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import fileinput
import regex
import sets
import string
import sys
import unicodedata
import xlrd

__author__ = "Andrey Konovalov"
__copyright__ = "Copyright (C) 2013 Andrey Konovalov"
__license__ = "MIT"
__version__ = "0.1"

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
def CapitalVary(s):
  if s == '':
    return ['']
  result = []
  head_lower = s[0].lower()
  head_upper = s[0].upper()
  tail_list = CapitalVary(s[1:])
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
    '(?P<surname>[А-ЯЁ][а-яё]+(?:\-[А-ЯЁ][а-яё]+)?)' + ' ' + \
    '(?P<first_initial>[А-ЯЁ])\.?' + ' ' + \
    '(?P<second_initial>[А-ЯЁ])\.?' + \
  ')' + \
  '(?:[^а-яА-ЯёЁ]|$)'
)

second_teacher_re = regex.compile(
  '(?:/|\-)' + \
  '(?:[^/\-]*? |)' + \
  '(?P<teacher>' + \
    '(?P<surname>[А-ЯЁ][а-яё]+(?:\-[А-ЯЁ][а-яё]+)?)' + \
  ')' + \
  ' ?(?:/|\-)'
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

subject_res = []
subject_names = [[]]
with open('subjects') as subject_file:
  while True:
    line = subject_file.readline().decode('utf-8')
    if line == '':
      break;
    line = line.rstrip()
    if len(line) > 0:
      subject_names[-1].append(line)
    else:
      assert len(subject_names[-1]) > 0
      subject_re = regex.compile( \
        '(?P<subject>' + '|'.join(subject_names[-1]) + ')' \
      )
      subject_res.append(subject_re)
      subject_names.append([])

# Removes consecutive whitespaces, adds a space after each dot.
def Simplify(s):
  s = s.replace('.', '. ')
  s = ' '.join(s.split())
  return s

unicode_punctuation_dict = dict((i, ' ') for i in xrange(sys.maxunicode)
                                if unicodedata.category(unichr(i)).startswith('P'))

# Does what Simplify() does, removes all punctuation and lowers case.
def Normalize(s):
  s = s.replace('.', '. ')
  s = s.translate(unicode_punctuation_dict)
  s = s.lower()
  s = ' '.join(s.split())
  return s

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
  value = Simplify(value)
  teacher_entries = []
  while True:
    m = first_teacher_re.search(value)
    if m == None:
      break
    teacher = m.group('teacher')
    surname = m.group('surname')
    first_initial = m.group('first_initial')
    second_initial = m.group('second_initial')
    start = m.start('teacher')
    end = m.end('teacher')
    if len(surname) >= 3:
      teacher_entries.append((start, (surname, first_initial, second_initial)))
    value = value[:start] + ('$' * len(teacher)) + value[end:]
  m = second_teacher_re.search(value)
  if m != None:
    teacher = m.group('teacher')
    surname = m.group('surname')
    start = m.start('teacher')
    end = m.end('teacher')
    if len(surname) >= 3:
      teacher_entries.append((start, (surname, None, None)))
    value = value[:start] + ('$' * len(teacher)) + value[end:]
  teacher_entries.sort()
  teacher_list = [teacher for (offset, teacher) in teacher_entries]
  return teacher_list

def GetLocations(value):
  value = Simplify(value)
  location_entries = []
  while True:
    m = building_room_re.search(value)
    if m == None:
      break
    location = m.group('location')
    room = m.group('room')
    building = m.group('building')
    for building_kind in [gk, lk, nk, kpm, rtk]:
      if building in building_kind:
        building = building_kind[0]
    start = m.start('location')
    end = m.end('location')
    location_entries.append((start, (room, building)))
    value = value[:start] + ('$' * len(location)) + value[end:]
  while True:
    m = lecture_room_re.search(value)
    if m == None:
      break
    location = m.group('location')
    room = m.group('room')
    for room_kind in [bh, bf, gf, az, cz]:
      if room in room_kind:
        room = room_kind[0]
    start = m.start('location')
    end = m.end('location')
    location_entries.append((start, (room, None)))
    value = value[:start] + ('$' * len(location)) + value[end:]
  location_entries.sort()
  unique_locations = []
  for (offset, location) in location_entries:
    if location not in unique_locations:
      unique_locations.append(location)
  return unique_locations

def GetSubjects(value):
  value = Normalize(value)
  subject_entries = []
  for i in xrange(len(subject_res)):
    subject_re = subject_res[i]
    subject_name = subject_names[i][0]
    m = subject_re.search(value)
    if m == None:
      continue
    subject = m.group('subject')
    start = m.start('subject')
    end = m.end('subject')
    subject_entries.append((start, subject_name))
    value = value[:start] + ('$' * len(subject)) + value[end:]
  subject_entries.sort()
  subjects = [subject for (offset, subject) in subject_entries]
  return subjects

def TeacherToStr(teacher):
  s = teacher[0]
  if teacher[1] != None and teacher[2] != None:
    s += ' ' + teacher[1] + '. ' + teacher[2] + '.'
  return s

def LocationToStr(locations):
  s = location[0]
  if location[1] != None:
    s += ' ' + location[1]
  return s

if __name__ == '__main__':
  for value in fileinput.input():
    value = value.decode('utf-8')

    subjects = GetSubjects(value)
    locations = GetLocations(value)
    teachers = GetTeachers(value)

    # Subjects are string as they are.
    locations = [LocationToStr(location) for location in locations]
    teachers = [TeacherToStr(teacher) for teacher in teachers]

    print '$'.join(subjects).encode('utf-8')
    print '$'.join(locations).encode('utf-8')
    print '$'.join(teachers).encode('utf-8')
