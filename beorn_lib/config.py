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
#    file: config
#    desc: Configuration.
#
#          This function simply will read/write a simple config file. It does less
#          things than the std library config reader, but it is part of the library
#          and needs no external support and is too simple a beasty to worry about
#          it being the same.
#
#          It will return a config item, that is a set of dictionaries with config
#          items in them.
#
#  author: Peter Antoine
#    date: 25/07/2015
#---------------------------------------------------------------------------------
#                     Copyright (c) 2015 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import time
import string
import errors
from collections import OrderedDict

class Config(object):
	""" Beorn Config Class

		This class handles the Configuration files.

		This handles configuration items in the following ways. For the [..] items
		it is added to the config dictionary with the string between the [] as the
		key. If there is more then one item with the same string then the item is
		removed and the item is replaced with a list item, but is keyed with the
		same name, both dictionary items are added to the list. Any subsequent items
		with the same name are added to the list.

		i.e.

		[item]
		name = somehting
		time = 5435435345
		[list]
		name = fdsfsdf
		xxx = fdsfsdfsd

		Will produce:
		 config = {'item':{'name':'something', 'time':5435435345}, 'list',{'name':'..','xxx':...}}

	    But after it finds, the following:

		[list]
		name = vvvvvvv
		xxx = fdsfsdfsd
		[list]
		name = fffffff
		xxx = fdsfsdfsd

		It will produce:

		 config = {'item':{'name':'something', 'time':5435435345},
		           'list',[{'name':'fdsfsdf','xxx':'fdsfsdfsd'},
				           {'name':'vvvvvvv','xxx':'fdsfsdfsd'},
				           {'name':'vvvvvvv','xxx':'fdsfsdfsd'}]}

		Obviously each config item does not need to have the same items and the config
		class does not check or care in anyway.

		The config items are stored in an ordered dict so that when writing back the configuration
		it does not change the order, so that changes can be diff'ed in an SCM as that will be
		backed by one (more that likely).
	"""

	def __init__(self, filename, config = None):
		""" Init the Config Class """
		if config is None:
			self.sections = OrderedDict()

		elif type(config) == dict:
			self.sections = OrderedDict(config)

		elif type(config) == OrderedDict:
			self.sections = config

		self.filename = filename

	def load(self):
		""" This function will load the configuration """
		if self.filename is None:
			result = ERROR_NO_FILENAME_SPECIFIED

		else:
			try:
				# now open the project file
				with open(self.filename) as f:
					items = f.read().splitlines()

				result = self._parseConfigItems(items)

			except IOError:
				self.filename = None
				result = ERROR_FAILED_TO_READ_FROM_FILE

		return result

	def save(self):
		""" Save Confiuration

			load(filename) -> result_code

			This function will load the project. It will expect the file to exist and be
			in the correct format as produced by the Project.save() function. This will load the
			project from the given file, also it will remember the filename and will use this name
			for updating the project later.
		"""
		result = OK

		if self.filename is None:
			result = ERROR_NO_FILENAME_SPECIFIED

		else:
			try:
				proj_file = open(self.filename,'wb')

				for line in self.export():
					proj_file.write("%s\n" % line)

				proj_file.close()

			except IOError:
				result = ERROR_FAILED_TO_WRITE_TO_FILE

		return result

	def export(self):
		""" Export Config

			This will produce a list of strings containing the configuration.
		"""
		result = []

		for key in self.sections:
			if type(self.sections[key]) == list:
				for list_item in self.sections[key]:
					result.append("[%s]" % key)
					result.extend(self._dumpItem(list_item))
			else:
				result.append("[%s]" % key)
				result.extend(self._dumpItem(self.sections[key]))

		return result

	def find(self, section, item = None, value = None):
		""" Find

			This function will return the item(s) that match the search criteria.
			If the item parameter is None, then it will return the whole section
			that matches the section that the name matches. If the item is given
			then it will return the item that matches the given name.

			If the section is a list then it will return all the items that match
			the section. It the item is not None it will return all the item from
			the section that has the specified item.

			If value is supplied it will check if the item as the value, and only
			return items that have the value.
		"""
		result = None

		if section in self.sections:
			if type(self.sections[section]) == list:
				# Ok, we have a list of items
				if item is None:
					result = self.sections[section]
				else:
					result = []
					for entry in self.sections[section]:
						if item in entry:
							if value is None or value == entry[item]:
								result.append(entry)

			else:
				if item is None:
					result = self.sections[section]
				elif item in self.sections[section]:
					if value is None or value == self.sections[section][item]:
						result = self.sections[section][item]

		return result

	def add(self, section, item = None, value = None):
		""" Add Item or Section to config

			This function will add an entry to the configuration.
		"""
		new_section = OrderedDict()
		new_section[item] = value

		self._addNewSection(section, new_section)

	def remove(self, section, item = None, value = None):
		""" Remove

			This function will remove all the items that match the search. it uses
			the same search as the find.
		"""
		if section in self.sections:
			if type(self.sections[section]) == list:
				# Ok, we have a list of items
				if item is None:
					del self.sections[section]
				else:
					new_list = []
					for entry in self.sections[section]:
						if item in entry:
							if value is not None and value != entry[item]:
								new_list.append(entry)
						else:
							new_list.append(entry)

					self.sections[section] = new_list
			else:
				if item is None or item in self.sections[section]:
					if value is None or value == self.sections[section][item]:
						del self.sections[section]

	def _dumpItem(self, item):
		""" This will dump a dictionary """
		result = []

		for key in item:
			result.append("%s = %s" % (key, item[key]))

		return result

	def _addNewSection(self, current_key, current_section):
		""" This de-duplicates adding a new item to the config """
		# Ok, deal with the old item
		if current_key in self.sections:
			if type(self.sections[current_key]) == list:
				self.sections[current_key].append(current_section)

			else:
				temp = self.sections[current_key]
				self.sections[current_key] = [temp, current_section]
		else:
			self.sections[current_key] = current_section

	def _parseConfigItems(self, items):
		""" This """
		result = True
		current_key = None
		current_section = OrderedDict()

		for item in items:
			if item[0] == '[':
				if current_section != {}:
					self._addNewSection(current_key, current_section)

					# clear down for the next go
					current_section = OrderedDict()
					current_key = None

				# now start the new item
				if item[-1] == ']':
					current_key = item[1:-1]

			elif len(item) > 0:
				# Ok, it's not just a blank line.
				equals = item.index('=')
				if equals == -1:
					result = False
					break

				else:
					current_section[item[0:equals-1]] = item[equals+2:]

		# handle stragglers
		if current_section != {}:
			self._addNewSection(current_key, current_section)

		return result

# vim: ts=4 sw=4 noexpandtab nocin ai
