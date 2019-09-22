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
#    file: scm_test
#    desc: Base Test Class for SCM Tests.
#
#  author: peter
#    date: 04/06/2019
#---------------------------------------------------------------------------------
#                     Copyright (c) 2019 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Import the external modules.
#---------------------------------------------------------------------------------
import os
import stat
import shutil
import unittest
import beorn_lib.scm as scm
from test.utils.repo_builder import writefile, amendDiffArray

#---------------------------------------------------------------------------------
# Test Data
#---------------------------------------------------------------------------------
text_data_1 = [ "This test case will build the scm for the given parameters.\n",
				"It is the base test for the query tests as this will create a \n",
				"known a predicable SCM that can be queried and the code tested \n",
				"against.\n" ]

text_data_2 = [ "This test case will build the scm for the given parameters.\n",
				"It is the base test for the query tests as this will create a \n",
				"This function will get the file from the repository, and test that\n",
				"getting the current header will match the same file returned via the\n",
				"specific commit id.\n",
				"known a predicable SCM that can be queried and the code tested \n",
				"against.\n" ]

diff_set = [([(0, 100)], 'a'),
			([(10, 10), (30, 20), (70, 20)], 'b'),
			([(5, 10), (35, 10), (75, 20), (99, 30)], 'c')]

#---------------------------------------------------------------------------------
# Test Sequences.
#---------------------------------------------------------------------------------
class SCMTest(unittest.TestCase):
	def __init__(self, testname = 'runTest',  scm_type = None, scm_dir = None, test_data = None):
		# initialise the test framework
		super(SCMTest, self).__init__(testname)

	@classmethod
	def setParameters(cls, directory, test_data_dir, scm_type):
		cls.directory = os.path.join(directory, scm_type)
		cls.server_directory = os.path.join(directory, "server_" + scm_type)
		cls.test_data_dir = test_data_dir
		cls.scm_type = scm_type
		cls.url = None

	@classmethod
	def setUpClass(cls):
		super(SCMTest, cls).setUpClass()

		cls.url = scm.startLocalServer(cls.scm_type, cls.server_directory)

		# remove the old one
		if os.path.isdir(cls.directory):
			shutil.rmtree(cls.directory, ignore_errors=True)

		new_scm = scm.create(cls.scm_type, cls.url, cls.directory)

		if new_scm is None:
			print "Error: failed to create repo"
		else:
			if new_scm.initialise():
				result = True

				# add initial commit 0
				branch_0 = new_scm.addBranch("branch_0")
				result &= writefile(os.path.join(cls.directory, 'test_1'), text_data_1)
				print result, os.path.join(cls.directory, 'test_1')
				print os.path.exists(os.path.join(cls.directory, 'test_1'))
				commit_1 = new_scm.addCommit(files = [os.path.join(os.path.join(cls.directory, 'test_1'))], empty = True, message = 'commit_1')
				# branch the repo @ 1
				branch_1 = new_scm.addBranch("branch_1", commit_1)
				new_scm.switchBranch(branch_1)
				result += writefile(os.path.join(cls.directory, 'test_1'), text_data_2)
				commit_2 = new_scm.addCommit(files = [os.path.join(cls.directory, 'test_1')], empty = True, message = 'commit_2')
				result += writefile(os.path.join(cls.directory, 'test_2'), text_data_2)
				commit_3 = new_scm.addCommit(files = [os.path.join(cls.directory, 'test_1'),os.path.join(cls.directory, 'test_2')], empty = True, message = 'commit_3')
				# second branch @ 1
				branch_2 = new_scm.addBranch("branch_2", commit_1)
				new_scm.switchBranch(branch_2)
				commit_4 = new_scm.addCommit(empty = True, message = 'commit_4')
				commit_5 = new_scm.addCommit(empty = True, message = 'commit_5')
				commit_6 = new_scm.addCommit(empty = True, message = 'commit_6')
				# branch @ 5
				branch_3 = new_scm.addBranch("branch_3", commit_5)
				new_scm.switchBranch(branch_3)
				commit_7 = new_scm.addCommit(empty = True, message = 'commit_7')
				commit_8 = new_scm.addCommit(empty = True, message = 'commit_8')
				# back to branch 2 - add to the end of commit 6
				commit_9 = new_scm.addCommit(empty = True, message = 'commit_9')
				# merge the two branches
				commit_10 = new_scm.merge(branch_3, branch_2)
				commit_11 = new_scm.addCommit(empty = True, message = 'commit_11')
				# go back to the main branch and add some commits.
				commit_12 = new_scm.addCommit(empty = True, message = 'commit_12')
				commit_13 = new_scm.addCommit(empty = True, message = 'commit_13')
				commit_14 = new_scm.addCommit(empty = True, message = 'commit_14')
				commit_15 = new_scm.merge(branch_2, branch_0)
				commit_16 = new_scm.addCommit(empty = True, message = 'commit_16')
				# Ok, let's branch off commit 2
				branch_4 = new_scm.addBranch("branch_4", commit_2)
				new_scm.switchBranch(branch_4)
				commit_17 = new_scm.addCommit(empty = True, message = 'commit_17')
				commit_18 = new_scm.addCommit(empty = True, message = 'commit_18')
				commit_19 = new_scm.addCommit(empty = True, message = 'commit_19')
				commit_20 = new_scm.addCommit(empty = True, message = 'commit_20')
				commit_21 = new_scm.addCommit(empty = True, message = 'commit_21')
				# Ok. switch back to branch 1
				commit_22 = new_scm.addCommit(empty = True, message = 'commit_22')
				# Ok, another branch
				branch_5 = new_scm.addBranch("branch_5", commit_3)
				new_scm.switchBranch(branch_5)
				commit_23 = new_scm.addCommit(empty = True, message = 'commit_23')
				commit_24 = new_scm.addCommit(empty = True, message = 'commit_24')
				commit_25 = new_scm.addCommit(empty = True, message = 'commit_25')
				# merge
				commit_26 = new_scm.merge(branch_5,branch_1)
				# new branch
				branch_6 = new_scm.addBranch("branch_6", commit_24)
				new_scm.switchBranch(branch_6)
				commit_27 = new_scm.addCommit(empty = True, message = 'commit_27')
				commit_28 = new_scm.addCommit(empty = True, message = 'commit_28')
				# add a new commit to the merge of b5 and b1
				commit_29 = new_scm.addCommit(empty = True, message = 'commit_29')
				# add new branch
				branch_7 = new_scm.addBranch("branch_7", commit_29)
				new_scm.switchBranch(branch_7)
				commit_30 = new_scm.addCommit(empty = True, message = 'commit_30')
				# merge
				commit_31 = new_scm.merge(branch_6,branch_1)
				# one more new branch - use switch_to_branch
				branch_8 = new_scm.addBranch("branch_8", commit_23, True)
				commit_32 = new_scm.addCommit(empty = True, message = 'commit_31')
				commit_33 = new_scm.addCommit(empty = True, message = 'commit_32')
				# now do a tripe merge
				new_scm.merge(branch_7,branch_1)
				commit_34 = new_scm.merge(branch_8,branch_1)
				# now merge that
				commit_35 = new_scm.merge(branch_4,branch_1)
				# one more merge
				commit_36 = new_scm.merge(branch_1,branch_0)
				commit_37 = new_scm.addCommit(empty = True, message = 'commit_37')
				commit_38 = new_scm.addCommit(empty = True, message = 'commit_38')

				# now add some hanging branches
				# this will also be the branch where the diff tests are done.
				branch_9 = new_scm.addBranch("branch_9", commit_8)
				new_scm.switchBranch(branch_9)
				contents = []
				result += writefile(os.path.join(cls.directory, 'diff_file'), amendDiffArray(contents, diff_set[0][0], diff_set[0][1]))
				commit_39 = new_scm.addCommit(files = [os.path.join(cls.directory, 'diff_file')], empty = False, message = 'commit_39')
				result += writefile(os.path.join(cls.directory, 'diff_file'), amendDiffArray(contents, diff_set[1][0], diff_set[1][1]))
				result += writefile(os.path.join(cls.directory, 'test_5'), text_data_2)
				commit_40 = new_scm.addCommit(files = [os.path.join(cls.directory, 'diff_file'), os.path.join(cls.directory, 'test_5')], empty = False, message = ['commit_40', '', 'this is a multi-line commit message','this will test stuff'])
				result += writefile(os.path.join(cls.directory, 'diff_file'), amendDiffArray(contents, diff_set[2][0], diff_set[2][1]))
				commit_41 = new_scm.addCommit(files = [os.path.join(cls.directory, 'diff_file')], empty = False, message = 'commit_41')

				# and another
				branch_10 = new_scm.addBranch("branch_10", commit_15)
				new_scm.switchBranch(branch_10)
				# add a new file
				result += writefile(new_scm.generateFileName('test_3'), text_data_2)
				commit_42 = new_scm.addCommit(files = [os.path.join(cls.directory, 'test_3')], empty = True, message = 'commit_42')
				commit_43 = new_scm.addCommit(empty = True, message = 'commit_43')
				commit_44 = new_scm.addCommit(empty = True, message = 'commit_44')
				# and one more
				branch_11 = new_scm.addBranch("branch_11", commit_20)
				new_scm.switchBranch(branch_11)
				commit_45 = new_scm.addCommit(empty = True, message = 'commit_45')
				commit_46 = new_scm.addCommit(empty = True, message = 'commit_46')
				commit_47 = new_scm.addCommit(empty = True, message = 'commit_47')
				# and finally
				branch_12 = new_scm.addBranch("branch_12", commit_26)
				new_scm.switchBranch(branch_12)
				commit_48 = new_scm.addCommit(empty = True, message = 'commit_48')
				commit_49 = new_scm.addCommit(empty = True, message = 'commit_49')
				commit_50 = new_scm.addCommit(empty = True, message = 'commit_50')

	def setUp(self):
		self.repo = scm.new(self.directory, self.url)
		print self.directory, self.repo
		self.repo.switchBranch(name='branch_0')
		self.repo.cleanRepository(deep_clean = True)

	@classmethod
	def tearDownClass(cls):
		""" Remove the Repository

			This function simple will remove the repository.
		"""
		scm.stopLocalServer(cls.scm_type)

		# remove the old one
		if os.path.isdir(cls.directory):
			for root, dirs, files in os.walk(cls.directory, topdown=False):
				for name in files:
					os.chmod(os.path.join(root, name), stat.S_IRWXU)
				for name in dirs:
					os.chmod(os.path.join(root, name), stat.S_IRWXU)

			shutil.rmtree(cls.directory, ignore_errors=True)


# vim: ts=4 sw=4 noexpandtab nocin ai
