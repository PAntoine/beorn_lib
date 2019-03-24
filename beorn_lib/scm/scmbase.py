#!/bin/python
#---------------------------------------------------------------------------------
#         file: scmbase
#  description: This is the base class for the scm.
#
#       author: Peter Antoine
#         date: 21/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os

#---------------------------------------------------------------------------------
# base class (and default) SCM class
#---------------------------------------------------------------------------------
class SCM_BASE(object):

	def __init__(self, repo_url, working_dir = None):
		self.url = repo_url
		self.working_dir = working_dir
		self.version = ''

	MERGE_WORKING	= 0
	MERGE_THEIRS	= 1
	MERGE_OURS		= 2

	#---------------------------------------------------------------------------------
	# Functions that query the state of the repository
	#---------------------------------------------------------------------------------
	@staticmethod
	def findAllReposInTree(path):
		""" Find all repos in tree.

			This function will return two lists, one of the repos that are found in
			the tree and the second all the sub-repos (submodules, etc...).
		"""
		return ([], [])

	#---------------------------------------------------------------------------------
	# Functions that query the state of the repository
	#---------------------------------------------------------------------------------

	def getSCMVersion(self):
		return None

	def getType(self):
		return 'NONE'

	def getUrl(self):
		return self.url

	def getRoot(self):
		return self.url

	def getName(self):
		if self.url is not None:
			return os.path.splitext(os.path.basename(self.url))[0]
		elif self.working_dir is not None:
			return os.path.splitext(os.path.basename(self.working_dir))[0]
		else:
			return self.getType()

	def genrateRelativeReference(self, name, distance):
		""" Generate Relative Reference

			Different repositories have difference ways of referencing distance from
			a current reference. This function will normalise this.

			If it cannot generate the correct reference then it will return None.
		"""
		return None

	def setPath(self,path):
		""" set the new path of the repository object. """
		self.url = path

	def hasVersion(self,version):
		return False

	def setVersion(self,version):
		return False

	def getVersion(self):
		return ''

	def getFile(self, file_name, specific_commit = None):
		return []

	def getChangeList(self, specific_commit):
		""" This function will return a change list for the specified change """
		return None

	def getPatch(self, specific_commit = None):
		return []

	def hasFileChanged(self, file_name, specific_commit = None):
		return True

	def getDirectoryListing(self,directory_name):
		return []

	def getTreeListing(self):
		""" This function will return the directory listing for the given commit.  """
		return []

	def getTreeListingGenerator(self):
		""" This function will return the directory listing for the given commit.  """
		if False:
			yield None
		else:
			raise StopIteration

	def getBranch(self):
		return ''

	def getCurrentVersion(self):
		return ''

	def getHistory(self, filename=None, version=None, max_entries=None):
		return []

	def getCommitList(self):
		return []

	def getTreeChanges(self, from_version = None, to_version = None, path = None):
		return []

	def getTreeChangesGenerator(self):
		if False:
			yield None
		else:
			raise StopIteration

	def getDiffDetails(self, from_version = None, to_version = None, path = None):
		return []

	def getTreeChangeDetails(self, from_version = None, to_version = None, path = None):
		return []

	def getTags(self):
		return (-1, [])

	def getBranches(self):
		return (None, [])

	def searchCommits(self, search_string, selected_commits = []):
		return []

	def checkObjectExists(self, object_name, specific_commit = None):
		return False

	def isRepositoryClean(self):
		return False

	#---------------------------------------------------------------------------------
	# Functions that amend the state of the repository
	#---------------------------------------------------------------------------------

	def initialise(self, directory_path = None, bare = False):
		return False

	def addBranch(self, branch_name, branch_point = None):
		return False

	def resetChanges(self, amend_filesystem=False):
		return False

	def addCommit(self, files = None, empty = False, message = None):
		return False

	def addItem(self, item):
		return False

	def removeItem(self, item, leave_on_filesystem=True):
		return False

	def switchBranch(self, branch_name):
		return False

	def merge(self, merge_from, merge_to = None):
		return False

	def fixConflict(self, item, how = MERGE_WORKING):
		return False

	def sync(self, pull = True, push = False):
		return False

	def cleanRepository(self, deep_clean=False):
		pass
