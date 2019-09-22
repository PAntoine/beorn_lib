#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#
#                    ,--.
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,
#                    | .-. '| .-. :| .-. ||  .--'|      \
#                    | `-' |\   --.' '-' '|  |   |  ||  |
#                     `---'  `----' `---' `--'   `--''--'
#
#    file: __main__
#    desc: This is the test runner for the beorn_lib tests.
#
#  author: peter
#    date: 21/10/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import sys
import shutil
import unittest

# the test needs to use relative paths - so the tests can run without installation
TEST_PATH = os.path.dirname(os.path.abspath(__file__))
(ROOT_PATH, _) = os.path.split(TEST_PATH)
(SUB_ROOT_PATH, _) = os.path.split(ROOT_PATH)
sys.path.append(ROOT_PATH)
sys.path.insert(1, SUB_ROOT_PATH)
sys.path.insert(1, TEST_PATH)
sys.path.insert(1, os.path.join(SUB_ROOT_PATH, 'beorn_lib'))

# import the tests
#import test.beorn_tests as beorn_tests
import beorn_tests
import scm_tests

SUPPORTED_SCMS = ['Git', 'P4']

def load_tests(	selected_group = None,
				test_case = None,
				tests_only = None,
				scm_only = None,
				scm_name = None):
	""" Load Tests

		This function will load the tests from the test module.
		It will add all the single tests to be run individually and
		for the tests that need to run on all the different supported
		scms it will then then add those for each supported SCM.
	"""
	suite = unittest.TestSuite()
	found = False

	# need to know where the test_data is
	temp_data = os.path.join(os.path.abspath('.'), 'temp_data')
	test_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')

	# add all the tests that only run once
	if not scm_only:
		for item_name in dir(beorn_tests):
			test_class = getattr(beorn_tests, item_name)
			if type(test_class) == type and (selected_group is None or item_name == selected_group):
				if issubclass(test_class, unittest.TestCase):
					tests = unittest.defaultTestLoader.getTestCaseNames(test_class)

					# now add the tests
					for test in tests:
						if test_case is None or test == test_case:
							suite.addTest(test_class(test, test_data, temp_data))
							found = True

	if not tests_only:
		for scm_type in SUPPORTED_SCMS:
			if scm_type == scm_name:
				for item_name in dir(scm_tests):
					test_class = getattr(scm_tests, item_name)
					if type(test_class) == type and (selected_group is None or item_name == selected_group):
						if issubclass(test_class, unittest.TestCase):
							tests = unittest.defaultTestLoader.getTestCaseNames(test_class)

							# create the testing environmen
							temp_data_root = os.path.join(os.path.abspath('.'), 'temp_data', 'test_scm')

							test_class.setParameters(temp_data_root, test_data, scm_type)

							# now add the tests
							for test in tests:
								if test_case is None or test == test_case:
									suite.addTest(test_class(test, scm_type, temp_data_root, test_data))
									found = True

	if not found:
		return None
	else:
		return suite

if __name__ == '__main__':
	run_class = None
	test_case = None
	failed = False
	scm_only = False
	tests_only = False
	scm_type =  None

	if len(sys.argv) > 1:
		for item in sys.argv[1:]:
			if item.startswith('-s'):
				scm_only = True

				pos = item.find('=')
				if pos > -1:
					scm_type = item[pos+1:]
			elif item.startswith('-t'):
				tests_only = True

			elif run_class is None:
				run_class = item

			elif test_case is None:
				test_case = item

			else:
				print "bad parameters."
				failed = True

	if not failed:
		temp_data = os.path.join(os.path.abspath('.'), 'temp_data')

		if os.path.exists(temp_data):
			shutil.rmtree(temp_data, ignore_errors=True)

		os.mkdir(temp_data)

		test_suite = load_tests(run_class, test_case, tests_only, scm_only, scm_type)

		shutil.rmtree(temp_data)

		if test_suite is None:
			print "Error: No tests have been found."
		else:
			test_result = unittest.TextTestRunner().run(test_suite)
			print test_result.errors

			print "tests ran:", test_result.testsRun
			print "tests failed:", test_result.failures

# vim: ts=4 sw=4 noexpandtab nocin ai
