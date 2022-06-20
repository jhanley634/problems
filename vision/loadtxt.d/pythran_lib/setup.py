#! /usr/bin/env python
from distutils.core import setup

try:
    from pythran.dist import PythranBuildExt, PythranExtension
    setup_args = {
        'cmdclass': {'build_ext': PythranBuildExt},
        'ext_modules': [PythranExtension('hello.hello', sources=['hello/hello.py'])],
    }
except ImportError:
    print('Not building Pythran extension')
    setup_args = {}

setup(name='hello',
      version='1.0',
      description='Yet another demo package',
      packages=['hello'],
      **setup_args)
