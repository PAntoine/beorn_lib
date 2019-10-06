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
#    file: code_reviews
#    desc: This is the wrapper class that handles the file management staff.
#
#  author: peter
#    date: 06/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import getpass
import platform
import beorn_lib
from base64 import b64encode, b64decode
from change import Change
from beorn_lib.nested_tree import NestedTreeNode
from code_review import CodeReview

class CodeReviews(NestedTreeNode):
	def __init__(self, root=None):
		super(CodeReviews, self).__init__()

		self.current_user		= getpass.getuser()
		self.current_machine	= platform.node()
		self.current_id			= self.current_user + '@' + self.current_machine
		self.colour = -1
		self.root = root

	def __getitem__(self, key):
		for item in self.getChildren():
			if type(key) == str or type(other) == unicode:
				if item.__class__.__name__ == key:
					return item

			elif isinstance(item, key):
				return item

		raise KeyError("Does not exist")

	def __contains__(self, other):
		""" Contains

			Will return True if 'other' is the name of one of the children.
		"""
		for item in self.getChildren():
			if type(other) == str or type(other) == unicode:
				if item.__class__.__name__ == other:
					return True

			elif isinstance(item, other):
				return True

		return False

	def getUser(self):
		return self.current_user

	def getNumComments(self):
		result = 0

		for item in self.getChildren():
			result += item.getNumComments()

		return result

	def addReviewEngine(self, name, configuration):
		if hasattr(beorn_lib.code_review, name):
			engine = getattr(beorn_lib.code_review, name)
			self.addChildNode(engine(self.root, configuration))

	def load(self):
		for item in self.getChildren():
			item.load()

	def save(self):
		for item in self.getChildren():
			item.save()

	def findHunk(self, review_id, change_id, name, hunk_id):
		result = None

		for engine in self:
			if review_id in engine:
				review = engine[review_id]

				if change_id in review:
					change = review[change_id]

					if name in change:
						change_file = change[name]

						if hunk_id in change_file:
							result = change_file[hunk_id]
		return result

	def findChangeFile(self, review_id, change_id, name):
		result = None

		for engine in self:
			if review_id in engine:
				review = engine[review_id]

				if change_id in review:
					change = review[change_id]

					if name in change[name]:
						result = change[name]

		return result

	def findChange(self, review_id, change_id):
		result = None

		for engine in self:
			if review_id in engine:
				review = engine[review_id]

				if change_id in review:
					result = review[change_id]

		return result

# vim: ts=4 sw=4 noexpandtab nocin ai
