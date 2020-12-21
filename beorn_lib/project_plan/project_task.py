#!/bin/python
#---------------------------------------------------------------------------------
#                                                   
#                    ,--.                                 
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,  
#                    | .-. '| .-. :| .-. ||  .--'|      \ 
#                    | `-' |\   --.' '-' '|  |   |  ||  | 
#                     `---'  `----' `---' `--'   `--''--' 
#                                                    
#         file: project_task
#  description: This file holds the class for the project task.
#
#       author: Peter Antoine
#         date: 20/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

from beorn_lib.nested_tree import NestedTreeNode

class ProjectTask:
	""" Project Task

		This class holds the definition of the Project Task.
	"""

	def __init__(self, task_id, task_type, duration, status, name, description, follows_task):
		self.task_id		= int(task_id)
		self.task_type		= task_type
		self.duration		= int(duration)
		self.status			= status
		self.name			= name
		self.description	= description
		self.node			= NestedTreeNode(self)

		if follows_task is None:
			self.follows_task = 0
		else:
			self.follows_task = int(follows_task)

	def toFileString(self):
		ini_format = "task%d = %s,%d,%s,%s,%s,%d\n"
		return ini_format % (self.task_id, self.task_type, self.duration, self.status, self.name, self.description, self.follows_task)

	def getChildren(self):
		""" Get the child tasks of the current task.

			This function will return the list of children that belong
			to this task.
		"""
		return self.node.getChildren()

# vim: ts=4 sw=4 noexpandtab nocin ai
