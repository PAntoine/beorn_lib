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

import os
from .review_engine import ReviewEngine, registerEngine
from beorn_lib.nested_tree import NestedTreeNode
from beorn_lib.code_review import CodeReview, Change, Comment, ChangeFile, Hunk

class LocalReviewEngine(ReviewEngine):
	decode_jump_list = {'change':	Change,
						'file':		ChangeFile,
						'comment':	Comment,
						'hunk':		Hunk,
						'review':	CodeReview}


	def __init__(self, configuration, password_function=None):
		super(LocalReviewEngine, self).__init__(configuration, password_function)

		self.directory = os.path.realpath('.indigobuggie')

	@classmethod
	def getDefaultConfiguration(cls):
		return {'root_directory': '.'}

	@classmethod
	def getDialogLayout(cls):
		return [('TextField', 'text', 'root_directory', 'Code Review Directory')]

	def getName(self):
		return "Local Code Reviews"

	def getNumComments(self):
		result = 0

		for item in self.getChildren():
			result += item.getNumComments()

		return result

	def load(self):
		""" Load

			This function will load the code review from the file system and populate
			the code review.
		"""
		files = os.listdir(self.directory)
		remove_list = []

		# load the note files
		for note_file in files:
			bits = note_file.split('@')

			file_name = os.path.join(self.directory, note_file)

			if bits[0] == self.getUser() and bits[1] == self.getCurrentMachine():
				# we have a file that belongs to the current user and current machine.
				self.loadFile(file_name, True)
			else:
				self.loadFile(file_name, False)

			# remove the note file from the list
			remove_list.append(note_file)

		# now remove the files we don't want to merge
		for r in remove_list:
			files.remove(r)

		# now compare the others against the current file
		for note_file in files:
			file_name = os.path.join(self.directory, note_file)
			self.mergefile(file_name)

		return True

	def decode(self, previous, decode_string, local):
		parts = decode_string.split(',')

		code_review = CodeReview(parts[0], parts[1], int(parts[2]))
		code_review.setLocal(local)

		return code_review


	def loadFile(self, file_name, local):
		try:
			with open(file_name, "rb") as f:
				data = f.readlines()
				current_item = None

				for item in data:
					parts = item[:-1].split(':', 1)

					if parts[0] in LocalReviewEngine.decode_jump_list:
						current_item = LocalReviewEngine.decode_jump_list[parts[0]].decode(current_item, parts[1], local)

					if parts[0] == 'review':
						self.addChildNode(current_item)
		except IOError:
			return False
		except OSError:
			return False
		return True

	def readerFunction(self, last_visited_node, node, value, level, direction, parameter):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = []

		if type(node) == LocalReviewEngine:
			value.append("HEADER")
		else:
			value.append(node.toString())


		return (node, value, False)

	def save(self):
		""" Save Note File

			This methods will save the note list to file. It will enumerate the Subjects and
			save all the notes within the subjects to file.
		"""
		file_name = os.path.join(self.directory , self.current_user + '@' + self.current_machine)

		try:
			out_file = open(file_name,'wb')
			for line in self.walkTree(self.readerFunction):
				out_file.write(line + '\n')

			out_file.close()
			result = True

		except IOError:
			result = False

		return result

	def addReview(self, change_list, is_local):
		new_review = CodeReview(author=change_list.author, is_local=is_local)
		new_review.addChildNode(Change(change_list, is_local=is_local), NestedTreeNode.INSERT_FRONT)
		self.addChildNode(new_review)
		return new_review

registerEngine(LocalReviewEngine)

# vim: ts=4 sw=4 noexpandtab nocin ai
