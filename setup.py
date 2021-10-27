#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='vplan-api',
	version='main',
	# Modules to import from other scripts:
	packages=find_packages(),
	# Executables
	scripts=[ "scraper.py", ],
	)
