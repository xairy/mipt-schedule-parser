#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import regex
import sets
import string
import sys
import unicodedata
import xlrd

#TODO: четные недели
#TODO: альтернативныe курс.
#TODO: 'МСС-Доц. Извеков-430 ГК, Доцент Березникова М. В. . -211 ГК; Проф. Рыжак Е. И. - 532 ГК'

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
  value = Simplify(value)
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

def GetSubjects(value):
  value = Normalize(value)
  subjects = []
  for i in xrange(len(subject_res)):
    subject_re = subject_res[i]
    subject_name = subject_names[i][0]
    m = subject_re.search(value)
    if m == None:
      continue
    subject = m.group('subject')
    subjects.append(subject_name)
    value = value[:m.start('subject')] + value[m.end('subject'):]
  return subjects

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
    locations = GetLocations(value)
    teachers = GetTeachers(value)
    subjects = GetSubjects(value)
    print value.encode('utf-8')
    for subject in subjects:
      print ('<s ' + subject + ' >').encode('utf-8')
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
