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
from beorn_lib import TimeKeeper, TASK_TIMER_ONESHOT, TASK_TIMER_REPEAT, TASK_TIMER_UNTIL, TASK_TIMER_EXPIRED

#---------------------------------------------------------------------------------
# Test Class
#---------------------------------------------------------------------------------

class TestTimeKeeper(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None):
		self.test_data = test_data
		self.timekeeper_dir = os.path.join(test_data, 'timekeeper')

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
			if node.__class__.__name__ == "Task":
				value.append(' '*levels + type(node).__name__ + ":" + str(node.getTime()))
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
			value.append('  ' + node.toString())

		return (node, value, False)

	def test_timekeeper(self):
		""" Basic TimeKeeper test.

			This test adds the basic items to the timekeeper objects.
		"""
		# start the creation tests
		test_timekeeper = TimeKeeper(self.timekeeper_dir)

	def test_timekeeperImport(self):
		""" Import some timekeeper files (generated from the old system).

			This test makes sure that the load and save works.
		"""
		for name in ['devhome_pantoine.tmk', 'homedesk_pantoine.tmk', 'pantoine-904HD_pantoine.tmk']:
			# start the creation tests
			filename = os.path.join(self.test_data, name)
			test_timekeeper = TimeKeeper(filename=filename)
			test_timekeeper.load()

			content = test_timekeeper.walkTree(self.readerFunction)

			test_timekeeper.getNextTaskTimeout()

	def handler_function(self, timer_event, signal_event, task):
		if signal_event:
			timer_event.set()

	def test_timekeeperTimers(self):
		""" test that timers work. """
		test_timekeeper = TimeKeeper(self.timekeeper_dir)

		# create two projects
		project_1 = test_timekeeper.addProject("project1")
		project_2 = test_timekeeper.addProject("project2")
		self.assertEqual(2, len(test_timekeeper.getChildren()))

		# test that get timeout does not break without jobs
		(item, _) = test_timekeeper.getNextTaskTimeout()
		self.assertIsNone(item)

		# add some jobs
		job_1_1 = project_1.addJob("job_1_1")
		job_1_2 = project_1.addJob("job_1_2")
		job_1_3 = project_1.addJob("job_1_3")
		self.assertEqual(3, len(project_1.getChildren()))

		job_2_1 = project_2.addJob("job_2_1")
		job_2_2 = project_2.addJob("job_2_2")
		self.assertEqual(2, len(project_2.getChildren()))

		# now add some tasks.
		base_test_time = int(time.time())

		task_1_2_1 = job_1_2.addTask('task_1_2_1', base_test_time + 10, 0)
		task_1_2_2 = job_1_2.addTask('task_1_2_2', base_test_time + 1, 0)
		task_1_2_3 = job_1_2.addTask('task_1_2_3', base_test_time + 3, 0)

		task_2_2_1 = job_1_2.addTask('task_2_2_1', base_test_time + 10, 0)
		task_2_2_2 = job_1_2.addTask('task_2_2_2', base_test_time + 1, 0)

		# test without setting a timeout
		(item, _) = test_timekeeper.getNextTaskTimeout()
		self.assertIsNone(item)

		# add some timeouts -- negative tests.
		self.assertFalse(task_1_2_2.setTimer(base_test_time - 10, 5, TASK_TIMER_ONESHOT))
		self.assertFalse(task_1_2_2.setTimer(base_test_time + 10, -1, TASK_TIMER_ONESHOT))
		self.assertFalse(task_1_2_2.setTimer(base_test_time + 10, -1, 0))
		self.assertFalse(task_1_2_2.setTimer(base_test_time + 10, -1, 50))
		(item, _) = test_timekeeper.getNextTaskTimeout()
		self.assertIsNone(item, "There was an invalid task set")

		# positive tests - in one job.
		self.assertTrue(task_1_2_2.setTimer(base_test_time + 15, 0, TASK_TIMER_ONESHOT))
		(item_1, time_out_1) = test_timekeeper.getNextTaskTimeout()
		self.assertIsNotNone(item_1, "There should be at least one timer set")

		self.assertTrue(task_1_2_3.setTimer(base_test_time + 10, 0, TASK_TIMER_ONESHOT))
		(item_2, time_out_2) = test_timekeeper.getNextTaskTimeout()
		self.assertIsNotNone(item_2, "There should be at least one timer set")

		self.assertNotEqual(item_1, item_2)
		diff = time_out_1 - time_out_2

		# to allow for clock rollover it should be at lest 4.
		self.assertGreaterEqual(diff, 4)
		self.assertGreaterEqual(diff, 0)

		# positive test with multiple tasks in multiple job
		self.assertTrue(task_2_2_1.setTimer(base_test_time + 5, 0, TASK_TIMER_ONESHOT))
		(item_3, time_out_3) = test_timekeeper.getNextTaskTimeout()
		self.assertNotEqual(item_3, item_2)

		self.assertTrue(task_2_2_2.setTimer(base_test_time + 6, 0, TASK_TIMER_ONESHOT))
		(item_4, time_out_4) = test_timekeeper.getNextTaskTimeout()
		self.assertEqual(item_3, item_4)

		# test the callback function
		event = threading.Event()

		timeout_function = lambda item : self.handler_function(event, True, item)
		test_timekeeper.enableTaskTimeOutCallback(timeout_function)
		event.wait(30)
		test_timekeeper.disableTaskTimeOut()

		# second
		event.clear()
		timeout_function = lambda item : self.handler_function(event, False, item)
		test_timekeeper.enableTaskTimeOutCallback(timeout_function)
		event.wait(20)
		test_timekeeper.disableTaskTimeOut()

		# now do a save
		list_1 = test_timekeeper.walkTree(self.all_nodes_function)
		test_timekeeper.save()

		# now do a load
		test_timekeeper_2 = TimeKeeper(self.timekeeper_dir)
		test_timekeeper_2.load()
		list_2 = test_timekeeper_2.walkTree(self.all_nodes_function)

		self.assertEqual(len(list_1), len(list_2))

# vim: ts=4 sw=4 noexpandtab nocin ai
