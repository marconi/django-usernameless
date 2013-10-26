#!/usr/bin/env python

import os
import sys
import usernameless

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist register upload')
    sys.exit()

packages = ['usernameless']
requires = ['django-impersonate==0.8.0',
            'django-registration==1.0',
            'django-autoslug==1.7.1']

setup(
    name='django-usernameless',
    version=usernameless.__version__,
    packages=packages,
    description='Custom user without username for Django-1.5',
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Marconi Moreto',
    author_email='caketoad@gmail.com',
    url='https://github.com/marconi/django-usernameless',
    zip_safe=False,
    install_requires=requires,
)
