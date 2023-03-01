#!/usr/bin/env python3
from os import chdir
from os import pardir
from os.path import abspath
from os.path import join
from os.path import normpath

from setuptools import setup


INSTALL_REQUIRES = ['centre-registry-app']
chdir(normpath(join(abspath(__file__), pardir)))
setup(
    name='centre_registry_config',
    use_scm_version={
        "root": "..",
        "fallback_version": "2.3.2.dev0"
    },
    setup_requires=['setuptools_scm'],
    packages=['centre_registry_project'],
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    license='GPLv3',
    description='CLARIN Centre Registry, a Django application. ',
    long_description='See README.md',
    url='https://trac.clarin.eu/wiki/Centre%20Registry',
    author=['Beatriz Sanchez Bribian', 'Sander Maijers', 'Michał Gawor', 'André Moreira'],
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
