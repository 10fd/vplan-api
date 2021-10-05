#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='vplan-api',
	version='main',
	# Modules to import from other scripts:
	packages=find_packages(),
	# Executables
	scripts=["index.py"],
	)
