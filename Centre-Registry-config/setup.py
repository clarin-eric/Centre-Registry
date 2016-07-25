#!/usr/bin/env python3
from os import chdir
from os import pardir
from os.path import abspath
from os.path import join
from os.path import normpath

from setuptools import setup

__version__ = '2.1'  # TODO: update on release
SETUP_REQUIRES = []  # ['wheel>=0.24']
INSTALL_REQUIRES = ['centre-registry-app>=2.1,<2.2']

chdir(normpath(join(abspath(__file__), pardir)))

setup(name='centre_registry_config',
      version=__version__,
      packages=['centre_registry_project'],
      include_package_data=True,
      install_requires=INSTALL_REQUIRES,
      setup_requires=SETUP_REQUIRES,
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
      ], )
