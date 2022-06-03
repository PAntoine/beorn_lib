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
#    file: dummy_scm
#    desc: Dummy SCM
#
#    This dummy SCM is used for testing.
#
#  author: peter
#    date: 29/08/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
from beorn_lib.scm import scm, SCM_BASE
from beorn_lib import SCMTree
from beorn_lib.source_tree import SourceTree

def checkForType(repository):
	""" Check For Type

		This function will check to see if the repository is a git repository. It
		will not check to see if it is valid, just that the path passed in points
		to something that could be a git repository.

		This check SPECIFICALLY does not validate a submodule, that is bad juju
		and causes all sorts of problems, you should always use the root repo or
		the real repo that is used for the submodule.
	"""
	result = False

	if os.path.isdir(repository) and os.path.isfile(os.path.join(repository, '.dmy')):
		result = True

	return result


class SCM_DUMMY(SCM_BASE):
	def __init__(self, repo_url, working_dir = None):
		self.branch = 'HEAD'
		self.change_list = []

		super(SCM_DUMMY, self).__init__(repo_url, working_dir)

	def all_nodes_function(self,last_visited_node, node,value,levels,direction, parameter):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = []

		if node.hasChild():
			item_type = 'dir'
		else:
			item_type = 'file'

		value.append(scm.SCMItem(item_type, node.getPath()))

		return (node, value, False)

	def mockModifiedItems(self, items):
		""" This will add updates to the SCM for the server files """
		self.change_list = items

	def getTreeChanges(self, from_version = None, to_version = None, path = None):
		return self.change_list

	def getTreeChangesGenerator(self):
		for item in self.change_list:
			yield item

	def __addNodes(self, node, node_list):
		for index, x in enumerate(node_list):
			name = "dir_item_" + str(index)
			new_node = SCMTree(name)
			node.addChildNode(new_node)

			if x != True:
				self.__addNodes(new_node, x)

	def buildSCMTree(self, structure):
		self.scm_tree = SCMTree('[base]', self)
		self.__addNodes(self.scm_tree, structure)

	def getSourceTree(self, version: str = None) -> SourceTree:
		""" This function will return the SCM contents as a SourceTree.  """
		# TODO: This needs to build the tree.
		#return self.scm_tree.walkTree(self.all_nodes_function)
		return SourceTree(self.getName())

	def aWalk(self, node):
		if node.hasChild():
			yield scm.SCMItem('dir', node.getPath())

			for item in node.getChildren():
				for a_item in self.aWalk(item):
					yield a_item
		else:
			yield scm.SCMItem('file', node.getPath())

	def getTreeListingGenerator(self):
		""" This function will return the directory listing for the given commit.  """
		for aa in self.scm_tree.getChildren():
			for item in self.aWalk(aa):
				yield item

	def getPath(self):
		""" Get Path

			Returns the path of the specific item.
		"""
		pass

scm.supported_scms.append(scm.SupportedSCM('dmy', checkForType, SCM_DUMMY))

# vim: ts=4 sw=4 noexpandtab nocin ai
