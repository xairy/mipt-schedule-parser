#!/usr/bin/env python
#coding: utf-8

from distutils.core import setup

setup(name='MIPT Schedule Parser',
    version='0.1.0',
    description='Parses standard mipt schedule xls file.',

    author='Andrey Konovalov',
    author_email='adech.fo@gmail.com',
    url='https://github.com/xairy/mipt-schedule-parser',

    license='LICENSE',
    long_description=open('README.md').read(),

    install_requires=[
        "xlrd >= 0.6.1",
        "regex >= 0.1.0",
    ],

    packages=['miptscheduleparser'],
    package_data={'miptscheduleparser': ['data/subjects', 'data/2013_fall/*', 'data/2014_spring/*']}
)
