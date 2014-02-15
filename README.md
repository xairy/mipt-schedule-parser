MIPT Schedule Parser
====================

The schedule parser consists of two independent scripts: one for converting
a schedule xls file into a simple plain text format and the other one is for
extracting subject's name, professor's name, building' names and room number
from a raw description string. For convenience there is also a third script
that does both those things simultaneously.

### Prerequisites

To run the parser scripts you need python 2.7, python-xlrd, python-regex.

Ubuntu / Linux Mint:

    sudo apt-get install python-xlrd, python-regex

### Schedule parser script

This script converts the schedule and prints it in the following format:

    FirstGroup().Number()
    Class(FirstGroup, Monday, 09.00 - 10.25).Description()
    ...
    Class(FirstGroup, Monday, 18.30 - 19.50).Description()
    ...
    ...
    Class(FirstGroup, Saturday, 09.00 - 10.25).Description()
    ...
    Class(FirstGroup, Saturday, 18.30 - 19.50).Description()
    SecondGroup().Number()
    Class(SecondGroup, Monday, 09.00 - 10.25).Description()
    ...
    ...
    Class(SecondGroup, Saturday, 18.30 - 19.50).Description()
    ...

Since each class can last for an noninteger number of class hours (e.g. 1.5)
and sometimes one half of an academic group has one class and the other half
has another, each class is described with 4 values.

    |---------------|-------------------------------------------------|
    |               |                       073                       |
    |---------------|-------------------------------------------------|
    |               | Subgroup a, Subclass 1 | Subgroup b, Subclass 1 |
    | 12.20 - 13.45 |------------------------|------------------------|
    |               | Subgroup a, Subclass 2 | Subgroup b, Subclass 2 |
    |---------------|-------------------------------------------------|

These 4 values are printed each on a separate line in the following order:

    Class(Subgroup a, Subclass 1).Description()
    Class(Subgroup b, Subclass 1).Description()
    Class(Subgroup a, Subclass 2).Description()
    Class(Subgroup b, Subclass 2).Description()

If the both group halves have the same class in each half of a class hour,
then all 4 values will be the same.

Each of these 4 values consists of the color of the according excel cell and
its value separated by the tab character.
  
Colors are encoded as numbers, where
green (empty) is encoded as 0,
blue (seminars) - as 1,
pink (lectures) - as 2,
yellow (PE, foreign languages, etc.) - as 3.

So, basically, the script prints the schedule as follows:

    for each Group:
      print Group.Number()
      for each Weekday:
        for each ClassHour:
          Class = Schedule.Class(Group, Weekday, ClassHour)
          print Class.Sub(a, 1).Color() + \t + Class.Sub(a, 1).Value()
          print Class.Sub(b, 1).Color() + \t + Class.Sub(a, 1).Value()
          print Class.Sub(a, 2).Color() + \t + Class.Sub(a, 1).Value()
          print Class.Sub(b, 2).Color() + \t + Class.Sub(a, 1).Value()

Usage:

    $ python schedule_parser.py 2013_fall/4kurs.xls
    011
    ...
    1    Теорет.физика 509 ГК 
    1    Теорет.физика 509 ГК 
    1    Теорет.физика 509 ГК 
    1    Теорет.физика 509 ГК
    ...
    034
    ...
    2    Физ.основы ДЗ 430 ГК
    2    Физическая механика 113 ГК
    2    Физ.основы ДЗ 430 ГК
    2    Физическая механика 113 ГК
    1    Физ.основы ДЗ 430 ГК
    1    Физ.мех. 514 ГК
    1    Физ.основы ДЗ 430 ГК
    1    Физ.мех. 514 ГК
    ...


### Cell parser script

The script works in a manner similar to addr2line.
For each line read from the input it will print 3 lines:

    $-separated list of all the subjects extracted
    $-separated list of all the professors' names extracted
    $-separated list of all the buldings and room numbers extracted

If you are running this script manually you may want to press Ctrl + D to flush
the input you entered so far.

Usage:

    $ python cell_parser.py
    Лин методы в р/т /Доц. Григорьев А. А. /117 ГК
    <Ctrl + D>
    Линейные методы в радиотехнике
    117 ГК
    Григорьев А. А.
    Альтерн. курсы 1 из 4-х: 1 Физика низкотемпературной плазмы 117 ГК 2. Биофизика 113 ГК
    <Ctrl + D>
    Физика низкотемпературной плазмы$Биофизика
    117 ГК$113 ГК
    
    <Ctrl + D>

### Full parser script

This script combines the two previous ones and prints the lists of subjects,
professors and rooms after each of the 4 lines that describe a class.

Usage:

    $ ./full_parser.py 2014_spring/1.xls
    ...
    2    Линейная алгебра / Доцент Чубаров И.А./   202 НК
    Линейная алгебра
    202 НК
    Чубаров И. А.
    2    Линейная алгебра / Доцент Чубаров И.А./   202 НК
    Линейная алгебра
    202 НК
    Чубаров И. А.
    2    Линейная алгебра / Доцент Чубаров И.А./   202 НК
    Линейная алгебра
    202 НК
    Чубаров И. А.
    2    Линейная алгебра / Доцент Чубаров И.А./   202 НК
    Линейная алгебра
    202 НК
    Чубаров И. А.
    ...
