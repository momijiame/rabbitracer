#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def _install_requires():
    return ['furl', 'kombu']


def _tests_require():
    return [
        'nose',
        'mox',
    ]

if __name__ == '__main__':
    setup(name='rabbitracer',
          version='0.1',
          description='RabbitMQ Firehose Dump Script',
          author='momijiame',
          url='https://github.com/momijiame/rabbitracer',
          packages=find_packages(exclude=['test']),
          install_requires=_install_requires(),
          test_suite='nose.collector',
          tests_require=_tests_require(),
          entry_points="""
          [console_scripts]
          rabbitracer = rabbitracer:main
          """,)
