#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#    file: test_search
#    desc: This file holds the tests that test the search functionality and the
#          bigraph functions.
#
#  author: Peter Antoine
#    date: 13/12/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Import the external modules.
#---------------------------------------------------------------------------------
import unittest
import beorn_lib.scm as scm
from beorn_lib.scm.bigraph import BIGRAPH as BIGRAPH
from .scm_test import SCMTest

#---------------------------------------------------------------------------------
# Test Sequences.
#---------------------------------------------------------------------------------
class TestSearch(SCMTest):
	def __init__(self, testname = 'runTest',  scm_type = None, scm_dir = None, test_data = None):
		super(TestSearch, self).__init__(testname)

	def test_BiGraph(self):
		""" This function tests that the bi-directional graph works.
		"""

		if self.scm_type == 'P4':
			unittest.skip("No testing for P4")
		else:
			test = scm.new(self.directory)

			graph = BIGRAPH.buildGraph(test)
			self.assertIsNotNone(graph,"Failed to builds the Graph")
			self.assertNotEqual(graph.index, [], "Graph index is empty, and should have elements in it")
			self.assertEqual(len(graph.index), 50, "Graph index has the wrong number of commits in it.")

	def test_BiGraphSearch(self):
		""" BIGRAPH Search Test

			This test exercises the bigraph searches.
		"""
		if self.scm_type == 'P4':
			unittest.skip("No testing for P4")
		else:
			test = scm.new(self.directory)
			graph = BIGRAPH.buildGraph(test)

			lists = graph.searchByBranch(['branch_0', 'branch_10', 'branch_5','branch_1'])

			self.assertEqual(4, len(lists))

	def test_BiGraphLinearise(self):
		""" BIGRAPH Search Linearise Test

			This test exercises the bigraph searches.
		"""
		if self.scm_type == 'P4':
			unittest.skip("No testing for P4")
		else:
			test = scm.new(self.directory)
			graph = BIGRAPH.buildGraph(test)

			search_result = graph.searchByBranch(['branch_0', 'branch_10', 'branch_5','branch_1'])

			commits = graph.lineariseSearch(search_result)

			self.assertEqual(25, len(commits))

# vim: ts=4 sw=4 noexpandtab nocin ai
