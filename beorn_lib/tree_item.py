#!/usr/bin/env python
#---------------------------------------------------------------------------------
#
#                    ,--.
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,
#                    | .-. '| .-. :| .-. ||  .--'|      \
#                    | `-' |\   --.' '-' '|  |   |  ||  |
#                     `---'  `----' `---' `--'   `--''--'
#
#    file: tree_item
#    desc: This is a simple class that holds the details for the tree items tree
#          entries.
#
#  author:
#    date: 30/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import string

class TreeItem(object):
	""" TreeItem Class """

	# View state
	TREE_ITEM_STATE_OPEN			= 0
	TREE_ITEM_STATE_CLOSED			= 1

	# Deleted, Added, unchanged, Amended
	item_text_status	= [ 'x', '+', ' ', '~', '*' ]

	# text directory markers: closed, open
	item_dir_markers	= [ 'v', '>' ]

	def	__init__(self, name, parent, payload = None, level = 0):
		self.name		= name
		self.parent		= parent
		self.value		= None
		self.state		= TreeItem.TREE_ITEM_STATE_CLOSED
		self.item_list	= []
		self.level      = level
		self.payload	= payload

	def isOpen(self):
		""" Is the State open. """
		if self.state == TreeItem.TREE_ITEM_STATE_CLOSED:
			return False
		else:
			return True

	def isLeaf(self):
		""" Is the item a leaf item or does it have children """
		return len(self.item_list) == 0

	def toggleState(self):
		""" Toggle State """
		if self.state == TreeItem.TREE_ITEM_STATE_CLOSED:
			self.state = TreeItem.TREE_ITEM_STATE_OPEN
		else:
			self.state = TreeItem.TREE_ITEM_STATE_CLOSED

	def setState(self, state):
		""" Set the Open State """
		self.open = state

	def getLevel(self):
		""" Get Level """
		return self.level

	def addEntry(self, entry_path):
		""" Add Entry

			This function will add an entry to the TreeItem or one of it's sub-trees.

			It expects the path to be rooted at the same level as the TreeItem entry
			and will create a tree relative to that.

			Note: that it expects a hard path and not a relative path, these will be
			ignored and the results will be unpredictable.
		"""
		result = None

		# first split the path into a list
		path_bits = []

		(path, file_name) = os.path.split(entry_path)

		if len(file_name) > 0:
			(path, head) = os.path.split(path)

			while len(head) > 0:
				path_bits.append(head)
				(path, head) = os.path.split(path)

			# now find the directory that the file belongs in
			current_dir = self
			parent = None

			ordered_path = path_bits[::-1]

			for index, bit in enumerate(ordered_path, 1):
				for item in current_dir.item_list:
					if bit == item.name:
						parent = current_dir
						current_dir = item
						break
				else:
					current_dir = current_dir.addSubEntry(bit)

			# Ok, we can add the file to the current directory, where it belongs
			result = current_dir.addSubEntry(file_name)

		return result

	def clearSubEntries(self):
		""" Clear Sub-Entries

			This function will clear all the sub-entries to the element.
		"""
		self.item_list = []

	def addSubEntry(self, name, payload = None):
		""" Add Sub Entry

			This function will add a sub-entry to a TreeItem item.
		"""
		result = TreeItem(name, self, payload = payload, level = self.level + 1)
		self.item_list.append(result)

		return result

	def addChild(self, entry):
		""" Add Child

			This function is not to un-similar to the one above only it
			takes a tree item as a parameter.
		"""
		entry.parent = self
		entry.level = self.level + 1
		self.item_list.append(entry)

	def appendEntry(self, entry):
		""" Append Entry

			This function will append a TreeItem to the current element.
		"""
		self.item_list.append(entry)

	def removeEntry(self, entry):
		""" Remove Entry

			This function will remove a TreeItem from the current element.
		"""
		if entry in self.item_list:
			self.item_list.remove(entry)

	def insertAfter(self, entry, new_entry):
		""" Insert After

			This function will insert an entry in the tree after the given
			element.
		"""
		result = False

		if entry in self.item_list:
			index = self.item_list(entry) + 1
			self.item_list.insert(index, new_entry)

			result = True

		return result

	def getPath(self):
		""" Get Path

			Returns the path of the specific item.
		"""
		current = self.parent
		result = self.name

		while current != None:
			result = os.path.join(current.name, result)
			current = current.parent

		return result

	def getItemList(self):
		""" Get Item List

			This function will return the list of items for the version.
		"""
		return self.item_list

	def walkTree(self, callback, level=0):
		""" Render Text Tree

			This function will recursively render the text tree. It will only walk down the
			item that have a status of OPEN.
		"""
		callback(self, level)

		if self.state == TreeItem.TREE_ITEM_STATE_OPEN:
			for item in self.item_list:
				item.walkTree(callback, level+1)

	def findItemByValue(self, value):
		""" Find Text Item

			This function will search the tree until the correct item is found.
		"""
		result = None

		if value == self.value:
			result = self

		else:
			for item in self.item_list:
				if value == item.value:
					result = item

				result = item.findItemByValue(value)

				if result is not None:
					break

		return result

	def update(self, sub_tree=True):
		""" Update

			This item will update the current item.

			If the item has children and the sub_tree is true then this
			will walk recursively call the this function.

			It is expected if you are noy using the updateTree method that
			this function will be overloaded.
		"""
		if sub_tree:
			for item in self.item_list:
				item.update(sub_tree)

	def updateTree(self, item_list):
		""" Update Tree

			This function will update the tree with the items that are found in the
			list. This function updates a node with the information from the list
			and this can cause the whole tree to be updated.

			This function assumes the order of the lists have not changed, just that
			items may have been added or deleted from the item_list. If this is not
			true then the behaviour of this function will be unpredictable.
		"""
		# Ok, need to compare the list against the list of items
		marker = 0

		item_length = len(item_list)

		while marker < item_length and marker < len(self.item_list):
			# are the two items the same
			if item_list[marker] == self.item_list[marker].payload:
				item_list[marker].updateTreeItem(self.item_list[marker])
				marker += 1

			else:
				# Ok, they do not match, so which list has changed?
				if self.item_list[marker].payload not in item_list:
					# Ok, item has been deleted from the list.
					del self.item_list[marker]

				else:
					# Ok, it must be a new item
					new_entry = item_list[marker].getTree(self)
					self.item_list.insert(marker, new_entry)
					marker += 1

		# add the items in the list that are not in the current tree
		while marker < item_length:
			if item_list[marker] is not None:
				new_entry = item_list[marker].getTree(self)
				self.item_list.append(new_entry)
			marker += 1

		# remove the items that are no longer in the tree
		self.item_list = self.item_list[0:marker]

# vim: ts=4 sw=4 noexpandtab nocin ai

