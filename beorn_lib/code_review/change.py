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
#    file: change
#    desc: This is a code review change.
#
#  author: peter
#    date: 02/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

from base64 import b64encode, b64decode
from comment import Comment
from change_file import ChangeFile
from beorn_lib.nested_tree import NestedTreeNode
from collections import namedtuple as namedtuple

DummyChange = namedtuple('DummyChange', ['commit_id', 'timestamp', 'author', 'description', 'changes'])

class Change(NestedTreeNode):
	@classmethod
	def decode(cls, previous, decode_string, local):
		parts = decode_string.split(',')

		# TODO: fix the vote loading.
		#votes = parts[6]

		new_change = DummyChange(parts[0], int(parts[3]), parts[4], parts[5].split('\x03'), [])
		change_item = Change(new_change, {}, parts[2], parts[1])

		change_item.setLocal(local)

		if previous.__class__.__name__ == "CodeReview":
			previous.addChildNode(change_item)
		else:
			curr = previous.getParent()

			while curr.__class__.__name__ != "CodeReview":
				curr = curr.getParent()

			curr.addChildNode(change_item)

		return change_item

	def __getitem__(self, key):
		for item in self.getChildren():
			if item.getID() == key:
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

	def __init__(self, change=None, votes=None, state = None, approver = None, is_local=False):
		super(Change, self).__init__(change, None)

		self.is_local = is_local

		if approver is None:
			self.approver = False
		else:
			self.approver = approver

		if state is None:
			self.approval_state = 1		# nasty hack to stop circular imports
		else:
			self.approval_state = state

		if change is None:
			self.change_id = None
			self.timestamp = 0
			self.author = "<no-one>"
			self.description = "none"
		else:
			self.change_id = change.commit_id
			self.timestamp = change.timestamp
			self.author = change.author
			self.description = change.description

			for item in change.changes:
				new_file = ChangeFile(item, is_local)
				self.addChildNode(new_file)

		if votes is not None:
			self.votes = votes
		else:
			self.votes = {}

	def getID(self):
		return self.change_id

	def toString(self):
		vote_string = "{"

		for vote in self.votes:
			vote_string += vote + ":" + str(votes[vote])

		vote_string += "}"

		return "change:" + self.change_id + "," + str(self.approver) + "," + str(self.approval_state) + "," + str(self.timestamp) + "," + self.author + "," + '\x03'.join(self.description) + "," + vote_string

	def isLocal(self):
		return self.is_local

	def setLocal(self, local):
		self.is_local = local

	def vote(self, user, vote):
		self.votes[user] = vote

	def getVotes(self):
		return self.votes

	def getState(self):
		return self.approval_state

	def setState(self, user, state):
		if state != self.approval_state:
			self.approval_state = state
			self.approver = user

	def isApproved(self):
		return self.approval_state == CODE_REVIEW_STATUS_APPROVED

	def getTitle(self):
		return self.description[0]

	def getDescription(self):
		return self.description[1:]

	def getNumComments(self):
		result = 0

		for item in self.getChildren():
			if type(item) == Comment:
				result += 1
			else:
				result += item.getNumComments()

		return result

# vim: ts=4 sw=4 noexpandtab nocin ai
