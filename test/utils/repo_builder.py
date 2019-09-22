#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#    file: repo_builder
#    desc: This will simply build a repository for testing.
#
#  author: Peter Antoine
#    date: 25/05/2015
#---------------------------------------------------------------------------------
#                     Copyright (c) 2015 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import shutil
import beorn_lib.scm as scm

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

def amendDiffArray(contents, change_list, fill_char):
	""" Write Diff File

		This function will write a file that contains the contents that
		is specified by the given change list. This is intended to make a
		file that the changes are known and will produce testable diffs.
	"""
	for (start, number) in change_list:
		contents[start : start + number] = [fill_char*80 + '\n']*number

	return contents

def writefile(filename, contents):
	""" Write File

		This function will write, and if it does not exist create the
		given file. It will fill the file with the content array.
	"""
	result = True
	try:
		outfile = open(filename,'w')
		outfile.writelines(contents)
		outfile.flush()
		outfile.close()

	except IOError, e:
		result = False

	return result

def buildRepo(self):
	""" Test Build SCM

		This test case will build the scm for the given parameters.
		It is the base test for the query tests as this will create a
		known a predicable SCM that can be queried and the code tested
		against.
	"""

	# remove the old one
	if os.path.isdir(self.repo_dir):
		shutil.rmtree(self.repo_dir, ignore_errors=True)

	# create repository
	new_scm = scm.create(self.scm_type, self.repo_dir, self.repo_dir)
	self.assertIsNotNone(new_scm)
	self.assertTrue(new_scm.initialise())

	# add initial commit 0
	branch_0 = new_scm.addBranch("branch_0")
	self.assertIsNotNone(branch_0)

	self.assertTrue(writefile(os.path.join(self.repo_dir, 'test_1'), text_data_1))

	commit_1 = new_scm.addCommit(files = ['test_1'], empty = True, message = 'commit_1')
	self.assertIsNotNone(commit_1)

	# branch the repo @ 1
	branch_1 = new_scm.addBranch("branch_1", commit_1)
	self.assertIsNotNone(branch_1)
	self.assertTrue(writefile(os.path.join(self.repo_dir, 'test_1'), text_data_2))

	commit_2 = new_scm.addCommit(files = ['test_1'], empty = True, message = 'commit_2')
	self.assertIsNotNone(commit_2)

	self.assertTrue(writefile(os.path.join(self.repo_dir, 'test_2'), text_data_2))
	commit_3 = new_scm.addCommit(files = ['test_1','test_2'], empty = True, message = 'commit_3')
	self.assertIsNotNone(commit_3)

	# second branch @ 1
	branch_2 = new_scm.addBranch("branch_2", commit_1)
	self.assertIsNotNone(branch_2)

	commit_4 = new_scm.addCommit(empty = True, message = 'commit_4')
	self.assertIsNotNone(commit_4)

	commit_5 = new_scm.addCommit(empty = True, message = 'commit_5')
	self.assertIsNotNone(commit_5)

	commit_6 = new_scm.addCommit(empty = True, message = 'commit_6')
	self.assertIsNotNone(commit_6)

	# branch @ 5
	branch_3 = new_scm.addBranch("branch_3", commit_5)
	self.assertIsNotNone(branch_3)

	commit_7 = new_scm.addCommit(empty = True, message = 'commit_7')
	self.assertIsNotNone(commit_7)

	commit_8 = new_scm.addCommit(empty = True, message = 'commit_8')
	self.assertIsNotNone(commit_8)

	# back to branch 2 - add to the end of commit 6
	self.assertIsNotNone(new_scm.switchBranch("branch_2"))
	commit_9 = new_scm.addCommit(empty = True, message = 'commit_9')
	self.assertIsNotNone(commit_9)

	# merge the two branches
	commit_10 = new_scm.merge("branch_3", "branch_2")
	self.assertIsNotNone(commit_10)

	commit_11 = new_scm.addCommit(empty = True, message = 'commit_11')
	self.assertIsNotNone(commit_11)

	# go back to the main branch and add some commits.
	self.assertIsNotNone(new_scm.switchBranch("branch_0"))
	commit_12 = new_scm.addCommit(empty = True, message = 'commit_12')
	self.assertIsNotNone(commit_12)

	commit_13 = new_scm.addCommit(empty = True, message = 'commit_13')
	self.assertIsNotNone(commit_13)

	commit_14 = new_scm.addCommit(empty = True, message = 'commit_14')
	self.assertIsNotNone(commit_14)

	commit_15 = new_scm.merge("branch_2", "branch_0")
	self.assertIsNotNone(commit_15)

	commit_16 = new_scm.addCommit(empty = True, message = 'commit_16')
	self.assertIsNotNone(commit_16)

	# Ok, let's branch off commit 2
	branch_4 = new_scm.addBranch("branch_4", commit_2)
	self.assertIsNotNone(branch_4)

	commit_17 = new_scm.addCommit(empty = True, message = 'commit_17')
	self.assertIsNotNone(commit_17)

	commit_18 = new_scm.addCommit(empty = True, message = 'commit_18')
	self.assertIsNotNone(commit_18)

	commit_19 = new_scm.addCommit(empty = True, message = 'commit_19')
	self.assertIsNotNone(commit_19)

	commit_20 = new_scm.addCommit(empty = True, message = 'commit_20')
	self.assertIsNotNone(commit_20)

	commit_21 = new_scm.addCommit(empty = True, message = 'commit_21')
	self.assertIsNotNone(commit_21)

	# Ok. switch back to branch 1
	self.assertIsNotNone(new_scm.switchBranch("branch_1"))
	commit_22 = new_scm.addCommit(empty = True, message = 'commit_22')
	self.assertIsNotNone(commit_22)

	# Ok, another branch
	branch_5 = new_scm.addBranch("branch_5", commit_3)
	self.assertIsNotNone(branch_5)

	commit_23 = new_scm.addCommit(empty = True, message = 'commit_23')
	self.assertIsNotNone(commit_23)

	commit_24 = new_scm.addCommit(empty = True, message = 'commit_24')
	self.assertIsNotNone(commit_24)

	commit_25 = new_scm.addCommit(empty = True, message = 'commit_25')
	self.assertIsNotNone(commit_25)

	# merge
	commit_26 = new_scm.merge("branch_5","branch_1")
	self.assertIsNotNone(commit_26)

	# new branch
	branch_6 = new_scm.addBranch("branch_6", commit_24)
	self.assertIsNotNone(branch_6)

	commit_27 = new_scm.addCommit(empty = True, message = 'commit_27')
	self.assertIsNotNone(commit_27)

	commit_28 = new_scm.addCommit(empty = True, message = 'commit_28')
	self.assertIsNotNone(commit_28)

	# add a new commit to the merge of b5 and b1
	self.assertIsNotNone(new_scm.switchBranch("branch_1"))
	commit_29 = new_scm.addCommit(empty = True, message = 'commit_29')
	self.assertIsNotNone(commit_29)

	# add new branch
	branch_7 = new_scm.addBranch("branch_7", commit_29)
	self.assertIsNotNone(branch_7)

	commit_30 = new_scm.addCommit(empty = True, message = 'commit_30')
	self.assertIsNotNone(commit_30)

	# merge
	commit_31 = new_scm.merge("branch_6","branch_1")
	self.assertIsNotNone(commit_31)

	# one more new branch
	branch_8 = new_scm.addBranch("branch_8", commit_23)
	self.assertIsNotNone(branch_8)

	commit_32 = new_scm.addCommit(empty = True, message = 'commit_31')
	self.assertIsNotNone(commit_32)

	commit_33 = new_scm.addCommit(empty = True, message = 'commit_32')
	self.assertIsNotNone(commit_33)

	# now do a tripe merge
	new_scm.merge("branch_7","branch_1")
	commit_34 = new_scm.merge("branch_8","branch_1")
	self.assertIsNotNone(commit_34)

	# now merge that
	commit_35 = new_scm.merge("branch_4","branch_1")
	self.assertIsNotNone(commit_35)

	# one more merge
	commit_36 = new_scm.merge("branch_1","branch_0")
	self.assertIsNotNone(commit_36)

	commit_37 = new_scm.addCommit(empty = True, message = 'commit_37')
	self.assertIsNotNone(commit_37)

	commit_38 = new_scm.addCommit(empty = True, message = 'commit_38')
	self.assertIsNotNone(commit_38)

	# now add some hanging branches
	# this will also be the branch where the diff tests are done.
	branch_9 = new_scm.addBranch("branch_9", commit_8)
	self.assertIsNotNone(branch_9)

	contents = []
	self.assertTrue(writefile(os.path.join(self.repo_dir, 'diff_file'), amendDiffArray(contents, diff_set[0][0], diff_set[0][1])))
	commit_39 = new_scm.addCommit(files = ['diff_file'], empty = False, message = 'commit_39')
	self.assertIsNotNone(commit_39)

	self.assertTrue(writefile(os.path.join(self.repo_dir, 'diff_file'), amendDiffArray(contents, diff_set[1][0], diff_set[1][1])))
	self.assertTrue(writefile(os.path.join(self.repo_dir, 'test_5'), text_data_2))
	commit_40 = new_scm.addCommit(files = ['diff_file', 'test_5'], empty = False, message = ['commit_40', '', 'this is a multi-line commit message','this will test stuff'])
	self.assertIsNotNone(commit_40)

	self.assertTrue(writefile(os.path.join(self.repo_dir, 'diff_file'), amendDiffArray(contents, diff_set[2][0], diff_set[2][1])))
	commit_41 = new_scm.addCommit(files = ['diff_file'], empty = False, message = 'commit_41')
	self.assertIsNotNone(commit_41)

	# and another
	branch_10 = new_scm.addBranch("branch_10", commit_15)
	self.assertIsNotNone(branch_10)

	# add a new file
	self.assertTrue(writefile(os.path.join(self.repo_dir, 'test_3'), text_data_2))

	commit_42 = new_scm.addCommit(files = ['test_3'], empty = True, message = 'commit_42')
	self.assertIsNotNone(commit_42)

	commit_43 = new_scm.addCommit(empty = True, message = 'commit_43')
	self.assertIsNotNone(commit_43)

	commit_44 = new_scm.addCommit(empty = True, message = 'commit_44')
	self.assertIsNotNone(commit_44)

	# and one more
	branch_11 = new_scm.addBranch("branch_11", commit_20)
	self.assertIsNotNone(branch_11)

	commit_45 = new_scm.addCommit(empty = True, message = 'commit_45')
	self.assertIsNotNone(commit_45)

	commit_46 = new_scm.addCommit(empty = True, message = 'commit_46')
	self.assertIsNotNone(commit_46)

	commit_47 = new_scm.addCommit(empty = True, message = 'commit_47')
	self.assertIsNotNone(commit_47)

	# and finally
	branch_12 = new_scm.addBranch("branch_12", commit_26)
	self.assertIsNotNone(branch_12)

	commit_48 = new_scm.addCommit(empty = True, message = 'commit_48')
	self.assertIsNotNone(commit_48)

	commit_49 = new_scm.addCommit(empty = True, message = 'commit_49')
	self.assertIsNotNone(commit_49)

	commit_50 = new_scm.addCommit(empty = True, message = 'commit_50')
	self.assertIsNotNone(commit_50)

	return new_scm

def removeRepo(self):
	""" Remove the Repository

		This function simple will remove the repository.
	"""
	# remove the old one
	if os.path.isdir(self.repo_dir):
		shutil.rmtree(self.repo_dir, ignore_errors=True)


# vim: ts=4 sw=4 noexpandtab nocin ai
