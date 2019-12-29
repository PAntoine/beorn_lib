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
#    file: swarm_code_reviews
#    desc: This is a test that works with swarm.
#
#  author: peter
#    date: 16/10/2019
#---------------------------------------------------------------------------------
#                     Copyright (c) 2019 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Import the external modules.
#---------------------------------------------------------------------------------
import os
import shutil
import unittest
import getpass
from beorn_lib.scm import SCM_P4
from beorn_lib.code_review import Change, Comment, SwarmReviewEngine
from test.utils.repo_builder import buildRepo, removeRepo

#---------------------------------------------------------------------------------
# Test Sequences.
#---------------------------------------------------------------------------------
class TestSwarmCodeReview(unittest.TestCase):
	def __init__(self, testname = 'runTest',  scm_type = None, scm_dir = None, test_data = None):
		self.scm = None
		self.scm_type = scm_type
		self.repo_dir = scm_dir

		# initialise the test framework
		super(TestSwarmCodeReview, self).__init__(testname)

	def all_nodes_function(self, last_visited_node, node, value, levels, direction):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = [' '*levels + type(node).__name__]
		else:
			if node.__class__.__name__ == 'Hunk':
				value.append(' '*levels + str(node.original_line) + " " + str(node.original_length))
			else:
				value.append(' '*levels + type(node).__name__)

		return (node, value, False)

	def password_function(self, user):
		return getpass.getpass()

	def test_codeReview(self):
		""" Code Review Test

			This function will test the code review component.
		"""
		config = {'swarm_server': 'http://192.168.178.40',
				'perforce_server': '192.168.178.31:1666',
				'poll_period': str(60*60),					# Once an hour
				'user': 'peter',
				'as_author': False,
				'user_group': [] }

		code = SwarmReviewEngine(config, self.password_function)
		code.scm = SCM_P4(repo_url = config['perforce_server'])
		code.update()
		items = code.walkTree(self.all_nodes_function)
		childs_a = code.getChildren()

		code.update()
		childs_b = code.getChildren()

		code.update()
		childs_c = code.getChildren()

		code.update()

		code.updateReviews()
		print "childs", len(childs_b), len(childs_a), len(childs_c)

# vim: ts=4 sw=4 noexpandtab nocin ai
