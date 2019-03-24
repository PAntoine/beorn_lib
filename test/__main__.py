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
import test.beorn_tests as beorn_tests

SUPPORTED_SCMS = ['git' ] #/*, 'hg']

SINGLE_TESTS = [#	beorn_tests.TestUser,
					beorn_tests.TestNotes,
					beorn_tests.TestProject,
					beorn_tests.TestProjectPlan,
					beorn_tests.TestTextDialog,
					beorn_tests.TestHTMLDialog,
					beorn_tests.TestTree,
					beorn_tests.TestNestedTree,
					beorn_tests.TestConfig,
					beorn_tests.TestSourceTree,
					beorn_tests.TestTimeKeeper
					]

SCM_TESTS = [ 	beorn_tests.TestCodeReview,
				beorn_tests.TestAmend,
				beorn_tests.TestSearch,
				beorn_tests.TestQuery
				]

def load_tests(selected_group = None, test_case = None):
	""" Load Tests

		This function will load the tests from the test module.
		It will add all the single tests to be run individually and
		for the tests that need to run on all the different supported
		scms it will then then add those for each supported SCM.
	"""
	suite = unittest.TestSuite()
	found = False

	# need to know where the test_data is
	test_data = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_data')

	# add all the tests that only run once
	for test_class in SINGLE_TESTS:
		if selected_group is None or test_class.__name__ == selected_group:
			tests = unittest.defaultTestLoader.getTestCaseNames(test_class)

			# now add the tests
			for test in tests:
				if test_case is None or test == test_case:
					suite.addTest(test_class(test, test_data))
					found = True

	for scm_type in SUPPORTED_SCMS:
		for test_class in SCM_TESTS:
			if selected_group is None or test_class.__name__ == selected_group:
				tests = unittest.defaultTestLoader.getTestCaseNames(test_class)

				# create the testing environment
				repo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data','test_scm', scm_type)

				# now add the tests
				for test in tests:
					if test_case is None or test == test_case:
						suite.addTest(test_class(test, scm_type, repo_dir, test_data))
						found = True

	if not found:
		return None
	else:
		return suite

if __name__ == '__main__':
	run_class = None
	test_case = None

	if len(sys.argv) > 1:
		run_class = sys.argv[1]

	if len(sys.argv) > 2:
		test_case = sys.argv[2]

	test_suite = load_tests(run_class, test_case)

	if test_suite is None:
		print "Error: No tests have been found."
	else:
		unittest.TextTestRunner().run(test_suite)

# vim: ts=4 sw=4 noexpandtab nocin ai
# vim: ts=4 sw=4 noexpandtab nocin ai
