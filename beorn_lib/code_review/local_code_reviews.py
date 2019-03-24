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
#    file: local_code_review
#    desc: This class defines a local code review.
#
#    	   it build on the code review class.
#
#  author: peter
#    date: 02/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
from beorn_lib.code_review import CodeReviews, CodeReview, Change, Comment, ChangeFile, Hunk
from beorn_lib.nested_tree import NestedTreeNode

class LocalCodeReviews(CodeReviews):
	decode_jump_list = {'change':	Change,
						'file':		ChangeFile,
						'comment':	Comment,
						'hunk':		Hunk,
						'review':	CodeReview}

	def __init__(self, root, configuration):
		super(LocalCodeReviews, self).__init__()

		if 'root_directory' in configuration and configuration['root_directory'] != '.':
			self.directory = configuration['root_directory']
		else:
			self.directory = root

		self.is_local	= False
		self.colour		= -1

	def __getitem__(self, key):
		for item in self.getChildren():
			if type(key) == CodeReview:
				if key.review_id == item.review_id:
					return item
			else:
				if key == item.review_id:
					return item

		raise KeyError("Does not exist")

	def __contains__(self, other):
		""" Contains

			Will return True if 'other' is the name of one of the children.
		"""
		for item in self.getChildren():
			if type(other) == CodeReview:
				if other.review_id == item.review_id:
					return True
			else:
				if other == item.review_id:
					return True

		return False

	def getName(self):
		return "Local Code Reviews"

	def isLocal(self):
		return self.is_local

	def setLocal(self, local):
		self.is_local = local

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

			if bits[0] == self.current_user and bits[1] == self.current_machine:
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
			file_name = os.path.join(self.directory, note_file )
			self.mergefile(file_name)

		return True

	def loadFile(self, file_name, local):
		try:
			with open(file_name, "rb") as f:
				data = f.readlines()
				current_item = None

				for item in data:
					parts = item[:-1].split(':', 1)

					if parts[0] in LocalCodeReviews.decode_jump_list:
						current_item = LocalCodeReviews.decode_jump_list[parts[0]].decode(current_item, parts[1], local)

					if parts[0] == 'review':
						self.addChildNode(current_item)

		except IOError:
			result = False

	def readerFunction(self, last_visited_node, node, value, level, direction):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = []

		if type(node) == LocalCodeReviews:
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

# vim: ts=4 sw=4 noexpandtab nocin ai
