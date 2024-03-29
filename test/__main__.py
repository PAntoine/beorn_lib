#!/usr/bin/env python3
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

#SUPPORTED_SCMS = ['Git', 'P4']
SUPPORTED_SCMS = ['Git']


def get_test_names(test_class, selected_group):
	tests = []

	if type(test_class) == type and (selected_group is None or test_class.__name__ == selected_group):
		if issubclass(test_class, unittest.TestCase):
			tests = unittest.defaultTestLoader.getTestCaseNames(test_class)

	return tests

def return_test_names(selected_group, tests_only, scm_only, scm_name):
	tests = []
	scm_results = []

	if not scm_only:
		for item_name in dir(beorn_tests):
			test_class = getattr(beorn_tests, item_name)
			values = get_test_names(test_class, selected_group)

			if len(values) > 0:
				tests.append((item_name, values))

	if not tests_only:
		for scm_type in SUPPORTED_SCMS:
			if scm_name is None or scm_type == scm_name:
				for item_name in dir(scm_tests):
					test_class = getattr(scm_tests, item_name)
					values = get_test_names(test_class, selected_group)

					if len(values) > 0:
						scm_results.append((item_name, values))

	return (tests, scm_results)

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
			tests = get_test_names(test_class, selected_group)

			# now add the tests
			for test in tests:
				if test_case is None or test == test_case:
					suite.addTest(test_class(test, test_data, temp_data))
					found = True
	else:
		print("SCM only, skipping other tests")

	if not tests_only:
		for scm_type in SUPPORTED_SCMS:
			if scm_name is None or scm_type == scm_name:
				for item_name in dir(scm_tests):
					test_class = getattr(scm_tests, item_name)
					tests = get_test_names(test_class, selected_group)

					if len(tests) > 0:
						# create the testing environment
						temp_data_root = os.path.join(os.path.abspath('.'), 'temp_data', 'test_scm')

						test_class.setParameters(temp_data_root, test_data, scm_type)

						# now add the tests
						for test in tests:
							if test_case is None or test == test_case:
								suite.addTest(test_class(test, scm_type, temp_data_root, test_data))
								found = True
	else:
		print("Tests only, skipping SCM tests")

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

	print_help = False
	list_available_tests = False

	if len(sys.argv) > 1:
		for item in sys.argv[1:]:
			if item.startswith('-s'):
				scm_only = True

				pos = item.find('=')
				if pos > -1:
					scm_type = item[pos+1:]
			elif item.startswith('-t'):
				tests_only = True

			elif item.startswith('-h'):
				print_help = True

			elif item.startswith('-l') or item.startswith('-?'):
				print_help = True
				list_available_tests = True

			elif run_class is None:
				run_class = item

			elif test_case is None:
				test_case = item

			else:
				print("bad parameters.")
				print_help = True

	if print_help:
		print("Usage: -s	- only run the SCM tests")
		print("Usage: -t	- only run the non-SCM tests")
		print("Usage: -h	- print the help.")
		print("Usage: -l	- print list of tests.")
		print("\n i.e. python test [options] [TestGroup] [TestCase]\n")

		if list_available_tests:
			test, scm_test = return_test_names(run_class, tests_only, scm_only, scm_type)

			if len(test) > 0:
				print()
				print("Tests:")
				for item in test:
					print("  Group: ", item[0])

					for testcase in item[1]:
						print("    TestCase: ", testcase)

			if len(scm_test) > 0:
				print()
				print("SCM Tests:")
				for item in scm_test:
					print("  Group: ", item[0])

					for testcase in item[1]:
						print("    TestCase: ", testcase)

	else:
		temp_data = os.path.join(os.path.abspath('.'), 'temp_data')

		if os.path.exists(temp_data):
			shutil.rmtree(temp_data, ignore_errors=True)

		os.mkdir(temp_data)

		test_suite = load_tests(run_class, test_case, tests_only, scm_only, scm_type)

		shutil.rmtree(temp_data)

		if test_suite is None:
			print("Error: No tests have been found.")
		else:
			test_result = unittest.TextTestRunner().run(test_suite)
			print(test_result.errors)

			print("tests ran:", test_result.testsRun)
			print("tests failed:", test_result.failures)

# vim: ts=4 sw=4 noexpandtab nocin ai
