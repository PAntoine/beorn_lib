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
#    file: project_plan_tests
#    desc: These are the tests for the project plan.
#
#  author: Peter Antoine
#    date: 05/01/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import string
import unittest
import beorn_lib.errors
from beorn_lib.project_plan import ProjectPlan

class TestProjectPlan(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None, temp_data = None):
		self.test_data = test_data
		self.temp_data = temp_data

		# initialise the test framework
		super(TestProjectPlan, self).__init__(testname)

	#--------------------------------------------------------------------------------
	# Helper Functions.
	#--------------------------------------------------------------------------------
	def collect_function(self,last_visited_node,node,value,levels,direction):
		""" This is a test function that is used to collect the data
			from the nodes that it has visited. It will return the
			list of nodes that it encounters.
		"""
		if not node.is_sub_node:
			if value is None:
				value = [node.payload]
			else:
				value.append(node.payload)

		return (node,value,False)

	def dump_endtime_function(self,last_visted_node,node,value,levels,direction):
		""" This is a test function that is used to return the calculated values
			from the nodes that it has visited.
		"""

		if not node.is_sub_node:
			if value is None:
				value = [(node.payload.task_id,node.payload.start,node.payload.end)]
			else:
				value.append((node.payload.task_id,node.payload.start,node.payload.end))

		return (node,value,False)

	def render_tasks(self,task,level):
		fields = [' ' for x in range(level)]
		fields.append(task[0].payload.task_id.__str__())

		if len(task[2]) > 0:
			for item in task[2]:
				if type(item) == tuple:
					self.render_tasks(item,level+1)
				else:
					for x in item:
						self.render_tasks(x,level+1)

	#--------------------------------------------------------------------------------
	# Test Functions.
	#--------------------------------------------------------------------------------
	def test_DateCalcFunction(self):
		""" Date Calculation Function

			This tests that the endtime calculation function works. It will de a series
			of tests that tests that the 1/4 rolling value calculates to the correct time
			for each of the week lengths. Only going to bother testing at one day length,
			as if that works it should all work.
		"""
		self.project_plan = ProjectPlan()

		# test different working week lengths
		for week_length in range(1,7):
			self.project_plan.days_per_week = week_length

			# start day of week for job
			for start_day_of_week in range(0,7):
				self.project_plan.first_day_of_week = start_day_of_week

				weekend = [0,0,0,0,0,0,0]
				day_to_week = [0,0,0,0,0,0,0]

				for day in range(7):
					if day < self.project_plan.first_day_of_week or (start_day_of_week + week_length) <= day:
						weekend[day] = 1
						day_to_week[day] = 6 - day

				# number of weeks
				for week_number in range(0,3):
					task_days = week_number * week_length

					start_time = self.project_plan.start_time + (start_day_of_week * 60 * 60 * 24)

					# days in the week
					for day_number in range(0,week_length):
						duration = ((week_number * week_length) + day_number) * self.project_plan.minutes_per_day
						real_time = start_time + (((week_number * 7) + day_number) * (60 * 60 * 24))
						calced_from_duration_time = self.project_plan.calculateEndTimes(start_time,duration)

						if calced_from_duration_time != real_time:
							self.assertTrue(calced_from_duration_time != real_time)


	def test_CreateProjectPlan(self):
		""" Create Project Plan

			This test will create a project plan.
		"""
		self.project_plan = ProjectPlan()

		# negative test
		self.assertFalse(self.project_plan.createProject('test create project','xxxxx/tests_create.bpf'))

		# positive test
		self.assertTrue(self.project_plan.createProject('test create project', os.path.join(self.test_data, 'tests_create.bpf')))

	def test_LoadProjectPlan(self):
		""" Load Project Plan

			This test will create a project plan.
		"""
		self.project_plan = ProjectPlan()

		# negative test
		self.assertFalse(self.project_plan.loadProject('test create project','xxxxx/tests_load.bpf'));

		# positive test
		self.assertTrue(self.project_plan.loadProject('test create project', os.path.join(self.test_data, 'tests_load.bpf')))

	def test_PopulateNewProjectPlan(self):
		""" PopulateNewProjectPlan

			This test will create a project plan.

                                 {4} -> [ 5] -> [ 6]                                     {14} -> [15] -> [16]
			   [1]-> [2] -> :3:---+               +----:3:-> [10] -> [11] -> [12] -> :13:-+                +-:13:-> [20] -> [21]
			    			     {7} -> [ 8] -> [ 9]                                     {17} -> [18] -> [19]


		"""
		self.project_plan = ProjectPlan()

		self.assertTrue(self.project_plan.createProject('test create project',os.path.join(self.test_data, 'tests_populate.bpf')))

		# now add the nodes
		# Task(task_id,task_type,duration,status,name,description):
		self.project_plan.AddTask(1,'task',self.project_plan.minutes_per_day,'created','task 1',"a simple task",None)
		self.project_plan.AddTask(2,'task',self.project_plan.minutes_per_day,'created','task 2',"a simple task",1)
		self.project_plan.AddTask(3,'task',self.project_plan.minutes_per_day,'created','task 3',"a simple task",2)
		self.project_plan.AddTask(10,'task',self.project_plan.minutes_per_day,'created','task 10',"a simple task",3)
		self.project_plan.AddTask(11,'task',self.project_plan.minutes_per_day,'created','task 11',"a simple task",10)
		self.project_plan.AddTask(12,'task',self.project_plan.minutes_per_day,'created','task 12',"a simple task",11)
		self.project_plan.AddTask(13,'task',self.project_plan.minutes_per_day,'created','task 13',"a simple task",12)
		self.project_plan.AddTask(20,'task',self.project_plan.minutes_per_day,'created','task 20',"a simple task",13)
		self.project_plan.AddTask(21,'task',self.project_plan.minutes_per_day,'created','task 21',"a simple task",20)

		# 1st children of 3
		self.project_plan.AddTask(4,'sub_task',self.project_plan.minutes_per_day,'created','task 3',"a simple task",3)
		self.project_plan.AddTask(5,'task',self.project_plan.minutes_per_day,'created','task 4',"a simple task",4)
		self.project_plan.AddTask(6,'task',self.project_plan.minutes_per_day,'created','task 5',"a simple task",5)

		# 2nd Children of 3
		self.project_plan.AddTask(7,'sub_task',self.project_plan.minutes_per_day,'created','task 7',"a simple task",3)
		self.project_plan.AddTask(8,'task',self.project_plan.minutes_per_day,'created','task 8',"a simple task",7)
		self.project_plan.AddTask(9,'task',self.project_plan.minutes_per_day,'created','task 9',"a simple task",8)

		# 1st children of 13
		self.project_plan.AddTask(14,'sub_task',self.project_plan.minutes_per_day,'created','task 14',"a simple task",13)
		self.project_plan.AddTask(15,'task',self.project_plan.minutes_per_day,'created','task 15',"a simple task",14)
		self.project_plan.AddTask(16,'task',self.project_plan.minutes_per_day,'created','task 16',"a simple task",15)

		# 2nd Children of 13
		self.project_plan.AddTask(17,'sub_task',self.project_plan.minutes_per_day,'created','task 17',"a simple task",13)
		self.project_plan.AddTask(18,'task',self.project_plan.minutes_per_day,'created','task 18',"a simple task",17)
		self.project_plan.AddTask(19,'task',self.project_plan.minutes_per_day,'created','task 19',"a simple task",18)

		self.project_plan.saveProject()

	def test_LoadAndReDateTree(self):
		""" Load And Re-Date Tree

			This test will load a project plan. This is the same plan as populate. Just loaded from an old one
			so the dates are known.

                                 {4} -> [ 5] -> [ 6]                                     {14} -> [15] -> [16]
			   [1]-> [2] -> :3:---+               +----:3:-> [10] -> [11] -> [12] -> :13:-+                +-:13:-> [20] -> [21]
			    			     {7} -> [ 8] -> [ 9]                                     {17} -> [18] -> [19]


		"""
		self.project_plan = ProjectPlan()

		self.assertTrue(self.project_plan.loadProject('test create project', os.path.join(self.test_data, 'tests_walk.bpf')))

		value = self.project_plan.plan_tree.walkTree(self.collect_function)

		# calculate the times for the items and check that they are valid
		self.project_plan.reDateTree()
		value = self.project_plan.plan_tree.walkTree(self.dump_endtime_function)

		# for the task added above, this is the correct layout of times.
		task_order_times = [(1, 1376006400, 1376092800), (2, 1376265600, 1376352000), (3, 1376352000, 1376611200),
							(4, 1376352000, 1376438400), (5, 1376438400, 1376524800), (6, 1376524800, 1376611200),
							(7, 1376352000, 1376438400), (8, 1376438400, 1376524800), (9, 1376524800, 1376611200),
							(10, 1376611200, 1376697600), (11, 1376870400, 1376956800), (12, 1376956800, 1377043200),
							(13, 1377043200, 1377475200), (14, 1377043200, 1377129600), (15, 1377129600, 1377216000),
							(16, 1377216000, 1377302400), (17, 1377043200, 1377129600), (18, 1377129600, 1377216000),
							(19, 1377216000, 1377302400), (20, 1377475200, 1377561600), (21, 1377561600, 1377648000)]

		self.assertTrue(value == task_order_times)


	def test_ListTree(self):
		self.project_plan = ProjectPlan()

		self.assertTrue(self.project_plan.loadProject('test create project', os.path.join(self.test_data, 'tests_walk.bpf')))
		project_list = self.project_plan.getProjectList(self.project_plan.plan_tree)

		for item in project_list:

			if type(item) == tuple:
				self.render_tasks(item,0)
			else:
				for x in item:
					self.render_tasks(x,0)


# vim: ts=4 sw=4 noexpandtab nocin ai
