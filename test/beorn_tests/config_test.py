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
#    file: config_test
#    desc: This file holds the tests for the config.
#
#  author: Peter Antoine
#    date: 25/07/2015
#---------------------------------------------------------------------------------
#                     Copyright (c) 2015 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import glob
import shutil
import unittest
import platform
import beorn_lib.errors
from collections import OrderedDict

from beorn_lib.config import Config

TEST_LIST = [	'[item]',
				'name = something',
				'time = 5435435345',
				'[list]',
				'xxx = fdsfsdfsd',
				'name = fdsfsdf',
				'[list]',
				'xxx = fdsfsdfsd',
				'name = qqqqqqq',
				'[list]',
				'xxx = fdsfsdfsd',
				'name = vvvvvvv']

DELETE_ITEM = [	'[item]',
				'time = 5435435345',
				'[list]',
				'xxx = fdsfsdfsd',
				'name = fdsfsdf',
				'[list]',
				'xxx = fdsfsdfsd',
				'name = qqqqqqq',
				'[list]',
				'xxx = fdsfsdfsd',
				'name = vvvvvvv',
				'[new]',
				'name = value',
				'[new_1]',
				'name%0 = value_1',
				'name%1 = value_2']

DELETE_ITEM_2 = ['[item]',
				'time = 5435435345',
				'[new]',
				'name = value',
				'[new_1]',
				'name%0 = value_1',
				'name%1 = value_2']

class TestConfig(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname='runTest', test_data=None, temp_data=None):
		self.temp_data = temp_data

		# do the ground work for the test
		self.config_dir = os.path.join(self.temp_data,'config')

		# initialise the test framework
		super(TestConfig, self).__init__(testname)

	def setUp(self):
		""" This function deletes all the files before the test runs """
		if os.path.isdir(self.config_dir):
			# tidy up the test
			filelist = glob.glob(self.config_dir + '/*')
			for dfile in filelist:
				os.remove(dfile)
		else:
			os.makedirs(self.config_dir)

	def test_config(self):
		""" Config Tests

			This test exercises the system notes.
		"""
		# basic test of a created config
		new_config = Config(os.path.join(self.config_dir, 'test.cfg'))
		self.assertIsNotNone(new_config)
		self.assertEqual([], new_config.export())

		# test creation with a configuration
		config = {	'item':{'name':'something', 'time':'5435435345'},
					'list':[{'name':'fdsfsdf','xxx':'fdsfsdfsd'},
							{'name':'qqqqqqq','xxx':'fdsfsdfsd'},
							{'name':'vvvvvvv','xxx':'fdsfsdfsd'}]}

		new_config = Config(os.path.join(self.config_dir, 'test.cfg'), config)
		self.assertEqual(TEST_LIST, new_config.export())

		# test that the save works
		self.assertEqual(0, new_config.save())

		# Test the load of the config
		load_config = Config(os.path.join(self.config_dir, 'test.cfg'))
		self.assertEqual([], load_config.export())
		load_config.load()
		self.assertEqual(TEST_LIST, load_config.export())

		# not find a single item - Negative Testing
		self.assertIsNone(load_config.find('itemx'))
		self.assertIsNone(load_config.find('itemx', 'name'))
		self.assertIsNone(load_config.find('itemx', ['name', 'xxx']))
		self.assertIsNone(load_config.find('item', ['namex']))
		self.assertIsNone(load_config.find('item', ['name', 'xxx']))
		self.assertIsNone(load_config.find('item', ['namex', 'something']))

		# find a single item
		self.assertEqual({'name':'something', 'time':'5435435345'}, load_config.find('item'))
		self.assertEqual('something', load_config.find('item', 'name'))
		self.assertEqual('5435435345', load_config.find('item', 'time'))

		# find a list item
		self.assertEqual([{'name':'fdsfsdf', 'xxx':'fdsfsdfsd'},
							{'name':'qqqqqqq', 'xxx':'fdsfsdfsd'},
							{'name':'vvvvvvv', 'xxx':'fdsfsdfsd'}], load_config.find('list'))

		# Find items with specific values
		self.assertEqual('5435435345', load_config.find('item', 'time'))

		# Add new item to the configuration
		new_config.setValue('new', 'name', 'value')
		self.assertEqual({'name':'value'}, new_config.find('new'))
		self.assertEqual('value', new_config.find('new', 'name'))

		# Add a new item that turns an item into a list item
		new_config.setValue('new_1', 'name', ['value_1', 'value_2'])
		self.assertEqual({'name':['value_1', 'value_2']} , new_config.find('new_1'))

		# remove item from the config item
		self.assertTrue(new_config.remove('item', 'name'))
		self.assertEqual(DELETE_ITEM, new_config.export())
		new_config.remove('list')
		self.assertEqual(DELETE_ITEM_2, new_config.export())

# vim: ts=4 sw=4 noexpandtab nocin ai
