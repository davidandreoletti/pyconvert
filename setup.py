#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'media.convert.application',
    version = '0.0.1dev',
    author = 'David Andreoletti',
    packages = find_packages(),
    description = 'Convert media files for storage into my own aperture libraries.',
)

print "packages==>";print find_packages()
