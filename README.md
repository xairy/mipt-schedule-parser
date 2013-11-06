MIPT Schedule parser
====================

The schedule parser consists of two independent scripts: one for converting
a schedule xls file into a simple plain text format and the other one is for
extracting subject's name, professor's name, building and room number from
a raw description string.

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

    Subgroup a, Subclass 1
    Subgroup b, Subclass 1
    Subgroup a, Subclass 2
    Subgroup b, Subclass 2

If the both group halves have the same class in each half of a class hour,
then all 4 values will be the same.

These values are actually the values of the according excel cells.

So, basically, the script prints the schedule as the follows:

    for each Group:
      print Group.Number()
      for each Weekday:
        for each ClassHour:
          Class = Schedule.Class(Group, Weekday, ClassHour)
          print Class.Sub(a, 1).Value()
          print Class.Sub(b, 1).Value()
          print Class.Sub(a, 2).Value()
          print Class.Sub(b, 2).Value()

Usage:

    $ python parser.py 2013_fall/1kurs.xls
    011
    ...
    Теорет.физика 509 ГК 
    Теорет.физика 509 ГК 
    Теорет.физика 509 ГК 
    Теорет.физика 509 ГК
    ...
    034
    ...
    Физ.основы ДЗ 430 ГК
    Физическая механика 113 ГК
    Физ.основы ДЗ 430 ГК
    Физическая механика 113 ГК
    Физ.основы ДЗ 430 ГК
    Физ.мех. 514 ГК
    Физ.основы ДЗ 430 ГК
    Физ.мех. 514 ГК
    ...


### Cell parser script

The script works in a manner similar to addr2line.
For each line read from the input it will print 3 lines:

1. $-separated list of all the subjects extracted
2. $-separated list of all the professors' names extracted


3. $-separated list of all the buldings and room numbers extracted

If you are running this script manually you may want to press Ctrl + D to flush
the input you entered so far.

Usage:

    $ ./cell_parser
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
