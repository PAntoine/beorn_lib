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
#    file: nested_tree_test
#    desc: This test will test the nested tree implementation.
#
#  author: Peter Antoine
#    date: 02/06/2015
#---------------------------------------------------------------------------------
#                     Copyright (c) 2015 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import unittest
from beorn_lib.nested_tree import NestedTreeNode
from beorn_lib.nested_tree import NestedTree

def counter(reset = False):
	if "this_id" not in counter.__dict__ or reset:
		counter.this_id = 0
	else:
		counter.this_id += 1

	return counter.this_id

class TestPayload:
	def __lt__(self, other):
		return self.my_id < other.my_id

	def __init__(self, reset = False):
		self.duration = 1
		self.my_id = counter(reset)
		self.start = 0
		self.end   = 0
		self.no_walk = False

class TestNestedTree(unittest.TestCase):
	""" Nested Tree Tests """
	def __init__(self,  testname = 'runTest', scm_type = None, scm_dir = None, test_data = None):
		_ = test_data
		_ = scm_type
		_ = scm_dir

		# initialise the test framework
		super(TestNestedTree, self).__init__(testname)

	def count_function(self, last_visited_node, node,  value,  direction,  levels):
		""" This is a test function that is used to count the number
			of nodes that are encountered.
		"""
		if value is None:
			value = 1
		else:
			value = value + 1

		return (node, value, False)

	def all_nodes_function(self, last_visited_node, node, value, levels, direction):
		""" This function will collect the values from all nodes that
			it encounters in the order that they were walked.
		"""
		if value is None:
			value = [node.payload]
		else:
			value.append(node.payload)

		return (node, value, False)

	def collect_function(self, last_visited_node, node, value, levels, direction):
		""" This is a test function that is used to collect the data
			from the nodes that it has visited. It will return the
			list of nodes that it encounters.
		"""
		if not node.is_sub_node:
			if value is None:
				value = [node.payload]
			else:
				value.append(node.payload)

		return (node, value, False)

	def levels_function(self, last_visited_node, node, value, level, direction):
		""" This is a test function that is used to render the levels information
			it is used to test that the levels counting code works.
		"""
		if value is None:
			node_list = []
		else:
			(_, node_list) = value

		if node.payload is not None:
			node_list.append((level, node.payload.my_id, direction))

		value = (level, node_list)

		return (node,value,False)

	def plain_levels_function(self, last_visited_node,  node, value, level, direction):
		""" This is a test function that is used to render the levels information
			it is used to test that the levels counting code works.
		"""
		if value is None:
			node_list = []
			lowest_level = 1
		else:
			(lowest_level, node_list) = value

		if node.payload is not None:
			node_list.append((level, node.payload))

		if level > lowest_level:
			lowest_level = level

		value = (lowest_level, node_list)

		return (node,value,False)

	def short_walk_function(self,last_visited_node, node,value,levels,direction):
		""" This is a test function that is used to collect the data
			from the nodes that it has visited. It will collect all the
			data for all the nodes, except those blocked by the short walk
			then it will climb back up the tree and carry on walking.

			It will return a list of the nodes that it visited.
		"""
		skip_children = False

		if not node.is_sub_node:
			if value is None:
				value = [node.payload]
			else:
				value.append(node.payload)

		# the magic short walk value - skip the children
		if node.payload is not None and node.payload.no_walk:
			skip_children = True

		return (node,value,skip_children)

	def calculate_function(self,last_visted_node, node,value,levels,direction):
		""" This is a test function that is used to calculate a value
			from the nodes that it has visited.
		"""
		if direction == NestedTreeNode.DIRECTION_DOWN and not node.is_sub_node:
			prev_payload = node.getPrevPayload()

			if prev_payload is None:
				node.payload.start = 0
				node.payload.end   = node.payload.duration
			else:
				node.payload.start = prev_payload.start
				node.payload.end   = prev_payload.start + node.payload.duration

		elif direction == NestedTreeNode.DIRECTION_NEXT:
			prev_payload = node.getPrevPayload()
			node.payload.start = prev_payload.end
			node.payload.end   = prev_payload.end + node.payload.duration

		elif direction == NestedTreeNode.DIRECTION_UP:
			prev_payload = node.getPrevPayload()

			# set the previous end
			if prev_payload.end < last_visted_node.payload.end:
				prev_payload.end = last_visted_node.payload.end

			if not node.is_sub_node:
				# now set the current nodes start and end (and the previous end)
				# have stepped up a level
				node.payload.start = last_visted_node.payload.end
				node.payload.end   = last_visted_node.payload.end + node.payload.duration

		return (node,1,False)

	def dump_endtime_function(self,last_visted_node, node,value,levels,direction):
		""" This is a test function that is used to return the calculated values
			from the nodes that it has visited.
		"""

		if not node.is_sub_node:
			if value is None:
				value = [(node.payload.my_id, node.payload.start, node.payload.end)]
			else:
				value.append((node.payload.my_id, node.payload.start, node.payload.end))

		return (node,value,False)

	def test_createTree(self):
		""" Create Object Test

			This is a simple test that checks that the tree object can be created
			correctly.

			This is an exploding tests, to see if the code functions.`
		"""
		graph = NestedTree()
		self.assertTrue(True)

	def test_createNode(self):
		""" Create Node Test

			This is a basic test to make sure that the object can be created.
			This is an exploding test to see if the code works.
		"""
		node = NestedTreeNode(0)
		self.assertTrue(True)

	def test_addNodes(self):
		""" Add Nodes.

			This test adds three nodes in a row to see if the graph code works.
			This is an exploding test to see if the code works.
		"""
		node1 = NestedTreeNode(1)
		node2 = NestedTreeNode(2)
		node3 = NestedTreeNode(3)

		graph = NestedTree()

		graph.addNodeAfter(node1)
		node1.addNodeAfter(node2)
		node2.addNodeAfter(node3)

		self.assertTrue(graph.hasSibling())
		self.assertTrue(node1.hasSibling())
		self.assertTrue(node2.hasSibling())


	def test_3NodeWalk(self):
		""" 3 Node Walk.

			This test adds three nodes in a row to see if the graph code works.

			It then will walk the tree to see if the it finds all the nodes.
		"""
		node1 = NestedTreeNode(1)
		node2 = NestedTreeNode(2)
		node3 = NestedTreeNode(3)

		graph = NestedTree()

		graph.addNodeAfter(node1)
		node1.addNodeAfter(node2)
		node2.addNodeAfter(node3)

		# we are only using the next function for this rest.
		count = 0
		count = graph.walkTree(self.count_function)
		self.assertTrue(count == 3)

	def test_5NodeWalk(self):
		""" 5 Node Walk - with insert before.

			This test adds three nodes in a row to see if the graph code works
			it also inserts two more nodes before node 2 and node 3.

			It then will walk the tree to see if the it finds all the nodes.
		"""
		node1 = NestedTreeNode(1)
		node2 = NestedTreeNode(2)
		node3 = NestedTreeNode(3)
		node4 = NestedTreeNode(4)
		node5 = NestedTreeNode(5)

		graph = NestedTree()

		# insert the three nodes
		graph.addNodeAfter(node1)
		node1.addNodeAfter(node2)
		node2.addNodeAfter(node3)

		# now insert the two extra nodes
		node2.addNodeBefore(node4)
		node3.addNodeBefore(node5)

		# we are only using the next function for this rest.
		count = 0
		count = graph.walkTree(self.count_function)
		self.assertTrue(count == 5)

	def test_SingleChildNode(self):
		""" Single Child Node with Walk.

			This test will add a single child node.

			It then will walk the tree to see if the it finds all the nodes.
		"""
		node1 = NestedTreeNode(1)
		graph = NestedTree()

		# insert the child node
		graph.addChildNode(node1)

		# we are only using the next function for this rest.
		count = 0
		count = graph.walkTree(self.count_function)
		self.assertTrue(count == 1)

	def test_TraceSimpleTree(self):
		""" Trace A Simple Tree

			This test will create the following tree:

			[root]
             |
             v
			[1] -> [2] -> [11] -> [17] -> [18]
                    |      |
					|      v
					|     [12] -> [13] -> [14] -> [15] -> [16]
					|
					v
				   [3] -> [4] -> [5] -> [9] -> [10]
                                  |
								  v
                                 [6] -> [7] -> [8]

			It should be a walk this tree and return the nodes in the correct order.
		"""
		graph = NestedTree()

		# create the nodes
		nodes = []
		for i in range(19):
			nodes.append(NestedTreeNode(i))

		# now build the tree
		graph.addChildNode(nodes[1])
		nodes[1].addNodeAfter(nodes[2])
		nodes[2].addNodeAfter(nodes[11])
		nodes[11].addNodeAfter(nodes[17])
		nodes[17].addNodeAfter(nodes[18])

		nodes[2].addChildNode(nodes[3])
		nodes[3].addNodeAfter(nodes[4])
		nodes[4].addNodeAfter(nodes[5])
		nodes[5].addNodeAfter(nodes[9])
		nodes[9].addNodeAfter(nodes[10])

		nodes[5].addChildNode(nodes[6])
		nodes[6].addNodeAfter(nodes[7])
		nodes[7].addNodeAfter(nodes[8])

		nodes[11].addChildNode(nodes[12])
		nodes[12].addNodeAfter(nodes[13])
		nodes[13].addNodeAfter(nodes[14])
		nodes[14].addNodeAfter(nodes[15])
		nodes[15].addNodeAfter(nodes[16])

		# we are only using the next function for this rest.
		value = graph.walkTree(self.collect_function)
		self.assertTrue(value == range(1, 19))

	def test_ChildNodeInsertion(self):
		"""
			This tests that the child node insertions work as expected.
			It will also check to see if they can be walked as expected.
		"""
		# test normal insertion - empty list
		graph = NestedTree()
		graph.addChildNode(NestedTreeNode(1))
		self.assertEqual(graph.walkTree(self.all_nodes_function), [1], "Basic insert failed")

		# test normal insertion - empty list - this is the same as above as is the default
		graph = NestedTree()
		graph.addChildNode(NestedTreeNode(1), NestedTreeNode.INSERT_END)
		graph.addChildNode(NestedTreeNode(2), NestedTreeNode.INSERT_END)
		graph.addChildNode(NestedTreeNode(3), NestedTreeNode.INSERT_END)
		self.assertEqual(graph.walkTree(self.all_nodes_function), [1, 2, 3], "Basic append insert")

		# test front insertion - empty list
		graph = NestedTree()
		graph.addChildNode(NestedTreeNode(3), NestedTreeNode.INSERT_FRONT)
		graph.addChildNode(NestedTreeNode(2), NestedTreeNode.INSERT_FRONT)
		graph.addChildNode(NestedTreeNode(1), NestedTreeNode.INSERT_FRONT)
		self.assertEqual(graph.walkTree(self.all_nodes_function), [1, 2, 3], "Basic in front insert")

		# test ascending insertion - empty list
		graph = NestedTree()
		graph.addChildNode(NestedTreeNode(8), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(2), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(3), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(7), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(6), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(5), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(1), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(4), NestedTreeNode.INSERT_ASCENDING)
		graph.addChildNode(NestedTreeNode(5), NestedTreeNode.INSERT_ASCENDING)
		self.assertEqual(graph.walkTree(self.all_nodes_function), [1, 2, 3, 4, 5, 5, 6, 7, 8], "Basic in front insert")


	def test_ChildNodeInsertionDecending(self):
		"""
			This tests that the child node insertions work as expected.
			It will also check to see if they can be walked as expected.
		"""
		# test descending insertion - empty list
		graph = NestedTree()
		graph.addChildNode(NestedTreeNode(1), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(4), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(5), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(6), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(7), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(3), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(8), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(2), NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(NestedTreeNode(5), NestedTreeNode.INSERT_DESCENDING)
		self.assertEqual(graph.walkTree(self.all_nodes_function), [8, 7, 6, 5, 5, 4, 3, 2, 1], "Basic descending insert")

		# test normal insertion - empty list
		nodes =  []
		nodes.append(NestedTreeNode(TestPayload(True)))
		for i in range(1, 10):
			nodes.append(NestedTreeNode(TestPayload()))

		graph = NestedTree()
		graph.addChildNode(nodes[1], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[4], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[5], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[6], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[7], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[3], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[8], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[2], NestedTreeNode.INSERT_DESCENDING)
		graph.addChildNode(nodes[5], NestedTreeNode.INSERT_DESCENDING)

		nodes[7].addChildNode(nodes[9])

		self.assertEqual((1, [(1, 8, 2), (1, 7, 3), (2, 9, 2), (1, 6, 1), (1, 5, 3), (1, 4, 3), (1, 3, 3), (1, 2, 3), (1, 1, 3)]), graph.walkTree(self.levels_function))

	def build_tree(self, use_id = True, mark_no_walk = False):
		"""
			This function will create the following tree:

			{} this indicate sub-tree nodes that have been created.

			[root]
             |
             v
			[1] -> [2] -> [24] -> [40] -> [41] -> [42] -> [43] -> [44] -> [46]
                    |      |                                       |       |
					|      v                                       v       v
					|     {25} -> [26] -> [27] -> [28] -> [29]    [45]    [47] -> [48]
                    |      |
					|      v
					|     {30} -> [31] -> [32] -> [33] -> [34]
                    |      |
					|      v
					|     {35} -> [36] -> [37] -> [38] -> [39]
					|
					v
				   {3} -> [4] -> [5] -> [12] -> [13] -> [14] -> [15] -> [22] -> [23]
                                  |                              |
								  v                              v
                                 {6} -> [7] -> [8]              {16} -> [17] -> [18]
                                  |                              |
								  v                              v
                                 {9} -> [10] -> [11]            {19} -> [20] -> [21]

			It should be a walk this tree and return the nodes in the correct order.

			If no walk is set, then nodes 3,15,34,41 and 46 a marked as no walk, so that
			only the nodes 16-21 and 47,48 will be skipped as they are no walkers.
		"""
		graph = NestedTree()

		# create the nodes
		nodes = []

		if (use_id):
			for i in range(49):
				nodes.append(NestedTreeNode(i))
		else:
			nodes.append(NestedTreeNode(TestPayload(True)))
			for i in range(1, 49):
				nodes.append(NestedTreeNode(TestPayload()))

		#	[1] -> [2] -> [24] -> [40] -> [41] -> [42] -> [43] -> [44] -> [46]
		graph.addChildNode(nodes[1])
		nodes[1].addNodeAfter(nodes[2])
		nodes[2].addNodeAfter(nodes[24])
		nodes[24].addNodeAfter(nodes[40])
		nodes[40].addNodeAfter(nodes[41])
		nodes[41].addNodeAfter(nodes[42])
		nodes[42].addNodeAfter(nodes[43])
		nodes[43].addNodeAfter(nodes[44])
		nodes[44].addNodeAfter(nodes[46])

		# [25] -> [26] -> [27] -> [28] -> [29]
		nodes[24].addSubTreeNode(nodes[25])
		nodes[25].addNodeAfter(nodes[26])
		nodes[26].addNodeAfter(nodes[27])
		nodes[27].addNodeAfter(nodes[28])
		nodes[28].addNodeAfter(nodes[29])

		# subgraph of 24 - added from 24
		# [30] -> [31] -> [32] -> [33] -> [34]
		nodes[24].addSubTreeNode(nodes[30])
		nodes[30].addNodeAfter(nodes[31])
		nodes[31].addNodeAfter(nodes[32])
		nodes[32].addNodeAfter(nodes[33])
		nodes[33].addNodeAfter(nodes[34])

		# subtree of 24 - added from 24
		# [35] -> [36] -> [37] -> [38] -> [39]
		nodes[24].addSubTreeNode(nodes[35])
		nodes[35].addNodeAfter(nodes[36])
		nodes[36].addNodeAfter(nodes[37])
		nodes[37].addNodeAfter(nodes[38])
		nodes[38].addNodeAfter(nodes[39])

		# child of 44 - single
		nodes[44].addChildNode(nodes[45])

		# child of 46 - pair and end tree on an up.
		nodes[46].addChildNode(nodes[47])
		nodes[47].addNodeAfter(nodes[48])

		# subtree of 2
		#  [3] -> [4] -> [5] -> [12] -> [13] -> [14] -> [15] -> [22] -> [23]
		nodes[2].addSubTreeNode(nodes[3])
		nodes[3].addNodeAfter(nodes[4])
		nodes[4].addNodeAfter(nodes[5])
		nodes[5].addNodeAfter(nodes[12])
		nodes[12].addNodeAfter(nodes[13])
		nodes[13].addNodeAfter(nodes[14])
		nodes[14].addNodeAfter(nodes[15])
		nodes[15].addNodeAfter(nodes[22])
		nodes[22].addNodeAfter(nodes[23])

		# subtree of 5
		# [6] -> [7] -> [8]
		nodes[5].addSubTreeNode(nodes[6])
		nodes[6].addNodeAfter(nodes[7])
		nodes[7].addNodeAfter(nodes[8])

		# subtree of 5
		# [9] -> [10] -> [11]
		nodes[5].addSubTreeNode(nodes[9])
		nodes[9].addNodeAfter(nodes[10])
		nodes[10].addNodeAfter(nodes[11])

		# subtree of 15
		# [16] -> [17] -> [18]
		nodes[15].addSubTreeNode(nodes[16])
		nodes[16].addNodeAfter(nodes[17])
		nodes[17].addNodeAfter(nodes[18])

		# subtree of 15
		# [19] -> [20] -> [21]
		nodes[15].addSubTreeNode(nodes[19])
		nodes[19].addNodeAfter(nodes[20])
		nodes[20].addNodeAfter(nodes[21])

		# Ok, need to make a couple of nodes as no-walk nodes to test that the
		# short walk code works.
		# So 3, 15, 34, and 41 as this are all different in the tree and should prove that
		# the code works.
		if not use_id and mark_no_walk:
			nodes[3].payload.no_walk = True
			nodes[15].payload.no_walk = True
			nodes[34].payload.no_walk = True
			nodes[41].payload.no_walk = True
			nodes[46].payload.no_walk = True

		return graph

	def test_TraceComplexTree(self):
		""" Trace A Complex Tree

			This will test to see if the sub-tree code works. Also it should walk the tree in
			a different order to a normal tree. It will walk down the next pointers after the
			sub-tree, before walking down the children of the sub-tree.
		"""

		graph = self.build_tree()

		# we are only using the next function for this rest.
		value = graph.walkTree(self.collect_function)

		self.assertTrue(value == range(1, 49))

	def test_CountComplexTree(self):
		""" count a complex tree

			This will test to see if the sub-tree code works. Also it should walk the tree in
			a different order to a normal tree. It will walk down the next pointers after the
			sub-tree, before walking down the children of the sub-tree.

			This uses another function to count the subtrees to check that the payloads can
			be used as required.
		"""
		graph = self.build_tree(False)

		# we are only using the next function for this rest.
		value = graph.walkTree(self.calculate_function)
		value = graph.walkTree(self.dump_endtime_function)

		# test the end of the tree is the correct one and the start and time are correct
		self.assertTrue(value[len(value)-1][0] == 48 and value[len(value)-1][1] == 25 and value[len(value)-1][2] == 26)

	def test_ShortWalkTree(self):
		""" test that the tree works if the short walk is done.

			This will test to see if the sub-tree code works. Also it should walk the tree in
			a different order to a normal tree. It will walk down the next pointers after the
			sub-tree, before walking down the children of the sub-tree.

			This uses another function to count the subtrees to check that the payloads can
			be used as required.
		"""
		graph = self.build_tree(False,True)

		# we are only using the next function for this rest.
		value = graph.walkTree(self.short_walk_function)

		correct_results = range(1,16) + range(22,46)

		for index in range(len(correct_results)):
			if value[index].my_id != correct_results[index]:
				self.assertTrue(value[index].my_id == correct_results[index])
				break

	def test_LevelsTree(self):
		""" test that the tree counts the levels during walks correctly.

			This uses another function to count the subtrees to check that the payloads can
			be used as required.
		"""
		graph = self.build_tree(False,True)

		# we are only using the next function for this rest.
		value = graph.walkTree(self.levels_function)

		# test that the walk worked correctly.
		# Note: that the last level is not 0, as the walk_function is not called on the root node.
		self.assertEqual(value,(2,[(1,1,2),(1,2,3),(3,3,2),(3,4,3),(3,5,3),(5,6,2),(5,7,3),(5,8,3),(5,9,2),(5,10,3),(5,11,3), \
								(3,12,1),(3,13,3),(3,14,3),(3,15,3),(5,16,2),(5,17,3),(5,18,3),(5,19,2),(5,20,3),(5,21,3), \
								(3,22,1),(3,23,3),(1,24,1),(3,25,2),(3,26,3),(3,27,3), (3,28,3),(3,29,3),(3,30,2),(3,31,3),\
								(3,32,3),(3,33,3),(3,34,3),(3,35,2),(3,36,3),(3,37,3),(3,38,3),(3,39,3),(1,40,1), (1,41,3),\
								(1,42,3),(1,43,3),(1,44,3),(2,45,2),(1,46,1),(2,47,2),(2,48,3)]))

	def test_LevelTreeExport(self):
		""" Level Tree Export.

			This test, will test that the level tree walks work and the tree can be exported
			as a levelled list.
		"""
		counter.this_id = 0
		graph = self.build_tree(False)

		tree = (graph,graph.getChildren())

		for item in tree[1]:

			if item.hasChild():
				children = item.getChildren()

				for c_list in children:
					if type(c_list) == list:
						for child in c_list:

							if child.hasChild():
								children_1 = child.getChildren()

								for c_list_1 in children_1:
									if type(c_list_1) == list:

										for child_2 in c_list_1:
											pass
					else:
						pass

	def test_MakeTree(self):
		""" Make Tree

			The test checks that makeSubTree function works.

			So the following tree:

				[1] -> [2] -> [3] -> [7] -> [8] -> [9] -> [10] -> [11] -> [12]
			                   |
							  {4} -> [5] -> [6]

			can be turned into:

				[1] -> [2] -> [3]
				               |
							  {4} -> [5] -> [6]
							   |
							  {7} -> [8] -> [9]
	 						                 |
							                {10}-> [11] -> [12]

			by calling sub-tree on (3), (9) in that order.

			Then add a new subTree:

				[1] -> [2] -> [3]
				               |
							  {4} -> [5] -> [6]
							   |
							  {7} -> [8] -> [9]
	 						   |             |
							   |            {10}-> [11] -> [12]
                               |
		                      {13} -> [14] -> [15]

			By adding a subTree to (3), this will prove it works. Also doing a
			next walk on (3).
		"""
		graph = NestedTree()

		# create the nodes
		nodes = []

		for i in range(16):
			nodes.append(NestedTreeNode(i))

		graph.addChildNode(nodes[1])
		graph.addChildNode(nodes[2])
		graph.addChildNode(nodes[3])
		graph.addChildNode(nodes[7])
		graph.addChildNode(nodes[8])
		graph.addChildNode(nodes[9])
		graph.addChildNode(nodes[10])
		graph.addChildNode(nodes[11])
		graph.addChildNode(nodes[12])

		nodes[3].addChildNode(nodes[4])
		nodes[4].addNodeAfter(nodes[5])
		nodes[5].addNodeAfter(nodes[6])
		self.assertEqual(graph.walkTree(self.collect_function), range(1, 13))
		self.assertEqual(graph.walkTree(self.plain_levels_function), (2, [(1, 1), (1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12)]))

		# Subtrees don't make sense unless the whole tree are subtrees.

		# ok, let's let makeSubTree do it's thing.
#		self.assertTrue(graph.makeSubTree(nodes[3]))
#		self.assertTrue(graph.makeSubTree(nodes[9]))
#		self.assertEqual(graph.walkTree(self.collect_function), range(1, 13))
#		self.assertEqual(graph.walkTree(self.plain_levels_function), (5, [(1, 1), (1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (5, 10), (5, 11), (5, 12)]))

		# ok, add the new sub-tree
		nodes[12].addSubTreeNode(nodes[13])
		nodes[13].addNodeAfter(nodes[14])
		nodes[14].addNodeAfter(nodes[15])

		# walk the tree
		value = graph.walkTree(self.collect_function)

		# now check the ordering is correct
		self.assertEqual(value, range(1, 16))

		# check the shape of the tree
		#self.assertFalse(nodes[3].hasSibling())
		self.assertFalse(nodes[6].hasSibling())
		self.assertFalse(nodes[12].hasSibling())

		self.assertTrue(nodes[3].hasChild())
		self.assertTrue(nodes[12].hasChild())

if __name__ == '__main__':
    unittest.main()

# vim: ts=4 sw=4 noexpandtab nocin ai
