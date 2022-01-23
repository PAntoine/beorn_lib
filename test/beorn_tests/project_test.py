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
#    file: project_test
#    desc: This test tests the project object.
#
#  author: Peter Antoine
#    date: 05/01/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import unittest
import beorn_lib.errors as errors
from beorn_lib.project import Project

class TestProject(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None, temp_data = None):
		self.test_data = test_data
		self.temp_data = temp_data

		# initialise the test framework
		super(TestProject, self).__init__(testname)

	def test_Project(self):
		""" Test the Project Class Works

			This test simply tests that the project works and can be loaded.
		"""
		project = Project()
		self.assertNotEqual(OK,project.isValid())
		self.assertEqual([],project.export())

		# set up the project manually
		project.name			= 'test project'
		project.description		= 'This is a multiline test descriptrion\nthis is to test the thing works with\nmutlline chars'
		project.start_date		= 1378571841
		project.release			= 'ssh://user@example/example.git'
		project.owner			= 'test_user'
		project.current_user	= project.owner
		project.users			= [project.owner]

		status = project.isValid()
		self.assertEqual(OK, status, errors.errors[status])

	def test_ProjectInitialise(self):
		"""  Project Initialise

			This test simply tests that the project initialise works.
		"""
		# set up the project manually
		project = Project()

		project.name			= 'test project'
		project.description		= 'This is a multiline test descriptrion\nthis is to test the thing works with\nmutlline chars'
		project.start_date		= 1378571841
		project.release			= 'ssh://user@example/example.git'
		project.owner			= 'test_user'
		project.current_user	= project.owner
		project.users			= [project.owner]

		# test data to load project
		test_data =	[	'name = dGVzdCBwcm9qZWN0\n',
						'description = VGhpcyBpcyBhIG11bHRpbGluZSB0ZXN0IGRlc2NyaXB0cmlvbgp0aGlzIGlzIHRvIHRlc3QgdGhlIHRoaW5nIHdvcmtzIHdpdGgKbXV0bGxpbmUgY2hhcnM=\n',
						'start_date = MTM3ODU3MTg0MQ==\n',
						'release = c3NoOi8vdXNlckBleGFtcGxlL2V4YW1wbGUuZ2l0\n',
						'owner = dGVzdF91c2Vy\n',
						'users = dGVzdF8xLHRlc3RfMg==\n']

		project_2 = Project()
		self.assertEqual(OK,project_2.initialise(test_data))

		# the two projects data should match
		self.assertEqual(project.name,project_2.name)
		self.assertEqual(project.description,project_2.description)
		self.assertEqual(project.start_date,project_2.start_date)
		self.assertEqual(project.release,project_2.release)
		self.assertEqual(project.owner,project_2.owner)

		# more test data to load project - without newlines
		test_data_1 = [	'name = dGVzdCBwcm9qZWN0',
						'description = VGhpcyBpcyBhIG11bHRpbGluZSB0ZXN0IGRlc2NyaXB0cmlvbgp0aGlzIGlzIHRvIHRlc3QgdGhlIHRoaW5nIHdvcmtzIHdpdGgKbXV0bGxpbmUgY2hhcnM=',
						'start_date = MTM3ODU3MTg0MQ==',
						'release = c3NoOi8vdXNlckBleGFtcGxlL2V4YW1wbGUuZ2l0',
						'owner = dGVzdF91c2Vy',
						'users = dGVzdF8xLHRlc3RfMg==\n']

		project_3 = Project()
		self.assertEqual(OK,project_3.initialise(test_data_1))

		# the two projects data should match
		self.assertEqual(project.name,project_3.name)
		self.assertEqual(project.description,project_3.description)
		self.assertEqual(project.start_date,project_3.start_date)
		self.assertEqual(project.release,project_3.release)
		self.assertEqual(project.owner,project_3.owner)

		# should fail to write as no project file given
		self.assertNotEqual(OK,project_2.save())

	def test_ProjectSaveAndLoad(self):
		"""  Project Save And Load

			This test simply tests that the project save and load works.
		"""
		# test data to load project
		test_data =	[	'name = dGVzdCBwcm9qZWN0\n',
						'description = VGhpcyBpcyBhIG11bHRpbGluZSB0ZXN0IGRlc2NyaXB0cmlvbgp0aGlzIGlzIHRvIHRlc3QgdGhlIHRoaW5nIHdvcmtzIHdpdGgKbXV0bGxpbmUgY2hhcnM=\n',
						'start_date = MTM3ODU3MTg0MQ==\n',
						'release = c3NoOi8vdXNlckBleGFtcGxlL2V4YW1wbGUuZ2l0\n',
						'owner = dGVzdF91c2Vy\n',
						'users = dGVzdF8xLHRlc3RfMg==\n']

		project = Project()
		self.assertEqual(OK,project.initialise(test_data))

		# now save the project
		test_filename = os.path.join(self.temp_data,'save_project.pf')
		self.assertEqual(OK,project.save(test_filename))

		# load the same project back in
		project_1 = Project()
		self.assertEqual(OK,project_1.load(test_filename))
		self.assertEqual(OK,project_1.isValid())
		self.assertEqual(project.name,project_1.name)
		self.assertEqual(project.description,project_1.description)
		self.assertEqual(project.start_date,project_1.start_date)
		self.assertEqual(project.release,project_1.release)
		self.assertEqual(project.owner,project_1.owner)

		# new test load the project
		project_2 = Project()
		test_filename = os.path.join(self.test_data,'load_project.pf')
		self.assertEqual(OK,project_2.load(test_filename))
		self.assertEqual(OK,project_2.isValid())
		self.assertEqual(project.name,project_2.name)
		self.assertEqual(project.description,project_2.description)
		self.assertEqual(project.start_date,project_2.start_date)
		self.assertEqual(project.release,project_2.release)
		self.assertEqual(project.owner,project_2.owner)


# vim: ts=4 sw=4 noexpandtab nocin ai
