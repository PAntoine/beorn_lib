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
#    file: code_review
#    desc: This class holds the code reviews.
#
#  author: peter
#    date: 02/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

from base64 import b64encode, b64decode
from beorn_lib.nested_tree import NestedTreeNode
from change import Change
from comment import Comment

class CodeReview(NestedTreeNode):
	CODE_REVIEW_STATUS_OPEN			= 1
	CODE_REVIEW_STATUS_APPROVED		= 2
	CODE_REVIEW_STATUS_ABANDONED	= 3
	CODE_REVIEW_STATUS_MERGED		= 4

	CODE_REVIEW_VOTE_UP		= 1
	CODE_REVIEW_VOTE_DOWN	= 2

	global_review_id = 0

	def __getitem__(self, key):
		for item in self.getChildren():
			if type(key) == Change:
				if item.change_id == key.getID():
					return item
			elif item.change_id == key:
				return item

		raise KeyError("Does not exist")

	def __contains__(self, other):
		""" Contains

			Will return True if 'other' is the name of one of the children.
		"""
		for item in self.getChildren():
			if isinstance(other, NestedTreeNode):
				if item.getID() == other.getID():
					return True
			elif item.getID() == other:
				return True
		return False

	def __init__(self, review_id = None, author = None, date = None, is_local=False):
		self.is_local = is_local

		if review_id is None:
			review_id = str(CodeReview.global_review_id)
			CodeReview.global_review_id += 1
		else:
			CodeReview.global_review_id = review_id + 1

		super(CodeReview, self).__init__()

		self.review_id	= review_id
		self.author		= author
		if date is None:
			self.date = 0
		else:
			self.date = date

	def toString(self):
		return "review:" + str(self.review_id) + "," + str(self.author) + "," + str(self.date)

	def isLocal(self):
		return self.is_local

	def setLocal(self, local):
		self.is_local = local

	def getID(self):
		return self.review_id

	def getCurrentChange(self):
		(result, _, _) = self.getNextNode()
		return result

	def getTitle(self):
		result = 'No Title'

		if self.hasChild():
			(first_child, _, _) = self.getNextNode()
			result = first_child.getTitle()

		return result

	def getDescription(self):
		result = []

		if self.hasChild():
			(first_child, _, _) = self.getNextNode()
			result = first_child.getDescription()

		return result

	def getVotes(self):
		if self.hasChild():
			(first_child, _, _) = self.getNextNode()
			return first_child.getVotes()
		else:
			return []

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def isApproved(self):
		if self.hasChild():
			(first_child, _, _) = self.getNextNode()
			return first_child.isApproved()
		else:
			return False

	def getApprover(self):
		return self.approver

	def getNumComments(self):
		result = 0

		for item in self.getChildren():
			if type(item) == Comment:
				result += 1
			else:
				result += item.getNumComments()

		return result

	def addChange(self, change_list):
		new_change = Change(change_list)
		self.addChildNode(new_change, NestedTreeNode.INSERT_FRONT)
		return new_change

	def clearLocal(self):
		""" Clear Local

			If you have amended the coderievew (added a comment) or voted
		"""
		if self.colour == colour:
			return self

		else:
			current = self

			while current is not None and current.colour <= colour:
				if current.colour == colour:
					return current

				if current.next_node is not None and current.next_node.colour <= colour:
					current = current.next_node
				elif current.child_node is not None:
					# Ok, we know it's between us and the next node, look children.
					current = current.child_node
				else:
					# Ok, can't exist.
					return None

		return None

# vim: ts=4 sw=4 noexpandtab nocin ai
