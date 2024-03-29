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
#    file: test_timekeeper
#    desc: Tests for TimeKeeper
#
#  author: peter
#    date: 24/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import glob
import time
import shutil
import unittest
import threading
from beorn_lib.timekeeper import TimeKeeper

#---------------------------------------------------------------------------------
# Test Class
#---------------------------------------------------------------------------------

class TestTimeKeeper(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None, temp_data = None):
		self.test_data = test_data
		self.temp_data = temp_data
		self.timekeeper_dir = os.path.join(temp_data, 'timekeeper')

		# initialise the test framework
		super(TestTimeKeeper, self).__init__(testname)

	def setUp(self):
		# generate platform non-specific
		if os.path.isdir(self.timekeeper_dir):
			# tidy up the test
			filelist = glob.glob(os.path.join(self.timekeeper_dir,'*'))
			for dfile in filelist:
				os.remove(dfile)
		else:
			os.makedirs(self.timekeeper_dir)

	def tearDown(self):
		shutil.rmtree(self.timekeeper_dir)

	def all_nodes_function(self, last_visited_node, node, value, levels, direction, parameter):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = [' '*levels + type(node).__name__]
		else:
			value.append(' '*levels + type(node).__name__)

		return (node, value, False)

	def readerFunction(self, last_visited_node, node, value, level, direction, parameter):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = []

		if node.__class__.__name__ == "Job":
			value.append('  ' + node.toString() + ' ' + node.getTotalString())

		return (node, value, False)

	def test_timekeeper(self):
		""" Basic TimeKeeper test.

			This test adds the basic items to the timekeeper objects.
		"""
		# start the creation tests
		test_timekeeper = TimeKeeper(self.timekeeper_dir)
		self.assertIsNotNone(test_timekeeper)

	def test_timekeeperImport(self):
		""" Import some timekeeper files (generated from the old system).

			This test makes sure that the load and save works.
		"""
		for name in ['devhome_pantoine.tmk', 'homedesk_pantoine.tmk', 'pantoine-904HD_pantoine.tmk']:
			# start the creation tests
			filename = os.path.join(self.test_data, name)
			test_timekeeper = TimeKeeper(filename=filename)
			self.assertTrue(test_timekeeper.load(), "Load file failed: " + filename)

			content = test_timekeeper.walkTree(self.readerFunction)
			self.assertNotEqual(0, len(content))

	def test_timekeeperSave(self):
		""" Import some timekeeper files then save them and then check that they match.  """
		for name in ['devhome_pantoine.tmk', 'homedesk_pantoine.tmk', 'pantoine-904HD_pantoine.tmk']:
			# start the creation tests
			filename = os.path.join(self.test_data, name)
			test_timekeeper = TimeKeeper(filename=filename)
			self.assertTrue(test_timekeeper.load(), "Load file failed: " + filename)

			content = test_timekeeper.walkTree(self.readerFunction)
			self.assertNotEqual(0, len(content))

			# hack the file name - not a good test - but is good enough
			test_timekeeper.filename = os.path.join(self.temp_data, name)
			self.assertTrue(test_timekeeper.save(), "Save file failed: " + filename)


# vim: ts=4 sw=4 noexpandtab nocin ai
