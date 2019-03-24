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
#    file: comment
#    desc: Code review comment.
#
#  author: peter
#    date: 04/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

from beorn_lib.nested_tree import NestedTreeNode

class Comment(NestedTreeNode):
	last_comment_id = 1

	@classmethod
	def getNextID(cls):
		cls.last_comment_id += 1
		return cls.last_comment_id

	@classmethod
	def decode(cls, parent, decode_string, local):
		parts = decode_string.split(',')
		new_comment = Comment(parts[0], int(parts[4]),parts[7].split('\x03'), int(parts[2]), bool(parts[5]), int(parts[6]))
		new_comment.setLocal(local)

		if new_comment.getID() > cls.last_comment_id:
			cls.last_comment_id = new_comment.getID()

		current = parent

		# find the owner level for the comment
		while (current is not None):
			if current.__class__.__name__ == parts[1]:
				current.addChildNode(new_comment)
				break

			current = current.getParent()
		return parent

	def __init__(self, user_name, time, text, line, pre_side=True, comment_id=None):
		super(Comment, self).__init__()

		self.is_local = False

		self.user_name = user_name
		self.time = time

		if comment_id is not None:
			self.comment_id = comment_id
		else:
			self.comment_id = Comment.getNextID()

		if type(text) == list:
			self.text = text
		else:
			self.text = [text]

		self.line = int(line)

		self.side = pre_side	# pre_side is the old code, post_side is the new code.
								# TODO: fix the naming this is really poor

	def getID(self):
		return self.comment_id

	def isPreSide(self):
		return self.side

	def isLocal(self):
		return self.is_local

	def setLocal(self, local):
		self.is_local = local

	def toString(self):
		return "comment:" + self.user_name + "," + self.getParent().__class__.__name__ + ","+ str(self.line) + "," + str(self.side) + "," + str(self.time) + "," + str(self.side) + "," + str(self.comment_id) + "," + '\x03'.join(self.text)

	def getCommentSide(self):
		return self.side

	def getLine(self):
		return self.line

	def getTitle(self):
		return self.text[0]

	def getContents(self):
		return self.text

	def setContents(self, contents):
		if type(contents) != list:
			self.text = [contents]
		else:
			self.text = contents

	def makeLocal(self):
		current = self.getParent()
		self.is_local = True

		while current is not None and not current.isLocal():
			current.setLocal(True)
			current = current.getParent()

# vim: ts=4 sw=4 noexpandtab nocin ai
