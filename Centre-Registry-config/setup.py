#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

__version__ = '2.1'  # TODO: update on release

from os import chdir as os_chdir
from os import pardir as os_pardir
import os.path
from setuptools import setup
from sys import version_info as sys__version_info

if sys__version_info < (3, 4):
    raise RuntimeError('ERROR: under Python version {0}.{1}, while version >= 3.4 required. '
                       .format(str(sys__version_info.major),
                               str(sys__version_info.minor)))

setup_requires = [] # ['wheel>=0.24']
install_requires = ['centre-registry-app>=2.1,<2.2']

os_chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os_pardir)))

setup(
    name='centre_registry_config',
    version=__version__,
    packages=['centre_registry_project'],
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    license='GPLv3',
    description='CLARIN Centre Registry, a Django application. ',
    long_description='See README.md',
    url='https://trac.clarin.eu/wiki/Centre%20Registry',
    author=['Beatriz Sanchez Bribian', 'Sander Maijers'],
    author_email=['centre-registry@clarin.eu'],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)