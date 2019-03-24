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
#    file: message_tree
#    desc:
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

class Message(NestedTreeNode):
	def __init__(self, mid = None, name = None, date = None, user = None, parent_id = None, reference = None, message = None):
		super(Message, self).__init__(name, None)

		self.mid=mid
		self.name=name
		self.date=date
		self.user=user_id
		self.parent_id=parent_id
		self.reference=reference
		self.message=message

	def __lt__(self, other):
		if type(other) is Message:
			return self.name < other.name
		return NotImplemented

	def __contains__(self, other):
		""" Contains

			Will return True if 'other' is the name of one of the children.
		"""
		if type(other) == str or type(other) == unicode:
			find_name = other
		elif isinstance(other, Message):
			find_name = other.name
		else:
			return False

		for child in self.getChildren():
			if find_name == child.name:
				return True
		else:
			return False

	def toString(self):
		""" To String

			toString() -> encoded message string
		"""
		if self.reference == '':
			reference = ''
		else:
			reference = b64encode(self.reference)

		if self.parent_id is None:
			parent_id = ''
		else:
			parent_id = self.parent_id

		return "%s = %s:%s:%s:%s:%s:%d" % (self.mid, b64encode(self.name), parent_id, self.user, reference, b64encode(self.message), self.date)

	def fromString(self, message_string):
		""" Load Message From A String

				load(message_string) -> result code

			This function will unpack the message string into Message.
		"""
		result = None
		parts = message_string.strip().split(' = ')
		id_parts = parts[1].split(':')

		if len(id_parts) >= 6:
			mid = parts[0]

			# id_parts = name, parent_id, user, reference, message, date
			self.name		= b64decode(id_parts[0].strip())
			self.parent_id	= id_parts[1].strip()
			self.user_id	= id_parts[2].strip()
			self.reference	= b64decode(id_parts[3].strip())
			self.message	= b64decode(id_parts[4].strip())
			self.date		= int(id_parts[5])

			result = self
		return result

	def getDate(self):
		return self.date

	def getName(self):
		return self.name

	def getMessageText(self):
		""" Get the Message Text """
		return self.message

# vim: ts=4 sw=4 noexpandtab nocin ai
