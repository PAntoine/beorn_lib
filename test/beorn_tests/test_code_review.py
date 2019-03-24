#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#    file: test_amend
#    desc: This test case builds a repository for the given type in a known layout
#          this is used to test that the supported scm type works.
#
#  author: Peter Antoine
#    date: 04/12/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Import the external modules.
#---------------------------------------------------------------------------------
import os
import shutil
import unittest
from beorn_lib.code_review import Change, Comment, LocalCodeReviews
from .repo_builder import buildRepo, removeRepo

#---------------------------------------------------------------------------------
# Test Sequences.
#---------------------------------------------------------------------------------
class TestCodeReview(unittest.TestCase):
	def __init__(self, testname = 'runTest',  scm_type = None, scm_dir = None, test_data = None):
		self.scm = None
		self.scm_type = scm_type
		self.repo_dir = scm_dir
		self.test_directory = os.path.join(test_data, 'code_review_test')

		# initialise the test framework
		super(TestCodeReview, self).__init__(testname)

	def setUp(self):
		self.scm = buildRepo(self)

		if os.path.isdir(self.test_directory):
			shutil.rmtree(self.test_directory, ignore_errors=True)

	def tearDown(self):
		removeRepo(self)
		
		if os.path.isdir(self.test_directory):
			shutil.rmtree(self.test_directory, ignore_errors=True)

	def all_nodes_function(self, last_visited_node, node, value, levels, direction):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = [' '*levels + type(node).__name__]
		else:
			value.append(' '*levels + type(node).__name__)

		return (node, value, False)

	def test_codeReview(self):
		""" Code Review Test

			This function will test the code review component.
		"""
		test = LocalCodeReviews(self.test_directory, {})
		self.assertIsNotNone(test)

		# test adding changes
		code_reviews = test.getChildren()
		self.assertEqual([], code_reviews)

		# switch to branch 9 - as the last commit has two files in the change.
		self.assertTrue(self.scm.setVersion("branch_9"))

		# Add the head of the current branch as a code review.
		history = self.scm.getHistory(max_entries=2)
		
		# now add a code review
		review = test.addReview(self.scm.getChangeList(history[0].version), True)
		code_reviews = test.getChildren()
		
		# test that the code review has been properly built
		self.assertEqual(1, len(test.getChildren()))
		self.assertEqual(1, len(test.getChildren()[0].getChildren()))
		self.assertEqual(3, len(test.getChildren()[0].getChildren()[0].getChildren()[0].getChildren()))

		# Need to test what the commit has - it should have 1 file with 3 changes.`
		#print review.getCurrentChange()
		#print review.getCurrentChange().getChildren()
		#print review.getCurrentChange().getChildren()[0].getChildren()

		# add some comments to a change
		comment = Comment('user1', 00000000, ["This is a comment on this line of stuff", "two lines of comment"], 0)
		review.getCurrentChange().getChildren()[0].getChildren()[1].addChildNode(comment)
		comment = Comment('user1', 00000001, ["This user really does not like you code"], 0)
		review.getCurrentChange().getChildren()[0].getChildren()[2].addChildNode(comment)
		comment = Comment('user2', 00000002, ["This user also does not like you code"], 0)
		review.getCurrentChange().getChildren()[0].getChildren()[2].addChildNode(comment)

		# add a new change
		new_change = review.addChange(self.scm.getChangeList(history[1].version))
		self.assertEqual(review.getCurrentChange(), new_change)
		
		# test that next change has been added as another change list
		self.assertEqual(2, len(review.getChildren()))
		self.assertEqual(2, len(test.getChildren()[0].getChildren()))
		self.assertEqual(3, len(test.getChildren()[0].getChildren()[0].getChildren()[0].getChildren()))

		code_reviews = test.getChildren()
		self.assertNotEqual([], code_reviews)

		# temp test for testing saving the code review.
		os.makedirs(self.test_directory)
		self.assertTrue(test.save())

		test_2 = LocalCodeReviews(self.test_directory, {})
		self.assertTrue(test_2.load())

		original = test.walkTree(self.all_nodes_function)
		loaded   = test_2.walkTree(self.all_nodes_function)

		self.assertEqual(original, loaded)

if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 noexpandtab nocin ai
