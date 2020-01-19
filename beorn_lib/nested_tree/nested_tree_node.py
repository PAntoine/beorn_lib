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
#    file: nested_tree_node
#    desc:
#
#  author: peter
#    date: 19/08/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

class NestedTreeNode (object):
	""" This is the node for the tree """

	# constants for tree walking
	DIRECTION_UP	= 1
	DIRECTION_DOWN	= 2
	DIRECTION_NEXT	= 3
	DIRECTION_STOP	= 4

	# how to insert a child_node into the list of child nodes.
	INSERT_FRONT		= 1
	INSERT_END			= 2
	INSERT_ASCENDING	= 3
	INSERT_DESCENDING	= 4

	def __init__(self, payload = None, is_sub_node = False):
		self.next_node 		= None
		self.prev_node 		= None
		self.parent_node	= None
		self.open 			= False
		self.is_sub_node	= is_sub_node
		self.child_node		= None
		self.payload		= payload
		self.colour			= None

		super(NestedTreeNode, self).__init__()

	def copy(self, old_node):
		self.next_node = old_node.next_node
		self.prev_node = old_node.prev_node
		self.parent_node = old_node.parent_node
		self.open = old_node.open
		self.is_sub_node = old_node.is_sub_node
		self.child_node = old_node.child_node
		self.payload = old_node.payload
		self.colour = old_node.colour

	def __iter__(self):
		for item in self.getChildren():
			yield item

	def __lt__(self, other):
		""" The less_than comparison operator. """
		if type(other) is NestedTreeNode:
			# if we are nested tree, then we compare the payloads
			# if possible.
			if isinstance(other.payload, type(self.payload)) and (hasattr(self.payload, '__lt__') or hasattr(self.payload, '__cmp__')):
				return self.payload < other.payload

		return NotImplemented

	def isOpen(self):
		return self.open

	def setOpen(self, state):
		self.open = state

	def toggleOpen(self):
		self.open = not self.open

	def hasChild(self):
		""" Has Child

			This function returns true if the node has a child node.
		"""
		if self.child_node is not None:
			return True
		else:
			return False

	def hasSibling(self):
		""" Has Sibling

			This function returns true if the node has a sibling node.
		"""
		if self.next_node is not None:
			return True
		else:
			return False

	def getSibling(self):
		""" Get Sibling

			This function will walk to the next node, ignoring any children
			that are logically the next node to walk to. If you want to walk
			the tree in order use getNext().

			This function will return 'None' if there are not siblings.
		"""
		return self.next_node

	def getParent(self):
		""" Gets the parent node """
		return self.parent_node

	def isChildOf(self, node):
		""" Returns true if the node is a child the given node """
		result = False
		current = self

		while current is not None:
			current = current.getParent()
			if current == node:
				result = True
				break

		return result

	def getNumberChildren(self):
		""" Get number of children.

			This will count the number of children.
		"""
		result = 0

		if self.hasChild():
			current_child = self.child_node

			while current_child is not None:
				if current_child.is_sub_node:
					# We have a sub node, so need to create a sub-node array and then walk
					# all the children for the sub-node.
					current_sub_child = current_child.child_node

					while current_sub_child is not None:
						result += 1
						current_sub_child = current_sub_child.next_node

				else:
					result += 1

				current_child = current_child.next_node

		return result

	def getChildren(self):
		""" Get the Children of the Node.

			This function will return a list (of lists) of the direct children
			of the current node. If the node has sub-trees belonging in to it
			each of these sub-trees (only the direct descendants) will be lists
			as separate list arrays.
		"""
		result = []

		if self.hasChild():
			current_child = self.child_node

			while current_child is not None:
				if current_child.is_sub_node:
					# We have a sub node, so need to create a sub-node array and then walk
					# all the children for the sub-node.
					current_sub_child = current_child.child_node
					child_array = []

					while current_sub_child is not None:
						child_array.append(current_sub_child)
						current_sub_child = current_sub_child.next_node

					result.append(child_array)

				else:
					result.append(current_child)

				current_child = current_child.next_node

		return result

	def getNextNode(self):
		""" Walk to the next node.

			This function is the method that handles walking the tree. It will go
			from the current node to the next node and when it reaches the end of
			the current sub-tree it will walk to the parent_node node. When it reaches
			the end of the tree it will return None.
		"""
		# do we have a child_node?
		if self.child_node is not None:
			result = (self.child_node, 1, NestedTreeNode.DIRECTION_DOWN)

		# is there a next current_node?
		elif self.next_node is not None:
			result = (self.next_node, 0, NestedTreeNode.DIRECTION_NEXT)

		# do we have a parent_node?
		elif self.parent_node is not None:
			(node,levels) = self.getNextUpNode()
			result = (node, levels, NestedTreeNode.DIRECTION_UP)

		# no children, no next, no parent_node, must be the root current_node.
		else:
			result = (None, 0, None)

		return result

	def skipChildren(self):
		""" Goto to the next non-child node.

			This function will simply go to the next node, skipping any children
			of the current node.
		"""
		if self.next_node is not None:
			result = (self.next_node,0,NestedTreeNode.DIRECTION_NEXT)

		# do we have a parent_node?
		elif self.parent_node is not None:
			(node,levels) = self.getNextUpNode()
			result = (node,levels,NestedTreeNode.DIRECTION_UP)

		else:
			# no children, no next, no parent_node, must be the root current_node.
			result = (None, 0, None)

		return result

	def getNextUpNode(self):
		""" Goto the Next Upper Node.

			This function is the method that is used to walk up a node, it will
			check for a parent that has a next node, if this is found then this
			is returned, if it is not found then the function returns None.
		"""
		result = None
		current = self.parent_node
		levels = -1

		while current is not None:
			if current.next_node is not None:
				result = current.next_node
				break

			current = current.parent_node
			levels -= 1

		return (result, levels)

	def getPrevPayload(self):
		""" This function will return the previous payload.

			It will calculate from the tree what is the previous payload the current
			node, and it will then return it.
		"""
		if self.is_sub_node:
			result = self.parent_node.payload

		elif self.prev_node is not None and self.prev_node.is_sub_node:
			result = self.prev_node.parent_node.payload

		elif self.prev_node is not None:
			result = self.prev_node.payload

		elif self.parent_node is not None:
			if self.parent_node.is_sub_node:
				result = self.parent_node.parent_node.payload
			else:
				result = self.parent_node.payload

		else:
			result = None

		return result

	def addNodeAfter(self, new_node):
		""" Add a node after

			This function will insert the node into the tree after the given node.
			It will only add a single node. If the current node has links it will
			be rejected.

			self -> new_node -> (self->next)
		"""
		result = False

		if new_node.next_node is None and new_node.prev_node is None:
			new_node.next_node = self.next_node
			new_node.prev_node = self

			if self.next_node is not None:
				self.next_node.prev_node = new_node

			self.next_node = new_node
			new_node.parent_node = self.parent_node
			result = True

			if self.parent_node is not None and self.parent_node.last_child_node == self:
				self.parent_node.last_child_node = new_node

		return result

	def addNodeBefore(self, new_node):
		""" Add a node before the given node

			This function will insert the node into the tree before the given node.
		"""
		result = False

		if new_node.next_node is None and new_node.prev_node is None:
			new_node.prev_node = self.prev_node
			new_node.next_node = self

			if self.prev_node is not None:
				self.prev_node.next_node = new_node

			self.prev_node = new_node
			new_node.parent_node = self.parent_node

			if self.parent_node is not None and self.parent_node.child_node == self:
				self.parent_node.child_node = new_node

			result = True

		return result

	def addChildNode(self, child_node, mode = INSERT_END):
		""" Add a node to the tree as a child_node.

			This added the child_node node to the list of nodes that are child_node of the
			parent_node. The child cannot have a parent node, it will be rejected. All other
			links are ignored.
		"""
		result = False

		if child_node.parent_node is None:
			result = True

			if self.child_node is None:
				# first child - this means all the reset will have children.
				self.child_node = child_node
				self.last_child_node = child_node
				child_node.prev_node = None
				child_node.next_node = None
				child_node.parent_node = self

			elif mode == NestedTreeNode.INSERT_FRONT:
				self.child_node.addNodeBefore(child_node)

			elif mode == NestedTreeNode.INSERT_END:
				self.last_child_node.addNodeAfter(child_node)

			elif mode == NestedTreeNode.INSERT_ASCENDING:
				current = self.child_node
				while current is not None:
					if child_node < current:
						current.addNodeBefore(child_node)
						break

					current = current.next_node
				else:
					# The while's else - we have reached the end of the children.
					self.last_child_node.addNodeAfter(child_node)

			elif mode == NestedTreeNode.INSERT_DESCENDING:
				current = self.last_child_node

				while current is not None:
					if child_node < current:
						current.addNodeAfter(child_node)
						break

					current = current.prev_node
				else:
					self.child_node.addNodeBefore(child_node)
			else:
				result = False

		return result

	def addSubTreeNode(self, child_node):
		""" Add a node to the tree as the first element of a sub-tree.

			The nodes that belong to this node a walked before the children of the parent.
			It changes the way that the tree is walked. As it uses the next pointers to
			handle the way that the sub-trees are connected.

			This structure means that the tree can be walked from any position in the tree
			without keeping track of where you have been and without doing searches for
			elements within parents. This structure trades memory for speed.

			   [p]
			    |
				v
			   [d] -> [d] -> [d]
			    |      |      |
				V      V      V
			   [c]    [c]    [c]

			Note: when counting sub-trees the depth is twice as deep as ordinary trees
			      as each level has a dummy node for tree organisation.
		"""
		result = False

		# child MUST NOT be a child already
		if child_node.parent_node is None:
			if self.child_node is None:
				# just add the child
				dummy_node = NestedTreeNode(None,True)
				self.addChildNode(dummy_node)
				dummy_node.addChildNode(child_node)

				result = True

			elif self.child_node.is_sub_node:
				# need to walk to the end of the children then add the node
				current_node = self.child_node

				while current_node.next_node is not None:
					current_node = current_node.next_node

				# add new sub tree
				dummy_node = NestedTreeNode(None,True)
				current_node.addNodeAfter(dummy_node)
				dummy_node.addChildNode(child_node)

				result = True

		return result

	def makeSubTree(self, node):
		""" Make the given node a sub-tree node.

			It will take the given node and make it's siblings into a sub-tree of the
			given node. If the node already has a sub-tree then the siblings will be
			added to the end of the sub-tree (using the normal sub-tree algorithm).
		"""
		node.deleteNode(False)
		return self.addSubTreeNode(node)

	def deleteNode(self, recursive):
		""" remove a node from the tree

			This will remove a node from the tree, it will also remove the node from
			a node that has it as parent_node.
		"""
		# Remove from parent if we are linked.
		if self.parent_node is not None:
			if self.parent_node.child_node == self:
				self.parent_node.child_node = self.next_node

			if self.parent_node.last_child_node == self:
				self.parent_node.last_child_node = self.prev_node

		if self.prev_node is not None:
			self.prev_node.next_node = self.next_node

		if self.next_node is not None:
			self.next_node.prev_node = self.prev_node

		if recursive:
			while self.child_node is not None:
				self.child_node.deleteNode(recursive)

		self.next_node = None
		self.prev_node = None
		self.parent_node = None

		return True

	def deleteChildren(self):
		""" remove all the children from this item.

			I should really give the garbage collector a bit of a workout here
			but old and paranoid so lets recursively remove the items.
		"""
		while self.child_node is not None:
			self.child_node.deleteNode(True)

	def findItemWithColour(self, colour):
		""" Find the item in the tree with the specific colour.

			The "colours" as in R/B colours should be linear in the tree. I.e. should
			be ascending in the tree so that the search can use a sort of binary chop
			to search through the tree. Also when the colours are updated in the tree
			you don't need to paint the whole tree, as the chop algo will ignore the
			colours that are out of order.

			Due to the nature of the search it is not recursive and does not need to
			walk back up the tree.
		"""
		if self.colour == colour:
			return self

		else:
			current = self

			while current is not None and current.colour <= colour:
				if current.colour == colour:
					return current

				if current.next_node is not None and current.next_node.colour <= colour:
					current = current.next_node
				elif current.child_node is not None:
					# Ok, we know it's between us and the next node, look children.
					current = current.child_node
				else:
					# Ok, can't exist.
					return None

		return None

	def walkTree(self, action_function = None):
		""" This function will walk the whole tree and call the actions.

			This function will walk the tree and it will call the functions
			when the walk reaches certain states. When the tree does to a
			next node, then the next_function is called if present, and the
			down_function called when the tree walks down to a child_node, and
			when the function walks up, the up_function is called.

			If the function wants to end the walk early then the function
			should return the current node as None and the loop will end.

			The functions accept two parameters current_node and the value.
			The value is for the functions and the walk does not use it. The
			current_node is the next node
		"""

		current_node = self
		value = None
		skip_children = False

		levels = 0

		while current_node is not None:
			last_visted_node = current_node
			level_change = 0

			if skip_children:
				(current_node, level_change, direction) = current_node.skipChildren()
			else:
				(current_node, level_change, direction) = current_node.getNextNode()

			levels += level_change

			if current_node is not None and action_function is not None:
				(current_node, value, skip_children) = action_function(last_visted_node, current_node, value, levels, direction)

		if value is None:
			return []
		else:
			return value

# vim: ts=4 sw=4 noexpandtab nocin ai
