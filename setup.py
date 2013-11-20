#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def _load_requires_from_file(filepath):
    return [pkg_name.rstrip('\r\n') for pkg_name in open(filepath).readlines()]


def _install_requires():
    return _load_requires_from_file('requirements.txt')


def _tests_require():
    return _load_requires_from_file('test-requirements.txt')


def _packages():
    return find_packages(
        exclude=[
            '*.tests',
            '*.tests.*',
            'tests.*',
            'tests'
        ]
    )

if __name__ == '__main__':
    setup(
        name='rabbitracer',
        version='0.1.1',
        description='RabbitMQ Firehose Dump Script',
        author='momijiame',
        author_email='amedama.ginmokusei@gmail.com',
        url='https://github.com/momijiame/rabbitracer',
        classifiers=[
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: Apache Software License',
            'Intended Audience :: Developers',
            'Natural Language :: Japanese',
            'Operating System :: POSIX'
        ],
        packages=_packages(),
        install_requires=_install_requires(),
        tests_require=_tests_require(),
        test_suite='nose.collector',
        entry_points="""
        [console_scripts]
        rabbitracer = rabbitracer:main
        """,
    )
