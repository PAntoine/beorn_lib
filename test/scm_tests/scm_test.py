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

		cls.commit = [None] * 51
		cls.branch = [None] * 13

		# remove the old one
		if os.path.isdir(cls.directory):
			shutil.rmtree(cls.directory, ignore_errors=True)

		new_scm = scm.create(cls.scm_type, cls.url, cls.directory)

		if new_scm is None:
			print("Error: failed to create repo")
		else:
			if new_scm.initialise():
				result = True

				# add initial commit 0
				cls.branch[0] = new_scm.addBranch("branch_0")
				result &= writefile(os.path.join(cls.directory, 'test_1'), text_data_1)
				cls.commit[1] = new_scm.addCommit(files = [os.path.join(os.path.join(cls.directory, 'test_1'))], empty = True, message = 'commit_1')
				# branch the repo @ 1
				cls.branch[1] = new_scm.addBranch("branch_1", cls.commit[1])
				new_scm.switchBranch(cls.branch[1])
				result += writefile(os.path.join(cls.directory, 'test_1'), text_data_2)
				cls.commit[2] = new_scm.addCommit(files = [os.path.join(cls.directory, 'test_1')], empty = True, message = 'commit_2')
				result += writefile(os.path.join(cls.directory, 'test_2'), text_data_2)
				cls.commit[3] = new_scm.addCommit(files = [os.path.join(cls.directory, 'test_1'),os.path.join(cls.directory, 'test_2')], empty = True, message = 'commit_3')
				# second branch @ 1
				cls.branch[2] = new_scm.addBranch("branch_2", cls.commit[1])
				new_scm.switchBranch(cls.branch[2])
				cls.commit[4] = new_scm.addCommit(empty = True, message = 'commit_4')
				cls.commit[5] = new_scm.addCommit(empty = True, message = 'commit_5')
				cls.commit[6] = new_scm.addCommit(empty = True, message = 'commit_6')
				# branch @ 5
				cls.branch[3] = new_scm.addBranch("branch_3", cls.commit[5])
				new_scm.switchBranch(cls.branch[3])
				cls.commit[7] = new_scm.addCommit(empty = True, message = 'commit_7')
				cls.commit[8] = new_scm.addCommit(empty = True, message = 'commit_8')
				# back to branch 2 - add to the end of commit 6
				cls.commit[9] = new_scm.addCommit(empty = True, message = 'commit_9')
				# merge the two branches
				cls.commit[10] = new_scm.merge(cls.branch[3], cls.branch[2])
				cls.commit[11] = new_scm.addCommit(empty = True, message = 'commit_11')
				# go back to the main branch and add some commits.
				cls.commit[12] = new_scm.addCommit(empty = True, message = 'commit_12')
				cls.commit[13] = new_scm.addCommit(empty = True, message = 'commit_13')
				cls.commit[14] = new_scm.addCommit(empty = True, message = 'commit_14')
				cls.commit[15] = new_scm.merge(cls.branch[2], cls.branch[0])
				cls.commit[16] = new_scm.addCommit(empty = True, message = 'commit_16')
				# Ok, let's branch off commit 2
				cls.branch[4] = new_scm.addBranch("branch_4", cls.commit[2])
				new_scm.switchBranch(cls.branch[4])
				cls.commit[17] = new_scm.addCommit(empty = True, message = 'commit_17')
				cls.commit[18] = new_scm.addCommit(empty = True, message = 'commit_18')
				cls.commit[19] = new_scm.addCommit(empty = True, message = 'commit_19')
				cls.commit[20] = new_scm.addCommit(empty = True, message = 'commit_20')
				cls.commit[21] = new_scm.addCommit(empty = True, message = 'commit_21')
				# Ok. switch back to branch 1
				cls.commit[22] = new_scm.addCommit(empty = True, message = 'commit_22')
				# Ok, another branch
				cls.branch[5] = new_scm.addBranch("branch_5", cls.commit[3])
				new_scm.switchBranch(cls.branch[5])
				cls.commit[23] = new_scm.addCommit(empty = True, message = 'commit_23')
				cls.commit[24] = new_scm.addCommit(empty = True, message = 'commit_24')
				cls.commit[25] = new_scm.addCommit(empty = True, message = 'commit_25')
				# merge
				cls.commit[26] = new_scm.merge(cls.branch[5],cls.branch[1])
				# new branch
				cls.branch[6] = new_scm.addBranch("branch_6", cls.commit[24])
				new_scm.switchBranch(cls.branch[6])
				cls.commit[27] = new_scm.addCommit(empty = True, message = 'commit_27')
				cls.commit[28] = new_scm.addCommit(empty = True, message = 'commit_28')
				# add a new commit to the merge of b5 and b1
				cls.commit[29] = new_scm.addCommit(empty = True, message = 'commit_29')
				# add new branch
				cls.branch[7] = new_scm.addBranch("branch_7", cls.commit[29])
				new_scm.switchBranch(cls.branch[7])
				cls.commit[30] = new_scm.addCommit(empty = True, message = 'commit_30')
				# merge
				cls.commit[31] = new_scm.merge(cls.branch[6],cls.branch[1])
				# one more new branch - use switch_to_branch
				cls.branch[8] = new_scm.addBranch("branch_8", cls.commit[23], True)
				cls.commit[32] = new_scm.addCommit(empty = True, message = 'commit_31')
				cls.commit[33] = new_scm.addCommit(empty = True, message = 'commit_32')
				# now do a tripe merge
				new_scm.merge(cls.branch[7],cls.branch[1])
				cls.commit[34] = new_scm.merge(cls.branch[8],cls.branch[1])
				# now merge that
				cls.commit[35] = new_scm.merge(cls.branch[4],cls.branch[1])
				# one more merge
				cls.commit[36] = new_scm.merge(cls.branch[1],cls.branch[0])
				cls.commit[37] = new_scm.addCommit(empty = True, message = 'commit_37')
				cls.commit[38] = new_scm.addCommit(empty = True, message = 'commit_38')

				# now add some hanging branches
				# this will also be the branch where the diff tests are done.
				cls.branch[9] = new_scm.addBranch("branch_9", cls.commit[8])
				new_scm.switchBranch(cls.branch[9])
				contents = []
				result += writefile(os.path.join(cls.directory, 'diff_file'), amendDiffArray(contents, diff_set[0][0], diff_set[0][1]))
				cls.commit[39] = new_scm.addCommit(files = [os.path.join(cls.directory, 'diff_file')], empty = False, message = 'commit_39')
				result += writefile(os.path.join(cls.directory, 'diff_file'), amendDiffArray(contents, diff_set[1][0], diff_set[1][1]))
				result += writefile(os.path.join(cls.directory, 'test_5'), text_data_2)
				cls.commit[40] = new_scm.addCommit(files = [os.path.join(cls.directory, 'diff_file'), os.path.join(cls.directory, 'test_5')], empty = False, message = ['commit_40', '', 'this is a multi-line commit message','this will test stuff'])
				result += writefile(os.path.join(cls.directory, 'diff_file'), amendDiffArray(contents, diff_set[2][0], diff_set[2][1]))
				cls.commit[41] = new_scm.addCommit(files = [os.path.join(cls.directory, 'diff_file')], empty = False, message = 'commit_41')

				# and another
				cls.branch[10] = new_scm.addBranch("branch_10", cls.commit[15])
				new_scm.switchBranch(cls.branch[10])
				# add a new file
				result += writefile(new_scm.generateFileName('test_3'), text_data_2)
				cls.commit[42] = new_scm.addCommit(files = [os.path.join(cls.directory, 'test_3')], empty = True, message = 'commit_42')
				cls.commit[43] = new_scm.addCommit(empty = True, message = 'commit_43')
				cls.commit[44] = new_scm.addCommit(empty = True, message = 'commit_44')
				# and one more
				cls.branch[11] = new_scm.addBranch("branch_11", cls.commit[20])
				new_scm.switchBranch(cls.branch[11])
				cls.commit[45] = new_scm.addCommit(empty = True, message = 'commit_45')
				cls.commit[46] = new_scm.addCommit(empty = True, message = 'commit_46')
				cls.commit[47] = new_scm.addCommit(empty = True, message = 'commit_47')
				# and finally
				cls.branch[12] = new_scm.addBranch("branch_12", cls.commit[26])
				new_scm.switchBranch(cls.branch[12])
				cls.commit[48] = new_scm.addCommit(empty = True, message = 'commit_48')
				cls.commit[49] = new_scm.addCommit(empty = True, message = 'commit_49')
				cls.commit[50] = new_scm.addCommit(empty = True, message = 'commit_50')


	def setUp(self):
		self.repo = scm.new(self.directory, self.url)
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
