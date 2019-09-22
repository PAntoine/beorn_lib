#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#    file: test_amend
#    desc: This test case builds a repository for the given type in a known layout
#          this is used to test that the supported scm type works.
#
#  author: Peter Antoine
#    date: 04/12/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Import the external modules.
#---------------------------------------------------------------------------------
import os
import unittest
from test.utils.repo_builder import buildRepo

#---------------------------------------------------------------------------------
# Test Sequences.
#---------------------------------------------------------------------------------
class TestAmend(unittest.TestCase):
	def __init__(self, testname = 'runTest',  scm_type = None, scm_dir = None, test_data = None):
		self.scm_type = scm_type
		self.repo_dir = scm_dir

		# initialise the test framework
		super(TestAmend, self).__init__(testname)

	def test_buildRepo(self):
		""" Test Build SCM

			This test case will build the scm for the given parameters.
			It is the base test for the query tests as this will create a
			known a predicable SCM that can be queried and the code tested
			against.
		"""
		buildRepo(self)

if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 noexpandtab nocin ai
