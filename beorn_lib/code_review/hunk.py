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
#    file: hunk
#    desc: This is the individual hunks of the change.
#
#  author: peter
#    date: 04/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

from beorn_lib.nested_tree import NestedTreeNode
from collections import namedtuple as namedtuple

DummyHunk = namedtuple('DummyHunk', [ 'original_line', 'original_length', 'new_line', 'new_length', 'lines'])

class Hunk(NestedTreeNode):
	@classmethod
	def decode(cls, parent, decode_string, local):
		parts = decode_string.split(",")
		hunk = DummyHunk(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), parts[5].split('\x03'))
		new_hunk = Hunk(hunk, int(parts[0]))

		if type(parent) == Hunk:
			parent.getParent().addHunk(new_hunk)
		else:
			parent.addHunk(new_hunk)

		new_hunk.setLocal(local)

		return new_hunk

	def __getitem__(self, key):
		for item in self.getChildren():
			if isinstance(key, NestedTreeNode):
				if item.getID() == key.getID():
					return item
			elif item.getID() == key:
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

	def __init__(self, hunk, hunk_id, is_local=False):
		super(Hunk, self).__init__()

		self.is_local = is_local;

		self.original_line = hunk.original_line
		self.original_length = hunk.original_length
		self.new_line = hunk.new_line
		self.new_length = hunk.new_length

		self.hunk_id = hunk_id

		self.lines = hunk.lines

	def toString(self, summary=False):
		if summary:
			if (self.original_length + self.new_length) > 0:
				granularity = 20.0 / (self.original_length + self.new_length);
			else:
				granularity = 1

			removed = '-' * int(granularity * self.original_length)
			added = '+' * (20 - int(granularity * self.original_length))

			# If you have more that 10,000 lines in a file -- RE-WRITE NOW!!!
			return "line: {:5d} {}{}".format(self.original_line, added, removed)
		else:
			return "hunk:" + str(self.hunk_id) + "," + str(self.original_line) + "," + str(self.original_length) + "," + str(self.new_line) + "," + str(self.new_length) + "," + '\x03'.join(self.lines)

	def isLocal(self):
		return self.is_local

	def setLocal(self, local):
		self.is_local = local

	def getID(self):
		return self.hunk_id

	def getStart(self):
		return self.original_line

	def getChangeStart(self):
		return self.new_line

	def isLineInHunk(self, line):
		return self.new_line <= line and (self.new_line + self.new_length) >= line

	def getCommentForLine(self, line_no, pre_side):
		for item in self.getChildren():
			if item.isPreSide() == pre_side and item.getLine() == line_no:
				return item

		return None

	def getChange(self):
		left = []
		right = []

		for line in self.lines:
			if line[0] == '+':
				right.append(line[1:])
			elif line[0] == '-':
				left.append(line[1:])
			else:
				left.append(line[1:])
				right.append(line[1:])

		# Was the file deleted.
		if self.original_length == 0:
			left = []

		# is it a new file.
		if self.new_length == 0:
			right = []

		return (left, right)

	def getContents(self):
		return line

	def getNumComments(self):
		return self.getNumberChildren()

# vim: ts=4 sw=4 noexpandtab nocin ai
