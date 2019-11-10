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
#    file: review_engine
#    desc: This is the base class for the supporte review engines.
#
#  author: peter
#    date: 29/09/2019
#---------------------------------------------------------------------------------
#                     Copyright (c) 2019 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import getpass
import platform
from code_review import CodeReview
from beorn_lib.nested_tree import NestedTree

registered_engines = {}


def registerEngine(engine_class):
	if engine_class.__name__ not in registered_engines:
		registered_engines[engine_class.__name__] = engine_class


def getSupportedNames():
	return registered_engines.keys()


def getSupportedEngines():
	result = []
	for item in registered_engines:
		result.append(registered_engines[item])
	return result


class ReviewEngine(NestedTree):
	@classmethod
	def getDefaultConfiguration(cls):
		return {}

	@classmethod
	def getDialogLayout(cls):
		return {}

	def __init__(self, configuration, password_function=None):
		super(ReviewEngine, self).__init__()

		self.is_dirty = False

	def __getitem__(self, key):
		for item in self:
			if key == item.getID():
				return item

		raise KeyError("Does not exist")

	def __contains__(self, other):
		""" Contains

			Will return True if 'other' is the name of one of the children.
		"""
		for item in self:
			if other == item.getID() or type(other) == CodeReview and other.getID() == item.getID():
				return True

		return False

	def setDirty(self):
		self.is_dirty = True

	def clearDirty(self):
		self.isDirty = False

	def isDirty(self):
		return self.is_dirty

	def pollServer(self):
		return False

	def getName(self):
		return ""

	def getUser(self):
		return getpass.getuser()

	def getCurrentMachine(self):
		return platform.node()

	def getNumReviews(self):
		return 0

	def update(self):
		return False

	def load(self):
		return True

	def save(self):
		return True

	def addReview(self, change_list):
		return None

	def createReview(self):
		return None

# vim: ts=4 sw=4 noexpandtab nocin ai
