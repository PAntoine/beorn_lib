#!/usr/bin/env python
#---------------------------------------------------------------------------------
#    file: test
#    desc: This file holds the tests for the SCM class.
#
#  author: Peter Antoine
#    date: 28/07/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Import the external modules.
#---------------------------------------------------------------------------------
import os
import unittest
from beorn_lib.scm.scmgit import SCM_GIT
from beorn_lib.scm.scmbase import SCM_BASE
from test.utils.repo_builder import amendDiffArray, diff_set, writefile
from beorn_lib.scm import scm, SCMStatus
from scm_test import SCMTest

#---------------------------------------------------------------------------------
# Test Data
#---------------------------------------------------------------------------------
text_data_1 = [ "This test case will change a file in the repo.\n" ]

#---------------------------------------------------------------------------------
# Test Sequences.
#---------------------------------------------------------------------------------
class TestQuery(SCMTest):
	def __init__(self, testname = 'runTest',  scm_type = None, scm_dir = None, test_data = None):
		super(TestQuery, self).__init__(testname)

	def test_newSCM(self):
		""" New an SCM.

			This is a simple test that checks that the repository of the supported
			types can be correctly instantiated.
		"""
		if self.scm_type == 'Git':
			self.assertEqual('Git', scm.new("git@github.com:PAntoine/scm.git").getType())
			self.assertEqual('Git', scm.new("ssh://user@server/project.git").getType())
			self.assertEqual('Git', scm.new("git://user@server/project.git").getType())
			self.assertEqual('Git', scm.new("file:/local/project.git").getType())
		if self.scm_type == 'P4':
			pass
		else:
			self.assertTrue(False,"Unknown SCM:" + self.scm_type.upper())

		# know nonsense directory should failed
		(status, _) = scm.findRepositoryRoot('/fdfdfd/fdfdd/fdfdf/fdfdf/fdfdfd/dfdfd')
		self.assertFalse(status)


	def test_createSCM(self):
		""" Create an SCM.

			This is a simple test that checks that the repository of the supported
			types can be correctly instantiated.
		"""
		# positive test
		self.assertTrue(self.repo.__class__.__name__ == 'SCM_' + self.scm_type.upper())

		# negative test unsupported scm
		test_2 = scm.create("xxx")

		self.assertTrue(isinstance(test_2, SCM_BASE))

	def test_diretoryListing(self):
		""" Directory Listing Test.

			This tests that that the repo lists the files in the current repo.
		"""
		repo_listing = self.repo.getDirectoryListing(".")

		for entry in repo_listing:
			if entry[0] == 'file':
				self.assertTrue(os.path.isfile(self.directory + '/' + entry[1]))

			elif entry[0] == 'dir':
				self.assertTrue(os.path.isdir(self.directory + '/' + entry[1]))

	def test_setVersion(self):
		""" Test Set Branch

			This function will test the setting of the branch.
			It will set the repo to a known branch and then see if a known
			file exists in it. The do a negative test for a branch that
			does not exist.
		"""
		# Setting version not supported on P4
		if self.scm_type != 'P4':
			# negative test
			self.assertFalse(self.repo.setVersion("xxxxxxxxxxxx"))

			# negative test for a file in the repo
			self.assertTrue(self.repo.setVersion("branch_2"))
			self.assertTrue(self.repo.getFile("test_3") == [])

			# positive test
			self.assertTrue(self.repo.setVersion("branch_10"))
			self.assertFalse(self.repo.getFile("test_3") == [])

	def test_getBranches(self):
		""" Test Get Branches

			This will check that it gets a list of branches, it cannot actually
			test the list is correct as the branches may change.
		"""
		self.assertFalse(self.repo.getBranches() == [])

	def test_getBranch(self):
		""" Test Get Branch

			This will get the current branch.
		"""
		branch_list = self.repo.getBranches()
		branch = self.repo.getBranch()

		self.assertTrue(len(branch_list) > 0)

		if self.scm_type != 'P4':
			# is the branch in the branch_list of branches
			# P4 does not have a default
			for entry in branch_list[1]:
				if entry.name == branch:
					found = True

				self.assertTrue(found)

	def test_getFile(self):
		""" Get File

			This function will get the file from the repository, and test that
			getting the current header will match the same file returned via the
			specific commit id.
		"""
		specific_commit = None

		# TODO: why do I do this? Makes no difference with the P4 test.
		if self.scm_type != 'P4':
			self.assertTrue(self.repo.setVersion("branch_1"))

		current_branch = self.repo.getBranch()
		branch_list = self.repo.getBranches()

		for entry in branch_list[1]:
			if entry.name == current_branch:
				specific_commit = entry.commit_id
				break

		# get the same version of the file three different ways.
		default_file = self.repo.getFile("test_1")
		branch_file = self.repo.getFile("test_1", current_branch)

		if specific_commit is not None:
			commit_file = self.repo.getFile("test_1", specific_commit)
			self.assertTrue(default_file == commit_file)

		self.assertTrue(default_file == branch_file)

		# check that two versions are different
		history = self.repo.getHistory("test_1")

		self.assertTrue(len(history) > 1)
		history_file = self.repo.getFile("test_1", history[1][0])

		self.assertFalse(history_file != [] and default_file == history_file)

	def test_setgetVersion(self):
		""" Set and Get Version Tests.

			This tests simple test that the version can be set and returned.
		"""
		# version stuff not currently supported.
		if self.scm_type != 'P4':
			self.assertTrue(self.repo.getVersion() == 'HEAD' or self.repo.getVersion() == 'branch_0')
			self.assertFalse(self.repo.setVersion("xxxxxxxxxxxx"))
			self.assertTrue(self.repo.setVersion("branch_6"))
			self.assertTrue(self.repo.getVersion() == "branch_6")

	def test_getCurrentVersion(self):
		""" Get Current Version Test.

			Basic test to get the current version of the underlying repos.
			Can't really do a full test without knowing too much about the
			current state of the current repo.
		"""
		self.assertTrue(self.repo.getCurrentVersion() != '')

	def test_getHistory(self):
		""" Get History.

			This function tests that the getting of history works for
			files and commits that are known to exist.
		"""
		self.assertTrue(self.repo.getHistory() != [])
		self.assertTrue(self.repo.getHistory('test_2') != [])
		self.assertTrue(self.repo.getHistory('xxxxxxxxxx') == [])

		if self.scm_type != 'P4':
			# P4 returns full history if the version did not exist.
			self.assertTrue(self.repo.getHistory('test_1','5555555555') == [])

	def test_searchCommits(self):
		""" Search Commits.

			This function will test the fact that the function will return
			search strings for a string that is known to be in the repo.
		"""
		if self.scm_type != 'P4':
			self.assertTrue(self.repo.searchCommits('This test') != [])

	def test_checkObjectExists(self):
		""" Test Object Existence.

			This function will test to see if the known (and unknown) object
			exists within the repository.
		"""
		current_branch = self.repo.getBranch()
		(status, branch_list) = self.repo.getBranches()
		specific_commit = None

		self.assertTrue(len(branch_list) > 0)

		for entry in branch_list:
			if entry.name == current_branch:
				specific_commit = entry.commit_id
				break

		# positive test.
		self.assertTrue(self.repo.checkObjectExists("test_1"))
		self.assertTrue(self.repo.checkObjectExists("test_1", current_branch))

		if self.repo.getType() != 'P4':
			self.assertTrue(self.repo.checkObjectExists("test_1", specific_commit))

		# negative test
		self.assertFalse(self.repo.checkObjectExists("xxxxxxxxxxx"))
		self.assertFalse(self.repo.checkObjectExists("xxxxxxxxxxx", current_branch))
		if self.repo.getType() != 'P4':
			self.assertFalse(self.repo.checkObjectExists("xxxxxxxxxxx", specific_commit))

	def test_getTreeChanges(self):
		""" Get Tree Changes

			This function will test the tree changes. As we don't have a test
			repository to test these files against the current repo and the
			relative versions.
		"""
		if self.scm_type != 'P4':
			# make sure we are on a known branch
			self.assertTrue(self.repo.setVersion("branch_12"))

			# test no changes
			self.assertEqual([], self.repo.getTreeChanges())

			# Old revision to current top
			self.assertEqual([SCMStatus('A', 'test_2')],  self.repo.getTreeChanges(from_version = self.repo.generateRelativeReference('HEAD', -7)))

			# within the tree - no changes
			self.assertEqual([SCMStatus('M', 'test_1')], self.repo.getTreeChanges(	from_version = self.repo.generateRelativeReference('HEAD', -8),
																					to_version = 'HEAD~7'))
			self.assertEqual([SCMStatus('A', 'test_2')], self.repo.getTreeChanges(	from_version = self.repo.generateRelativeReference('HEAD', -7),
																					to_version = 'HEAD~6'))

			# modify existing file
			self.assertTrue(writefile(os.path.join(self.directory,'test_1'), text_data_1))
			self.assertEqual([SCMStatus('M', 'test_1')],  self.repo.getTreeChanges())

			self.assertEqual([SCMStatus('M', 'test_1'), SCMStatus('A', 'test_2')],  self.repo.getTreeChanges(
																								from_version = self.repo.generateRelativeReference('HEAD', -8)))

			# Add a new file
			self.assertTrue(writefile(os.path.join(self.directory, 'test_3'), text_data_1))
			self.assertEqual(set([SCMStatus('A', 'test_3'), SCMStatus('M', 'test_1')]),  set(self.repo.getTreeChanges()))
			self.assertEqual([SCMStatus('M', 'test_1'), SCMStatus('A', 'test_2'), SCMStatus('A', 'test_3')],
								self.repo.getTreeChanges(from_version = self.repo.generateRelativeReference('HEAD', -8)))

			# within the tree - with tree change
			self.assertEqual([SCMStatus('M', 'test_1')], self.repo.getTreeChanges(	from_version = self.repo.generateRelativeReference('HEAD', -8),
																			to_version = 'HEAD~7'))
			self.assertEqual([SCMStatus('A', 'test_2')], self.repo.getTreeChanges(	from_version = self.repo.generateRelativeReference('HEAD', -7),
																			to_version = 'HEAD~6'))


			self.repo.cleanRepository(True)


	def test_getDiffDetails(self):
		""" Get Diff Details

			This function will test the tree changes. As we don't have a test
			repository to test these files against the current repo and the
			relative versions.
		"""
		if self.scm_type == 'P4':
			diff = self.repo.getDiffDetails(from_version = '1', to_version = '3')
		else:
			self.assertTrue(self.repo.setVersion("branch_9"))

			# Check the first known diff - should be adding of a new file.
			diff = self.repo.getDiffDetails(from_version = self.repo.generateRelativeReference('branch_9', -3), to_version = 'branch_9')
			self.assertEqual(2, len(diff))
			self.assertEqual(1, len(diff[0].change_list))
			self.assertEqual(1, len(diff[1].change_list))

			diff = self.repo.getDiffDetails(from_version = self.repo.generateRelativeReference('branch_9', -3),
											to_version = self.repo.generateRelativeReference('branch_9', -2))
			self.assertEqual(1, len(diff))
			self.assertEqual(1, len(diff[0].change_list))

			diff = self.repo.getDiffDetails(from_version = self.repo.generateRelativeReference('branch_9', -2),
											to_version = self.repo.generateRelativeReference('branch_9', -1))
			self.assertEqual(2, len(diff))
			self.assertEqual(3, len(diff[0].change_list))
			self.assertEqual(1, len(diff[1].change_list))

			diff = self.repo.getDiffDetails(from_version = self.repo.generateRelativeReference('branch_9', -1), to_version = 'branch_9')
			self.assertEqual(1, len(diff))
			self.assertEqual(4, len(diff[0].change_list))

	def test_getTreeChangeDetails(self):
		""" Get Tree Changes Details

			This function will test the tree changes. We have a known number of changes on
			a specific branch and count that the branches are there.
		"""
		if self.scm_type != 'P4':
			diff = self.repo.getTreeChangeDetails(from_version = self.repo.generateRelativeReference('branch_9', -3), to_version = 'branch_9')
			self.assertEqual(3, len(diff))
			self.assertEqual(1, len(diff[0]))
			self.assertEqual(2, len(diff[1]))
			self.assertEqual(1, len(diff[2]))

# vim: ts=4 sw=4 noexpandtab nocin ai

