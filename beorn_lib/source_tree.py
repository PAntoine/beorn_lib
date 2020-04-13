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
#    file: source_tree
#    desc: Source Tree Item.
#
#  author: peter
#    date: 17/10/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
from beorn_lib.utilities import Utilities
from beorn_lib.nested_tree import NestedTreeNode

class SourceTree(NestedTreeNode):
	# class properties
	suffix_filter = []
	directory_filter = []

	@classmethod
	def setSuffixFilter(cls, suffix_filter):
		cls.suffix_filter = suffix_filter

	@classmethod
	def setDirectoryFilter(cls, directory_filter):
		cls.directory_filter = directory_filter

	@classmethod
	def getSuffixFilter(cls):
		return cls.suffix_filter

	@classmethod
	def getDirectoryFilter(cls):
		return cls.directory_filter

	def __init__(self, name, root=None):
		self.name = name
		if root is not None:
			self.root = os.path.realpath(root)
			self.is_dir = True
		else:
			self.root = None
			self.is_dir = False

		self.scm  = None
		self.on_filesystem = False
		self.flag = None
		self.submodule = False

		# state of the item.
		self.item_state = {}

		super(SourceTree, self).__init__(name, None)

	def copy(self, new_node):
		super(SourceTree, self).copy(new_node)

		self.name = new_node.name
		self.root = new_node.root
		self.scm = new_node.scm
		self.is_dir = new_node.is_dir
		self.on_filesystem = new_node.on_filesystem
		self.flag = new_node.flag
		self.submodule = new_node.submodule
		self.item_state = new_node.item_state

	def __lt__(self, other):
		if type(other) is SourceTree:
			return self.name < other.name
		return NotImplemented

	def __contains__(self, other):
		""" Contains

			Will return True if 'other' is the name of one of the children.
		"""
		if type(other) == str or type(other) == unicode:
			find_name = other
		elif isinstance(other, SourceTree):
			find_name = other.name
		else:
			return False

		for child in self.getChildren():
			if find_name == child.name:
				return True
		else:
			return False

	def getName(self):
		return self.name

	def findChild(self, other):
		if type(other) == str or type(other) == unicode:
			find_name = other
		elif isinstance(other, SourceTree):
			find_name = other.name
		else:
			return None

		for child in self.getChildren():
			if find_name == child.name:
				return child
		else:
			return None

	def isDir(self):
		return self.is_dir

	def isLink(self):
		# TODO: implement this!!
		return False

	def rebaseTree(self, new_path):
		""" Rebase the Tree.

			It will only rebase the tree towards the root (that is to make usage easier).
			It will copy all the children of the tree to the new root. It will also create
			all the nodes between the new root and the current.
		"""
		result = self
		current_path = self.getPath()

		if new_path != current_path and Utilities.isChildDirectory(current_path, new_path):

			meh = os.path.relpath(current_path, new_path)
			result = SourceTree(os.path.basename(new_path), os.path.realpath(new_path))

			# add the route between the new root and the old.
			add_stuff = result.addTreeNodeByPath(meh)
			add_stuff.addChildNode(self)

		return result

	def isOnFilesystem(self):
		return self.on_filesystem

	def updateItemState(self, name, state):
		self.item_state[name] = state

		# We have been changed, so all parents have to be modified.
		self.setFlag('M')

	def removeItemState(self, name):
		if name in self.item_state:
			del self.item_state[name]

		# TODO: need to update the tree start, that would need
		#		a proper tree walk. Need to walk up and then
		#		test all children. If there are no items with
		#		states, then would have to walk to the next
		#		parent and test there children, looking for
		#		a change. If those children don't have changes
		#		then remove and move up.

	def hasState(self):
		return self.item_state != {}

	def state(self):
		for scm_type in self.item_state:
			yield (scm_type, self.item_state[scm_type])

	def getState(self, scm_name=None):
		result = None

		if scm_name is not None:
			if scm_name in self.item_state:
				result = self.item_state[scm_name]
		else:
			result = self.item_state

		return result

	def setFlag(self, flag):
		self.flag = flag

		current = self.getParent()

		while current is not None:
			if current.flag is None or current.flag < flag:
				current.flag = flag

				current = current.getParent()
			else:
				break

	def clearFlag(self):
		self.flag = None

		current = self.getParent()

		while current is not None:
			if current.flag is not None:
				current.flag = None

				current = current.getParent()
			else:
				break

	def getFlag(self):
		return self.flag

	def setSCM(self, scm, submodule=False):
		""" Set SCM

			If this item in the tree points to an SCM then this
			function should be called with a reference to the
			scm. The reference is application specific.
		"""
		self.scm = scm
		self.submodule = submodule

	def isSCM(self):
		""" IsSCM is this item an scm reference """
		return self.scm is not None

	def isSubmodule(self):
		""" If the submodule flag is set """
		return self.scm is not None and self.submodule

	def getSCM(self):
		""" return the scm that has (or has not) been set on the item """
		return self.scm

	def findSCM(self):
		if self.scm is not None:
			return self.scm
		else:
			parent = self.getParent()

			while parent is not None:
				if parent.getSCM() is not None:
					return parent.getSCM()
				else:
					parent = parent.getParent()
			return None

	def getChilden(self):
		""" TODO """
		current = self.child_node

		while current is not None:
			yield current
			current = current.next_node

	def getPath(self, full=False):
		""" Get Path

			Returns the path of the specific item.
		"""
		if self.root is not None:
			result = self.root
		else:
			result = self.name

			current = self.parent_node

			while current is not None:
				if current.root is not None:
					if full:
						result = os.path.join(current.root, result)
					else:
						result = os.path.join(current.name, result)
					break
				else:
					result = os.path.join(current.name, result)
					current = current.parent_node

		return result

	def replace(self, new_node):
		""" Copy the Node to the new object.

			This function will replace the node. Be careful as it is
			essentially doing a shallow copy so all the child nodes will
			not be duplicated and be will shared by the old node.

			The children of this item need to be re-parented. So this
			will make the tree inconsistent if both nodes are used. So
			the node that is being replaced should be discarded.

			The point of this function is too allow for a nodes class
			type to be changed without breaking the tree.
		"""
		# replace in the list
		if self.next_node is not None:
			self.next_node.prev_node = new_node

		if self.prev_node is not None:
			self.prev_node.next_node = new_node

		# Copy the values
		new_node.next_node		= self.next_node
		new_node.prev_node		= self.prev_node
		new_node.parent_node	= self.parent_node
		new_node.is_sub_node	= self.is_sub_node
		new_node.child_node		= self.child_node
		new_node.payload		= self.payload

		# Update the children to their new parent
		current = self.child_node

		while current is not None:
			current.parent_node = new_node
			current = current.getSibling()

	def __mergeChildren(self, dir_list):
		""" TODO """
		current = self.child_node
		index = 0

		while current is not None and index < len(dir_list):
			if dir_list[index] < current.name:
				new_item = SourceTree(dir_list[index])
				new_item.on_filesystem = True
				current.addNodeBefore(new_item)
				index += 1

			elif dir_list[index] > current.name:
				# Item does not exist on file system
				current.on_filesystem = False
				current = current.next_node

			else:
				# the same
				current = current.next_node
				index += 1


	def prune(self, recursive=True):
		""" Prune

			This function will prune the tree. It will remove any item from the tree
			that does not belong to either and SCM or is in the file system. It will
			not prune itself.
		"""
		remove_list = []

		# Ok, prune the children first (if recursive), else remember the items
		# that need to be removed as we can't delete them without breaking the
		# linked list walk.
		for item in self.getChilden():
			if not item.on_filesystem and not item.hasState():
				remove_list.append(item)

			if recursive:
				item.prune(recursive)

		# now remove the item(s) while not referencing it.
		for item in remove_list:
			item.deleteNode(False)


	def splitPath(self, path):
		result = []

		(drive, p_copy) = os.path.splitdrive(path)

		while p_copy != os.path.sep and p_copy != '':
			(p_copy, tail) = os.path.split(p_copy)
			result.insert(0, tail)

		return result

	def addTreeNodeByPath(self, path, existing_node=None):
		""" Add an Item to the Tree by Path

			It will find the place that the item belongs
			and if the item does not exist, create add the new
			item. If the item exists already, then return the
			old one.
		"""
		path_bits = self.splitPath(path)

		result = None
		found = True
		new_path = self.getPath()

		if not self.isSuffixFiltered(path):
			result = self
			for part in path_bits:

				new_path = os.path.join(new_path, part)
				if found:
					next_item = result.findChild(part)
					if next_item is None:
						found = False
					else:
						result = next_item

				if not found:
					if self.isDirectoryFiltered(part):
						result = None
						break
					else:
						if existing_node is None:
							is_exist = os.path.exists(new_path)
							is_link = False
							is_dir  = False

							if is_exist:
								is_link = os.path.islink(new_path)
								is_dir  = os.path.isdir(new_path)

							new_node = SourceTree(part)
							new_node.on_filesystem	= is_exist
							new_node.is_link  		= is_link
							new_node.is_dir			= is_dir
						else:
							new_node = existing_node

						result.addChildNode(new_node, mode=NestedTreeNode.INSERT_ASCENDING)
						result = new_node

		return result

	def findItemNode(self, path):
		""" Find Item Node

		This function will find a node in the tree from a path. If the
		node exists then it will return the Node, else None.
		"""
		if self.root == path:
			result = self
		else:
			if self.root and path.startswith(self.root):
				path = os.path.relpath(path, self.root)

			path_bits = self.splitPath(path)

			result = self

			for part in path_bits:
				result = result.findChild(part)

				if result is None:
					break

		return result

	def isOnFileSystem(self):
		return self.on_filesystem

	def checkOnFileSystem(self):
		""" Check Item On File System

			Check to see if the item is still on the file system.
		"""
		self.on_filesystem = os.path.exists(self.getPath(True))
		return self.on_filesystem

	def isSuffixFiltered(self, name):
		result = False

		if self.suffix_filter != []:
			(path, suffix) = os.path.splitext(name)
			result = suffix[1:] in self.suffix_filter

		return result

	def isDirectoryFiltered(self, name):
		result = False

		if self.directory_filter != []:
			if name in self.directory_filter:
				result = True

		return result

	def update(self, path='', recursive=True):
		""" Update

			This function will refresh the directory files that are on
			the filesystem. It will not actually remove any items from
			the tree, that should be done by calling prune().
		"""
		if path == '':
			path = self.getPath()

		if self.is_dir or self.root is not None:
			# Ok, we are in a directory
			dir_list = os.listdir(path)

			# Ok, no children need to add some
			for item in dir_list:
				if item not in self:
					child_path = os.path.join(path, item)

					is_dir = os.path.isdir(child_path)
					is_link = os.path.islink(child_path)

					if (is_dir and not self.isDirectoryFiltered(item)) or (not is_dir and not self.isSuffixFiltered(item)):
						new_item = SourceTree(item)
						new_item.is_dir = is_dir
						new_item.is_link = is_link
						new_item.on_filesystem = True
						self.addChildNode(new_item, mode=NestedTreeNode.INSERT_ASCENDING)

		# We need to walk down all the children
		for child in self.getChilden():
			child_path = os.path.join(path, child.getName())

			child.on_filesystem = os.path.exists(child_path)

			if recursive:
				child.update(child_path)

# vim: ts=4 sw=4 noexpandtab nocin ai
