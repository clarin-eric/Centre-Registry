#!/usr/bin/env python3
from os import chdir
from os import pardir
from os.path import abspath
from os.path import join
from os.path import normpath

from setuptools import setup

__version__ = '2.2.0'

INSTALL_REQUIRES = ['Django==1.9.10', 'django-debug-toolbar==1.6']
TEST_REQUIRES = ['lxml==3.6.4', 'selenium==2.53.6']
chdir(normpath(join(abspath(__file__), pardir)))
setup(
    name='centre_registry_app',
    version=__version__,
    packages=['centre_registry'],
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    test_requires=TEST_REQUIRES,
    license='GPLv3',
    description='CLARIN Centre Registry, a Django application. ',
    long_description='See README.md',
    url='https://trac.clarin.eu/wiki/Centre%20Registry',
    author=['Beatriz Sanchez Bribian', 'Sander Maijers'],
    author_email=['centre-registry@clarin.eu'],
    zip_safe=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ])
