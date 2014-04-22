#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='mipt-schedule-parser',
    version='0.1.0',
    description='Parses standard mipt schedule xls file.',

    author='Andrey Konovalov',
    author_email='adech.fo@gmail.com',
    url='https://github.com/xairy/mipt-schedule-parser',

    license='MIT license, see LICENSE',
    long_description=open('README.md').read(),

    install_requires=[
        "xlrd >= 0.6.1",
        "regex >= 0.1.0",
    ],

    packages=find_packages(),
    package_data={'miptscheduleparser': ['data/subjects', 'data/2013_fall/*', 'data/2014_spring/*']},
    include_package_data=True,

    test_suite = 'miptscheduleparser.test.suite'
)
