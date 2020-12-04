#!/bin/python
#---------------------------------------------------------------------------------
#
#                    ,--.
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,
#                    | .-. '| .-. :| .-. ||  .--'|      \
#                    | `-' |\   --.' '-' '|  |   |  ||  |
#                     `---'  `----' `---' `--'   `--''--'
#
#         file: project_plan
#  description: This file holds the classes that make up the project plan.
#
#       author: Peter Antoine
#         date: 20/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------
import os
import time
import string
from beorn_lib.nested_tree import NestedTree
from project_task import ProjectTask as ProjectTask

class ProjectPlan:

	# file states
	OPEN_READING_STATE		= 1
	LOAD_PROJECT_STATE		= 2
	LOAD_TASK_STATE			= 3

	""" Project Plan Class

		This class controls the project plan files.
	"""
	def __init__(self):
		self.name				= 'Project'
		self.filename			= None
		self.start_time			= int((time.mktime(time.gmtime()) / (60 * 60 * 24))) * (60 * 60 * 24)	# now
		self.days_per_week 		= 5									# 5 days
		self.minutes_per_day	= 450								# 7.5 hours
		self.first_day_of_week	= 0									# Monday
		self.last_task_id		= 0									# task_id's start at 1
		self.tasks				= {}								# dictionary of tasks

		self.plan_tree			= NestedTree()						# Create the node tree

		self.calcuateTheWeek()

		self.initialised		= False								# project plan state

	def calcuateTheWeek(self):
		""" Calculate the Week.

			This function adjusts the week arrays that are used to help with correcting the time.
		"""
		# create the week structures
		self.day_of_week		= [0,0,0,0,0,0,0]
		self.days_to_week		= [0,0,0,0,0,0,0]
		self.weekend			= [0,0,0,0,0,0,0]

		for index in range(7):
			self.day_of_week[index] = ((index + 7) - self.first_day_of_week) % 7

			if self.day_of_week[index] >= self.days_per_week:
				self.day_of_week[index] = 0
				self.days_to_week[index] = (7 - index + self.first_day_of_week) % 7
				self.weekend[index] = 1

	def calculate_dates_function(self,last_visted_node,node,value,levels,direction,parameter):
		""" This is a function that is used to calculate the start and end times of the
			items in the tree.
		"""
		if direction == NestedTree.DIRECTION_DOWN and not node.is_sub_node:
			prev_payload = node.getPrevPayload()

			if prev_payload is None:
				node.payload.start = self.calculateStartTime(self.start_time)
				node.payload.end   = self.calculateEndTimes(node.payload.start,node.payload.duration)
			else:
				node.payload.start = self.calculateStartTime(prev_payload.start)
				node.payload.end   = self.calculateEndTimes(node.payload.start,node.payload.duration)

		elif direction == NestedTree.DIRECTION_NEXT:
			prev_payload = node.getPrevPayload()
			node.payload.start = self.calculateStartTime(prev_payload.end)
			node.payload.end   = self.calculateEndTimes(node.payload.start,node.payload.duration)

		elif direction == NestedTree.DIRECTION_UP:
			prev_payload = node.getPrevPayload()

			# set the previous end
			if prev_payload.end < last_visted_node.payload.end:
				prev_payload.end = self.calculateStartTime(last_visted_node.payload.end)

			if not node.is_sub_node:
				# now set the current nodes start and end (and the previous end)
				# have stepped up a level
				node.payload.start = self.calculateStartTime(last_visted_node.payload.end)
				node.payload.end   = self.calculateEndTimes(node.payload.start,node.payload.duration)

		return (node,1,False)

	def createProject(self,project_name,project_file):
		""" Create Project File.

			This function will create new project file. It will write the default
			settings to the file.
		"""
		if self.initialised:
			result = False

		elif project_name == None or project_name == '':
			result = False

		elif project_file == None or project_file == '':
			result = False
		else:
			self.name     = project_name
			self.filename = project_file

			result = self.saveProject()

		self.initialised = result

		return result

	def reDateTree(self):
		""" Re-Calculate The Task Dates

			This function will re-calculate the dates for the items in the tree.
			This function should be called after any task (or group of tasks) have
			the duration amended, or a task has been added or removed.
		"""
		# set the start and endtimes of the tasks
		value = self.plan_tree.walkTree(self.calculate_dates_function)

	def loadProject(self,project_name,project_file):
		""" Load the Project Plan

			loadProject(<project_name>,<filename>) -> Boolean

			This function will load the project plan into the class. If the file
			does not exist then it will create an empty project plan.

			This function can only called once and any subsequent calls will fail.
		"""
		if self.initialised:
			result = False

		elif project_name == None or project_name == '':
			result = False

		elif project_file == None or project_file == '':
			result = False
		else:
			self.name     = project_name
			self.filename = project_file

			try:
				# now open the project file
				proj_file = open(self.filename,'r')

				state = ProjectPlan.OPEN_READING_STATE
				result = True

				for line in proj_file:
					if line[0:1] == '[':
						# It's a section header, is it correct
						if line[1:-2] == "project":
							if state != ProjectPlan.OPEN_READING_STATE:
								self.error_string = "bad file format - [project] found in wrong place"
								result = False
							else:
								state = ProjectPlan.LOAD_PROJECT_STATE

						elif line[1:-2] == "tasks":
							if state != ProjectPlan.LOAD_PROJECT_STATE:
								self.error_string = "bad file format - [tasks] found in wrong place"
								result = False
							else:
								state = ProjectPlan.LOAD_TASK_STATE

						else:
							self.error_string = "bad file format - unknown [%s] found in project file" % (line[1:-2])
							result = False

					else:
						if state == ProjectPlan.LOAD_PROJECT_STATE:
							parts = line.partition(" = ")

							if parts[0] == 'name':
								self.name = parts[2]

							elif parts[0] == 'starttime':
								self.start_time = int(parts[2])

							elif parts[0] == 'daysperweek':
								self.days_per_week = int(parts[2])

							elif parts[0] == 'minutesperday':
								self.minutes_per_day = int(parts[2])

							elif parts[0] == 'firstdayofweek':
								self.first_day_of_week = int(parts[2])

						elif state == ProjectPlan.LOAD_TASK_STATE:
							parts = line.partition(" = ")
							t_bits = parts[2].rstrip('\n').split(',')

							if len(t_bits) == 6:
								result = self.AddTask(int(parts[0][4:]),t_bits[0],t_bits[1],t_bits[2],t_bits[3],t_bits[4],int(t_bits[5]))
							else:
								result = False
								break

				# now update the week values
				self.calcuateTheWeek()

				# now calculate the start/end times
				self.reDateTree()

			except IOError:
				result = False

			self.initialised = result
			return result


	def AddTask(self,task_id,task_type,duration,status,name,description,follows_task):
		""" Add Task

			This function will add a task to the project plan.
			If the job number is None, then the function will create a new job and add it into the part of the
			tree specified by the parameters.
		"""
		result = False

		# Use the given Id or add a new one.
		if task_id is None:
			self.last_task_id = self.last_task_id + 1
			task_id = self.last_task_id
		else:
			task_id = task_id

			if task_id > self.last_task_id:
				self.last_task_id = task_id

		if not self.tasks.has_key(task_id):
			self.tasks[task_id] = ProjectTask(task_id,task_type,duration,status,name,description,follows_task)

			if follows_task == 0 or follows_task is None:
				self.plan_tree.addChildNode(self.tasks[task_id].node)

			elif task_type == 'task':
				self.tasks[follows_task].node.addNodeAfter(self.tasks[task_id].node)

			elif task_type == 'sub_task':
				self.tasks[follows_task].node.addSubTreeNode(self.tasks[task_id].node)

			result = True

		return result

	def calculateEndTimes(self,start_time,duration):
		""" Calculate End Time.

			This function takes a task and calculates it's endtime from the duration. It will
			take into account the weekend and day lengths of the project to calculate this
			value.
		"""
		# how many weeks does the task take.
		weeks = (duration / self.minutes_per_day) / self.days_per_week
		remain_days = (duration / self.minutes_per_day) - (weeks * self.days_per_week)
		remains = duration - (((weeks * self.days_per_week) + remain_days) * self.minutes_per_day)

		# calculate end time
		end_time  = start_time + (((((weeks * 7) + remain_days) * (60 * 24)) + remains) * 60)

		return end_time

	def calculateStartTime(self,start_time):
		""" Calculate Start Time.

			This function will take in a start time and adjust it to fit the working week. If
			the start time falls outside of the working day, or falls onto the weekend then the
			date will be moved onto the next working day.
		"""
		remains_of_the_day = start_time % (60 * 60 * 24)
		days = remains_of_the_day / (self.minutes_per_day * 60)

		# did the day rollover?
		start_time = start_time + (days * 60 * 60 * 24)  - (days * self.minutes_per_day * 60)

		# in the weekend?
		weekend_adjustment = self.days_to_week[time.gmtime(start_time).tm_wday] * (60 * 60 * 24)
		start_time = start_time + weekend_adjustment

		return start_time

	def saveProject(self):
		""" This function saves the current project.

			This function saves the project header, then dumps all the tasks in the
			list and there connections.
		"""
		try:
			proj_file = open(self.filename,'w')

			# write the header
			header = []
			header.append('[project]\n')

			ini_format = "%s = %s\n"

			header.append(ini_format % ('name',self.name))
			header.append(ini_format % ('starttime',self.start_time))
			header.append(ini_format % ('daysperweek',self.days_per_week))
			header.append(ini_format % ('minutesperday',self.minutes_per_day))
			header.append(ini_format % ('firstdayofweek',self.first_day_of_week))
			header.append('[tasks]\n')

			# write the header
			proj_file.writelines(header)

			for task in self.tasks:
				proj_file.write(self.tasks[task].toFileString())

			# write the footer and close the file
			proj_file.close()
			result = True

		except IOError:
			result = False

		return result

	def getProjectList(self,node):
		""" This function will generate a list of the project tasks.

			If the project tasks has sub-tasks then these will be listed as sub-lists.
		"""

		listing = []

		for item in node.getChildren():
			if item.hasChild():
				children = item.getChildren()
				item_list = []

				for c_list in children:
					sub_list = []

					if type(c_list) == list:
						for child in c_list:
							l_list = child.getChildren()
							sub_list.append((child,0,l_list))
					else:
						sub_list.append((c_list,0,c_list.getChildren()))

					item_list.append(sub_list)

				listing.append((item,0,item_list))

			else:
				listing.append((item,0,[]))

		return listing

# vim: ts=4 sw=4 noexpandtab nocin ai

