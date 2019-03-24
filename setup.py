#!/bin/python
#---------------------------------------------------------------------------------
#
#                    ,--.
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,
#                    | .-. '| .-. :| .-. ||  .--'|      \
#                    | `-' |\   --.' '-' '|  |   |  ||  |
#                     `---'  `----' `---' `--'   `--''--'
#
#         file: setup
#  description: This is the package file for the beorn_libs.
#
#       author: Peter Antoine
#         date: 20/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
#import version as version
from setuptools import setup, find_packages

# make this nasty hack a bit tidier and make it work properly
# from anywhere in the file system.
execfile("beorn_lib/version.py")

setup(name='BeornLib',
      version=__version__,
      description='Beorn Shared Functions Library',
      author=__author__,
      author_email=__email__,
      url=__url__,
      package_data={'': ['version.py']},
      packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
	  install_requires=['pycrypto', 'py-bcrypt']
     )

