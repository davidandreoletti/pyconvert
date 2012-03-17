#!/usr/bin/env python

pythonPackageName="pyconvert"
pythonPackageVersion="0.0.1"
pythonPackageFullName=pythonPackageName + " " + pythonPackageVersion

# Check minimun Python interpreter version required
import sys
if not hasattr(sys, "hexversion") or sys.hexversion < 0x020701f0:
    sys.stderr.write("Installation FAILED: " + pythonPackageFullName +
                     " requires Python 2.7.1 or better.\n")
    sys.exit(1)

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name=pythonPackageName,
    version=pythonPackageVersion,
    author='David Andreoletti',
    packages=find_packages(),
    description='Python application to convert files for storage into my own aperture libraries.',
)

print "packages==>" + str(find_packages())
