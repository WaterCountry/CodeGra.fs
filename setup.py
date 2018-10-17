#!/usr/bin/env python3

import sys

from setuptools import setup

import codegra_fs

version = '.'.join(map(str, codegra_fs.__version__))

if sys.version_info < (3, 5):
    print('Sorry only python 3.5 and up is supported', file=sys.stderr)
    sys.exit(1)

setup(
    name='CodeGra.fs',
    author='The CodeGrade team',
    author_email='info@codegra.de',
    version=version,
    description='File-system for CodeGrade instances',
    install_requires=['requests>=2.18.4', 'fusepy>3.0.0'],
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=['codegra_fs'],
    entry_points={
        'console_scripts':
            [
                'cgfs = codegra_fs.cgfs:main',
                'cgapi-consumer = codegra_fs.api_consumer:main'
            ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
    ],
)
