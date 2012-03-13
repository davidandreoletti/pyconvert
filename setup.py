#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='pyconvert',
    version='0.0.1dev',
    author='David Andreoletti',
    packages=find_packages(),
    description='Python application to convert files for storage into my own aperture libraries.',
)

print "packages==>" + str(find_packages())
