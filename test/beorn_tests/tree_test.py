#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#    file: tree_test
#    desc: This tests the tree functionality.
#
#  author: Peter Antoine
#    date: 15/03/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import unittest
from beorn_lib.tree_item import TreeItem

#---------------------------------------------------------------------------------
# Helper Class
#---------------------------------------------------------------------------------
class TestClass(object):
	def __init__(self, item):
		self.item = item

	def updateTreeItem(self, item):
		item.updateTree([])

	def getTree(self, parent = None):
		new_item = TreeItem('item_' + str(self.item), parent, payload = self)

		return new_item

#---------------------------------------------------------------------------------
# Test Class
#---------------------------------------------------------------------------------

class TestTree(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None, temp_data = None):
		self.test_data = test_data
		self.temp_data = temp_data

		# initialise the test framework
		super(TestTree, self).__init__(testname)

	#---------------------------------------------------------------------------------
	# Test Data
	#---------------------------------------------------------------------------------
	test_item = [ 	TestClass('0'),
					TestClass('1'),
					TestClass('2'),
					TestClass('3'),
					TestClass('4'),
					TestClass('5'),
					TestClass('6'),
					TestClass('7'),
					TestClass('8'),
					TestClass('9'),
					TestClass('10'),
					TestClass('11'),
					TestClass('12'),
					TestClass('13'),
					TestClass('14'),
					TestClass('15'),
					TestClass('16'),
					TestClass('17'),
					TestClass('18'),
					TestClass('19')
				]

	#---------------------------------------------------------------------------------
	# Helper Functions
	#---------------------------------------------------------------------------------
	def buildTree(self, tree_list, entry = None):
		""" Build Tree """
		if entry is None:
			result = TreeItem('base', None)
		else:
			result = entry

		# Ok,  two identical lists
		for item in tree_list:
			new_item = TreeItem('item_' + str(item), result, payload = TestTree.test_item[item])
			result.appendEntry(new_item)

		return result

	def compareLists(self, item, item_list):
		""" Compare Lists """
		result = False

		if len(item.item_list) == len(item_list):
			for index in range(0, len(item.item_list)):
				if item.item_list[index].payload != item_list[index]:
					break
			else:
				result = True

		return result

	#---------------------------------------------------------------------------------
	# Test Functions
	#---------------------------------------------------------------------------------

	def test_TestUpdateTree(self):
		""" Test Update Tree """

		base = self.buildTree(range(1, 7))
		object_list = [TestTree.test_item[1], TestTree.test_item[2], TestTree.test_item[3], TestTree.test_item[4], TestTree.test_item[5], TestTree.test_item[6]]
		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

		# Ok,  b is longer than a
		base = self.buildTree([1, 2, 3, 4, 5, 6])
		object_list = [	TestTree.test_item[1],
						TestTree.test_item[2],
						TestTree.test_item[3],
						TestTree.test_item[4],
						TestTree.test_item[5],
						TestTree.test_item[6],
						TestTree.test_item[7]]

		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

		#Ok,  b is longer then a,  in the middle
		base = self.buildTree([1, 2, 3, 4, 5, 6])
		object_list = [	TestTree.test_item[1],
						TestTree.test_item[8],
						TestTree.test_item[2],
						TestTree.test_item[3],
						TestTree.test_item[7],
						TestTree.test_item[4],
						TestTree.test_item[5],
						TestTree.test_item[6]]

		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

		#Ok,  b is shorter then a,  in the middle
		base = self.buildTree([1, 2, 3, 4, 5, 6])
		object_list = [TestTree.test_item[1], TestTree.test_item[2], TestTree.test_item[5], TestTree.test_item[6]]

		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

		#Ok,  b is shorter then a,  in the middle with a new element
		base = self.buildTree([1, 2, 3, 4, 5, 6])
		object_list = [TestTree.test_item[1], TestTree.test_item[2], TestTree.test_item[7], TestTree.test_item[5], TestTree.test_item[6]]

		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

		#Ok,  a is short then b at the front
		base = self.buildTree([1, 2, 3, 4, 5, 6])
		object_list = [	TestTree.test_item[1],
						TestTree.test_item[2],
						TestTree.test_item[3],
						TestTree.test_item[4],
						TestTree.test_item[5],
						TestTree.test_item[6]]

		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

		#Ok,  a is short then b at the front,  with a new element at the end
		base = self.buildTree([2, 3, 4, 5, 6, 7])
		object_list = [	TestTree.test_item[1],
						TestTree.test_item[2],
						TestTree.test_item[3],
						TestTree.test_item[4],
						TestTree.test_item[5],
						TestTree.test_item[6]]

		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

		#Ok,  deleted elements at the end and the middle for a.
		base = self.buildTree([2, 3, 4, 8, 9, 10, 5, 6, 7])
		object_list = [	TestTree.test_item[1],
						TestTree.test_item[2],
						TestTree.test_item[3],
						TestTree.test_item[4],
						TestTree.test_item[5],
						TestTree.test_item[6]]

		base.updateTree(object_list)
		self.assertTrue(self.compareLists(base, object_list))

# vim: ts=4 sw=4 noexpandtab nocin ai
