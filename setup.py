#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def _read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


DEPENDENCIES = [
    'py',
    'pytest',
    ]

DESCRIPTION = ("py.test plugin to create a 'tmpdir' containing predefined "
	       "files/directories.")
LONG_DESCRIPTION = _read('README.rst') + '\n\n' + _read('CHANGELOG.rst')

setup(
    name='pytest-datafiles',
    version='1.0',
    py_modules=['pytest_datafiles'],
    url='https://github.com/omarkohl/pytest-datafiles',
    license='MIT',
    install_requires=DEPENDENCIES,
    author='Omar Kohl',
    author_email='omarkohl@gmail.com',
    maintainer='Omar Kohl',
    maintainer_email='omarkohl@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    entry_points={
        'pytest11': ['pytest_datafiles = pytest_datafiles'],
	},
    keywords='pytest datafiles tmpdir',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
        ]
    )
