#!/usr/bin/python
#coding: utf-8

from __future__ import unicode_literals

import fileinput
import regex
import sets
import sys
import urllib2

__author__ = "Andrey Konovalov"
__copyright__ = "Copyright (C) 2014 Andrey Konovalov"
__license__ = "MIT"
__version__ = "0.1"

teacher_entry_re = regex.compile(
  '\<a href="(?P<link>[^"]+)" ' +
  'title="(?P<name>[^ ]+ [^ ]+ [^ ]+)">[^\<]+</a>   ' +
  '</div> <div class=\'searchresult\'></div>'
)

surname = 'Иванов'
initials = ['', '']


def FindTeacher(surname, initials):
  body = urllib2.urlopen(
    ('http://wikimipt.org/index.php?search=' + surname).encode('utf-8')
  ).read().decode('utf-8')

  results = []
  while True:
    m = teacher_entry_re.search(body)
    if m == None:
      break
    body = body[:m.start('name')] + body[m.end('name'):]
    results.append((m.group('name'), m.group('link')))

  links = []
  for result in results:
    name = result[0].split()
    if len(name) == 3 and name[0] == surname:
      if name[1][0] == initials[0] and name[2][0] == initials[1]:
        links.append('http://wikimipt.org' + result[1])
      if initials[0] == '' and initials[1] == '':
        links.append('http://wikimipt.org' + result[1])
  return links

if __name__ == '__main__':
  for name in fileinput.input():
    name = name.decode('utf-8').rstrip().split()
    surname = name[0]
    initials = ['', ''] if len(name) == 1 else [name[1], name[2]]
    links = FindTeacher(surname, initials)
    print ' '.join(links).encode('utf-8')
