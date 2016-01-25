#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='korbit',
    version='0.1',
    description='korbit API wrapper for Python',
    url='http://github.com/Hoonjin/korbit-python/',
    author='Daniel Ji',
    author_email='bwjhj1030@gmail.com',
    license='MIT',
    install_requires=['requests'],
    packages=['korbit'],
)
