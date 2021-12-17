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
#    file: test_source_tree
#    desc: This will test the source tree.
#
#  author: peter
#    date: 21/10/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------
import os
import unittest
from beorn_lib import SourceTree


#---------------------------------------------------------------------------------
# Test Class
#---------------------------------------------------------------------------------
class TestSourceTree(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname='runTest', test_data=None, temp_data=None):
		self.test_data = test_data
		self.temp_data = temp_data

		# initialise the test framework
		super(TestSourceTree, self).__init__(testname)

	def setUp(self):
		# generate platform non-specific
		TestSourceTree.tree_format = []
		for item in TestSourceTree.proto_tree_format:
			TestSourceTree.tree_format.append(os.path.join(*item))

		self.test_root = os.path.join(self.temp_data, 'source_test_tree')

	def tearDown(self):
		self.deleteTree(self.test_root)

	#---------------------------------------------------------------------------------
	# Test Data
	#---------------------------------------------------------------------------------
	dir_1 = [True, True, True]
	dir_2 = [True, dir_1, True, dir_1]
	dir_3 = [dir_2, True, [True, True]]

	dir_4 = [True, [True, True, True], True]
	dir_5 = [True, dir_4]

	dir_6 = [dir_1, dir_2, dir_1]

	test_tree = [True, [dir_1], dir_3, True, dir_5, dir_6, True]

	proto_tree_format = [
			['test_source', '.dmy'],
			['test_source', 'dir_item_0'],
			['test_source', 'dir_item_1'],
			['test_source', 'dir_item_1', 'dir_item_0'],
			['test_source', 'dir_item_1', 'dir_item_0', 'dir_item_0'],
			['test_source', 'dir_item_1', 'dir_item_0', 'dir_item_1'],
			['test_source', 'dir_item_1', 'dir_item_0', 'dir_item_2'],
			['test_source', 'dir_item_2'],
			['test_source', 'dir_item_2', 'dir_item_0'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_0'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_1'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_1', 'dir_item_0'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_1', 'dir_item_1'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_1', 'dir_item_2'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_2'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_3'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_3', 'dir_item_0'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_3', 'dir_item_1'],
			['test_source', 'dir_item_2', 'dir_item_0', 'dir_item_3', 'dir_item_2'],
			['test_source', 'dir_item_2', 'dir_item_1'],
			['test_source', 'dir_item_2', 'dir_item_2'],
			['test_source', 'dir_item_2', 'dir_item_2', 'dir_item_0'],
			['test_source', 'dir_item_2', 'dir_item_2', 'dir_item_1'],
			['test_source', 'dir_item_3'],
			['test_source', 'dir_item_4'],
			['test_source', 'dir_item_4', 'dir_item_0'],
			['test_source', 'dir_item_4', 'dir_item_1'],
			['test_source', 'dir_item_4', 'dir_item_1', 'dir_item_0'],
			['test_source', 'dir_item_4', 'dir_item_1', 'dir_item_1'],
			['test_source', 'dir_item_4', 'dir_item_1', 'dir_item_1', 'dir_item_0'],
			['test_source', 'dir_item_4', 'dir_item_1', 'dir_item_1', 'dir_item_1'],
			['test_source', 'dir_item_4', 'dir_item_1', 'dir_item_1', 'dir_item_2'],
			['test_source', 'dir_item_4', 'dir_item_1', 'dir_item_2'],
			['test_source', 'dir_item_5'],
			['test_source', 'dir_item_5', 'dir_item_0'],
			['test_source', 'dir_item_5', 'dir_item_0', 'dir_item_0'],
			['test_source', 'dir_item_5', 'dir_item_0', 'dir_item_1'],
			['test_source', 'dir_item_5', 'dir_item_0', 'dir_item_2'],
			['test_source', 'dir_item_5', 'dir_item_1'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_0'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_1'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_1', 'dir_item_0'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_1', 'dir_item_1'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_1', 'dir_item_2'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_2'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_3'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_3', 'dir_item_0'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_3', 'dir_item_1'],
			['test_source', 'dir_item_5', 'dir_item_1', 'dir_item_3', 'dir_item_2'],
			['test_source', 'dir_item_5', 'dir_item_2'],
			['test_source', 'dir_item_5', 'dir_item_2', 'dir_item_0'],
			['test_source', 'dir_item_5', 'dir_item_2', 'dir_item_1'],
			['test_source', 'dir_item_5', 'dir_item_2', 'dir_item_2'],
			['test_source', 'dir_item_6']]

	proto_source_modified = [
			['A', ['dir_item_2', 'dir_item_0', 'dir_item_2']],
			['A', ['dir_item_2', 'dir_item_2']],
			['D', ['dir_item_5', 'dir_item_new']],
			['A', ['dir_item_2', 'dir_item_0', 'dir_item_1', 'dir_item_1']],
			['M', ['dir_item_2', 'dir_item_0', 'dir_item_3', 'dir_item_1']],
			['M', ['dir_item_4', 'dir_item_1', 'dir_item_1', 'dir_item_2']],
			['M', ['dir_item_5', 'dir_item_1', 'dir_item_1', 'dir_item_2']],
			['A', ['dir_item_5', 'dir_item_2', 'dir_item_2']]]

	#---------------------------------------------------------------------------------
	# Helper Function
	#---------------------------------------------------------------------------------
	def deleteTree(self, path):
		for item in os.walk(path, topdown=False):
			for leaf in item[2]:
				os.unlink(os.path.join(item[0], leaf))

			os.rmdir(item[0])

	def buildSourceTree(self, path, tree):
		os.makedirs(path)

		if path == self.test_root:
			my_file = os.path.join(path, '.dmy')
			mf = open(my_file, 'w')
			mf.close()

		for index, x in enumerate(tree):
			name = "dir_item_" + str(index)
			curr_path = os.path.join(path, name)

			if type(x) == bool and x:
				with open(curr_path, 'w') as source_file:
					source_file.writelines(["line: %d\n" % i for i in range(1, 30)])
			else:
				self.buildSourceTree(curr_path, x)

	def createDirectory(self, item, tree):
		for index, x in enumerate(tree):
			name = "dir_item_" + str(index)

			if type(x) == bool and x:
				item.addChildNode(SourceTree(name))
			else:
				new_item = SourceTree(name)
				item.addChildNode(new_item)
				self.createDirectory(new_item, x)

	def all_nodes_function(self, last_visited_node, node, value, levels, direction, parameter):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			if parameter is not None:
				value = [os.path.abspath(node.getPath())]
			else:
				value = [node.getPath()]
		else:
			if parameter is not None:
				value.append(os.path.abspath(node.getPath()))
			else:
				value.append(node.getPath())

		return (node, value, False)

	#---------------------------------------------------------------------------------
	# Test Function
	#---------------------------------------------------------------------------------
	def test_TestBasicTree(self):
		""" Test Basic Tree """
		source_tree = SourceTree('test_source', root=self.test_root)

		source_tree.addChildNode(SourceTree('.dmy'))
		self.createDirectory(source_tree, TestSourceTree.test_tree)

		# check if the array matche
		self.assertEqual(source_tree.walkTree(self.all_nodes_function), TestSourceTree.tree_format)

	def test_TestSourceLocalFiles(self):
		""" Test Source Files """
		self.buildSourceTree(self.test_root, TestSourceTree.test_tree)

		source_tree = SourceTree('test_source', root=self.test_root)

		source_tree.update()
		source_tree.update()
		self.assertEqual(source_tree.walkTree(self.all_nodes_function), TestSourceTree.tree_format)

		source_tree.update()
		walked_tree = source_tree.walkTree(self.all_nodes_function)
		self.assertEqual(walked_tree, TestSourceTree.tree_format)

		file_name = os.path.join(self.test_root, 'dir_item_2', 'dir_item_0', 'dir_item_1', 'dir_item_1')
		found = source_tree.findItemNode(file_name)
		self.assertTrue(found.isOnFileSystem(), "file exists and is not flagged as such")

		os.unlink(file_name)
		found = source_tree.findItemNode(file_name)
		self.assertTrue(found.isOnFileSystem(), "file flagged incorrectly on file system - before update")

		source_tree.update()
		found = source_tree.findItemNode(file_name)
		self.assertIsNotNone("File that does not exist on file system still shows in tree")
		self.assertFalse(found.isOnFileSystem(), "file flagged incorrectly on file system")

		source_tree.update()
		walked_tree = source_tree.walkTree(self.all_nodes_function)
		self.assertEqual(walked_tree, TestSourceTree.tree_format, "tree walk does not match built tree")

		source_tree.prune()
		found = source_tree.findItemNode(file_name)
		self.assertIsNone(found, "Item still in tree after prune")

		fred = os.path.join('dir_item_5', 'dir_item_1')
		found = source_tree.findItemNode(fred)
		found.deleteNode(True)
		walked_tree = source_tree.walkTree(self.all_nodes_function)

		found = source_tree.findItemNode(fred)
		self.assertIsNone(found)

		self.assertNotEqual(walked_tree, TestSourceTree.tree_format, "tree walk does not match built tree")

	def test_TestSubTreeAdd(self):
		""" Test Basic Tree """
		source_tree = SourceTree('test_source', root=self.test_root)

		source_tree.addChildNode(SourceTree('.dmy'))
		self.createDirectory(source_tree, TestSourceTree.test_tree)

		# On, rebase the tree up two levels.
		d = os.path.split(source_tree.getPath())
		f = os.path.split(d[0])
		difference = os.path.relpath(source_tree.getPath(), f[0])

		source_tree.addTreeNodeByPath(f[0], rebase_tree=True)

		fred = os.path.join(f[0], 'dir_item_5', 'dir_item_1')
		found = source_tree.findItemNode(fred)
		self.assertIsNone(found)

		new_test_tree = []
		for item in TestSourceTree.tree_format:
			# rebasing the tree - should move it to the true directory name
			new_test_tree.append(os.path.join('beorn_lib', difference) + item[11:])

		b = source_tree.walkTree(self.all_nodes_function)

		# check if the array matches the new one - ignoring the two new nodes at the
		# front to the two new level directories.
		self.assertEqual(source_tree.walkTree(self.all_nodes_function)[2:], new_test_tree)

	def test_TestSourceFilesChanges(self):
		""" Test Changes to the Source Tree """
		self.buildSourceTree(self.test_root, TestSourceTree.test_tree)

		source_tree = SourceTree('test_source', root=self.test_root)
		source_tree.update()

		walked_tree = source_tree.walkTree(self.all_nodes_function)
		self.assertEqual(walked_tree, TestSourceTree.tree_format, "tree walk does not match built tree")

	def test_StateAddAndRemove(self):
		""" Test that SCM state changes amend the tree correctly """
		pass
		# TODO # - I know weak - but meh, it works.

	def test_PruneAfterFileDelete(self):
		""" Test that the files that are deleted from the file system stay in the tree
			and are only pruned when the prune is called. Also that if any other flags
			are set on the tree they are not removed when the prune is called. """
		pass
		# TODO #

# vim: ts=4 sw=4 noexpandtab nocin ai
