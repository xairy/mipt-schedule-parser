#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import unittest
import xlrd

import cell_parser

class LocationsTest(unittest.TestCase):
  def setUp(self):
    self.cases = [ \
      ( \
        'МСС /211 ГК , 532 ГК/', \
        [('211', 'ГК'), ('532', 'ГК')] \
      ), ( \
        'Теория игр и принятие решений / Доцент Меньшиков И. С. - для "кт" и "эк" - обязательно; для "мф" - а. к. -1 110 КПМ', \
        [('110', 'КПМ')] \
      ), ( \
        'Механика сплошных сред Проф. Жмур В. В. -211 ГК проф. Рыжак Е. И. - 532 ГК', \
        [('211', 'ГК'), ('532', 'ГК')] \
      ), ( \
        'Альтерн. курсы 1 из 4-х: 1 Физика низкотемпературной плазмы 117 ГК 2. Биофизика 113 ГК', \
        [('117', 'ГК'), ('113', 'ГК')] \
      ), ( \
        'Лин методы в р/т /Доц. Григорьев А. А. /117 ГК', \
        [('117', 'ГК')] \
      ), ( \
        'Теоретическая физика 202 НК, Б. Физ. , 123 ГК, 432 ГК, 521 ГК, 532 ГК, 507а ГК, 509 ГК, 511 ГК', \
        [('202', 'НК'), ('123', 'ГК'), ('432', 'ГК'), ('521', 'ГК'), ('532', 'ГК'), \
         ('507а', 'ГК'), ('509', 'ГК'), ('511', 'ГК'), ('Б. Физ.', None)] \
      ), ( \
        'Функциональный анализ ( 31б, 32а, 33, 34в, 36бв)/Доцент Боговский М. Е. / 430 ГК ' + \
        'Уравнения математической физики (31а, 32б, 34аб, 35, 36а) /Доцент Шаньков В. В. /Акт. зал', \
        [('430', 'ГК'), ('Акт. Зал', None)] \
      ), ( \
        'Физические основы фотоники и нанофотоники /Профессор Фомичёв А. А. / 113 ГК', \
        [('113', 'ГК')] \
      ), ( \
        'Вычислительная математика /Лобачев/ 202 НК', \
        [('202', 'НК')] \
      ), ( \
        'Сетевые технологии /Ст. преп. Подлесных / 113 ГК', \
        [('113', 'ГК')] \
      ), ( \
        'Основы физики конденсированного состояния /К. ф. -м. н. Куксин А. Ю/ 516а ГК -альт. курс', \
        [('516а', 'ГК')] \
      ), ( \
        'Теоретическая физика Б. Хим. , 430 ГК, 113 ГК', \
        [('430', 'ГК'), ('113', 'ГК'), ('Б. Хим.', None)] \
      ), ( \
        'Диф. ур-ния Б. Хим', \
        [('Б. Хим.', None)] \
      ), ( \
        'оодкдз/401кпм КПМ401 КПМ', \
        [('401', 'КПМ')] \
      ), ( \
        'Общеинженерная подготовка /Нечетная неделя/ 301ЛК', \
        [('301', 'ЛК')] \
      ), ( \
        'Теория вероятностей Чит. зал', \
        [('Чит. Зал', None)] \
      ), ( \
        'Теор. физика 511 Гк', \
        [('511', 'ГК')] \
      ), ( \
        '', \
        [] \
      ) \
    ]
  def runTest(self):
    for i in xrange(len(self.cases)):
      self.assertEqual(cell_parser.GetLocations(self.cases[i][0]), self.cases[i][1])

class TeachersTest(unittest.TestCase):
  def setUp(self):
    self.cases = [ \
      ( \
        'МСС /211 ГК , 532 ГК/', \
        [] \
      ), ( \
        'Теория игр и принятие решений / Доцент Меньшиков И. С. - для "кт" и "эк" - обязательно; для "мф" - а. к. -1 110 КПМ', \
        [('Меньшиков', 'И', 'С')] \
      ), ( \
        'Механика сплошных сред Проф. Жмур В. В. -211 ГК проф. Рыжак Е. И. - 532 ГК', \
        [('Жмур', 'В', 'В'), ('Рыжак', 'Е', 'И')] \
      ), ( \
        'Альтерн. курсы 1 из 4-х: 1 Физика низкотемпературной плазмы 117 ГК 2. Биофизика 113 ГК', \
        [] \
      ), ( \
        'Лин методы в р/т /Доц. Григорьев А. А. /117 ГК', \
        [('Григорьев', 'А', 'А')] \
      ), ( \
        'Теоретическая физика 202 НК, Б. Физ. , 123 ГК, 432 ГК, 521 ГК, 532 ГК, 507а ГК, 509 ГК, 511 ГК', \
        [] \
      ), ( \
        'Функциональный анализ ( 31б, 32а, 33, 34в, 36бв)/Доцент Боговский М. Е. / 430 ГК ' + \
        'Уравнения математической физики (31а, 32б, 34аб, 35, 36а) /Доцент Шаньков В. В. /Акт. зал', \
        [('Боговский', 'М', 'Е'), ('Шаньков', 'В', 'В')] \
      ), ( \
        'Физические основы фотоники и нанофотоники /Профессор Фомичёв А. А. / 113 ГК', \
        [('Фомичёв', 'А', 'А')] \
      ), ( \
        'Вычислительная математика /Лобачев/ 202 НК', \
        [('Лобачев', None, None)] \
      ), (\
        'Сетевые технологии /Ст. преп. Подлесных / 113 ГК', \
        [('Подлесных', None, None)] \
      ), ( \
        'Основы физики конденсированного состояния /К. ф. -м. н. Куксин А. Ю/ 516а ГК -альт. курс', \
        [('Куксин', 'А', 'Ю')] \
      ), ( \
        'Теоретическая физика Б. Хим. , 430 ГК, 113 ГК', \
        [] \
      ), ( \
        'Диф. ур-ния Б. Хим', \
        [] \
      ), ( \
        'оодкдз/401кпм КПМ401 КПМ', \
        [] \
      ), ( \
        'Общеинженерная подготовка /Нечетная неделя/ 301ЛК', \
        [] \
      ), ( \
        'МСС-Доц. Извеков-430 ГК, Доцент Березникова М. В. . -211 ГК; Проф. Рыжак Е. И. - 532 ГК', \
        [('Березникова', 'М', 'В'), ('Рыжак', 'Е', 'И'), ('Извеков', None, None)] \
      ), ( \
        '', \
        [] \
      ) \
    ]
  def runTest(self):
    for i in xrange(len(self.cases)):
      self.assertEqual(cell_parser.GetTeachers(self.cases[i][0]), self.cases[i][1])

class SubjectsTest(unittest.TestCase):
  def setUp(self):
    self.cases = [ \
      ( \
        'МСС /211 ГК , 532 ГК/', \
        ['Механика сплошных сред'] \
      ), ( \
        'Теория игр и принятие решений / Доцент Меньшиков И. С. - для "кт" и "эк" - обязательно; для "мф" - а. к. -1 110 КПМ', \
        ['Теория игр и принятие решений'] \
      ), ( \
        'Механика сплошных сред Проф. Жмур В. В. -211 ГК проф. Рыжак Е. И. - 532 ГК', \
        ['Механика сплошных сред'] \
      ), ( \
        'Альтерн. курсы 1 из 4-х: 1 Физика низкотемпературной плазмы 117 ГК 2. Биофизика 113 ГК', \
        ['Биофизика', 'Физика низкотемпературной плазмы'] \
      ), ( \
        'Лин методы в р/т /Доц. Григорьев А. А. /117 ГК', \
        ['Линейные методы в радиотехнике'] \
      ), ( \
        'Теоретическая физика 202 НК, Б. Физ. , 123 ГК, 432 ГК, 521 ГК, 532 ГК, 507а ГК, 509 ГК, 511 ГК', \
        ['Теоретическая физика'] \
      ), ( \
        'Функциональный анализ ( 31б, 32а, 33, 34в, 36бв)/Доцент Боговский М. Е. / 430 ГК ' + \
        'Уравнения математической физики (31а, 32б, 34аб, 35, 36а) /Доцент Шаньков В. В. /Акт. зал', \
        ['Уравнения математической физики', 'Функциональный анализ',] \
      ), ( \
        'Физические основы фотоники и нанофотоники /Профессор Фомичёв А. А. / 113 ГК', \
        ['Физические основы фотоники и нанофотоники'] \
      ), ( \
        'Вычислительная математика /Лобачев/ 202 НК', \
        ['Вычислительная математика'] \
      ), (\
        'Сетевые технологии /Ст. преп. Подлесных / 113 ГК', \
        ['Сетевые технологии'] \
      ), ( \
        'Основы физики конденсированного состояния /К. ф. -м. н. Куксин А. Ю/ 516а ГК -альт. курс', \
        ['Основы физики конденсированного состояния'] \
      ), ( \
        'Теоретическая физика Б. Хим. , 430 ГК, 113 ГК', \
        ['Теоретическая физика'] \
      ), ( \
        'Диф. ур-ния Б. Хим', \
        ['Дифференциальные уравнения'] \
      ), ( \
        'оодкдз/401кпм КПМ401 КПМ', \
        ['ООДКДЗ'] \
      ), ( \
        'Общеинженерная подготовка /Нечетная неделя/ 301ЛК', \
        ['Общеинженерная подготовка'] \
      ), ( \
        'Химия: лаб. практикум', \
        ['Химия: Лабораторный практикум'] \
      ), ( \
        '', \
        [] \
      ) \
    ]
  def runTest(self):
    for i in xrange(len(self.cases)):
      self.assertEqual(cell_parser.GetSubjects(self.cases[i][0]), self.cases[i][1])

if __name__ == '__main__':
   unittest.main()
