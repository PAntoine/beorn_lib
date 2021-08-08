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
#    file: change_file
#    desc: This is an individual file from a change_set.
#
#  author: peter
#    date: 04/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

from .hunk import Hunk
from .comment import Comment
from beorn_lib.nested_tree import NestedTreeNode
from collections import namedtuple as namedtuple

DummyChangeItem	= namedtuple('DummyChangeItem', ['new_file', 'change_list'])

class ChangeFile(NestedTreeNode):
	@classmethod
	def decode(cls, previous, decode_string, local):
		parts = decode_string.split(',')
		new_item = DummyChangeItem(parts[0], [])
		new_change = ChangeFile(new_item)

		new_change.setLocal(local)

		if previous.__class__.__name__ == "Change":
			previous.addChildNode(new_change)
		else:
			curr = previous.getParent()

			while curr.__class__.__name__ != "Change":
				curr = curr.getParent()

			curr.addChildNode(new_change)

		return new_change

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

	def __init__(self, change_item, is_local=False):
		super(ChangeFile, self).__init__()
		self.is_local = is_local
		self.name = change_item.new_file

		for index, hunk in enumerate(change_item.change_list):
			new_hunk = Hunk(hunk, index, is_local)
			self.addChildNode(new_hunk)

	def getID(self):
		return self.name

	def isLocal(self):
		return self.is_local

	def setLocal(self, local):
		self.is_local = local

	def getHunkByID(self, hunk_id):
		result = None

		for item in self.getChildren():
			if item.getID() == hunk_id:
				result = item
				break

		return result

	def addHunk(self, hunk):
		self.addChildNode(hunk)

	def toString(self):
		return "file:" + self.name

	def getName(self):
		return self.name

	def getNumComments(self):
		result = 0

		for item in self.getChildren():
			if type(item) == Comment:
				result += 1
			else:
				result += item.getNumComments()

		return result

# vim: ts=4 sw=4 noexpandtab nocin ai
