# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use boilerplate to start simple
# usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os
import sys
from setuptools import setup, find_packages


# Meta information
name = 'pygov-br'
project = 'pygov_br'
author = 'Matheus Fernandes'
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)


# Save version and author to __meta__.py
with open(os.path.join(dirname, 'src', project, '__meta__.py'), 'w') as F:
    F.write('__version__ = %r\n__author__ = %r\n' % (version, author))

INSTALL_DEPS = [
    'requests>=2.11.1',
    'beautifulsoup4',
    'click'
]

if sys.version_info < (2, 7):
    INSTALL_DEPS.append('importlib')

setup(
    # Basic info
    name=name,
    version=version,
    author=author,
    author_email='matheus.souza.fernandes@gmail.com',
    url='',
    description='A short description for your project.',
    long_description=open('README.rst').read(),

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=INSTALL_DEPS,
    extras_require={
        'dev': [
            'mock',
            'responses',
            'pytest',
            'pytest-cov',
            'coveralls',
            'flake8',
            'manuel',
        ],
    },

    # Scripts
    entry_points={
        'console_scripts': ['pygov-br = pygov_br.__main__:main'],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
