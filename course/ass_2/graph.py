from node import Node
from queue import Queue
from constants import Constants
from copy import deepcopy

# Everything here is STATIC
class Graph:
	root = None
	node_count = 0
	configs = None

	def init():
		Graph.configs = dict()
		empty_grid = Graph.get_empty_grid()
		Graph.root = Node(empty_grid, None, True)
		q = Queue()
		q.put(Graph.root)
		while(q.qsize() != 0):
			cur_node = q.get()
			Graph.node_count = Graph.node_count+1
			is_end, player = cur_node.is_complete()
			if(is_end == False):
				nodes_to_expand = Graph.get_next_nodes_to_expand(cur_node)
				Graph.add_nodes_to_expand_to_q(nodes_to_expand, q)

	def add_nodes_to_expand_to_q(nodes_to_expand, q):
		for node_ in nodes_to_expand:
			q.put(node_)

	def get_next_nodes_to_expand(node):
		nodes_to_expand = []
		row = 0
		next_turn = not node.user_turn
		while(row < Constants.dim):
			col = 0
			while(col < Constants.dim):
				if(node.grid[row][col] == Constants.unoccupied):
					grid_copy_1 = deepcopy(node.grid)
					grid_copy_2 = deepcopy(node.grid)
					grid_copy_1[row][col] = Constants.user
					grid_copy_2[row][col] = Constants.computer
					is_present_, node_ = Graph.is_present(grid_copy_1)
					if( is_present_ == True ):
						new_node_1 = node_
					else:
						new_node_1 = Node(grid_copy_1, node, next_turn)
						Graph.configs[str(grid_copy_1)] = new_node_1
						nodes_to_expand.append(new_node_1)
					is_present_, node_ = Graph.is_present(grid_copy_2)
					if( is_present_ == True ):
						new_node_2 = node_
					else:
						new_node_2 = Node(grid_copy_2, node, next_turn)
						Graph.configs[str(grid_copy_2)] = new_node_2
						nodes_to_expand.append(new_node_2)
					node.children.append(new_node_1)
					node.children.append(new_node_2)
				col = col+1
			row = row+1
		return nodes_to_expand

	def get_empty_grid():
		grid = []
		row = 0
		while(row < Constants.dim):
			col = 0
			row_ = []
			while(col < Constants.dim):
				row_.append(Constants.unoccupied)
				col = col+1
			grid.append(row_)
			row = row+1
		return grid

	def is_present(tar_grid):
		is_present_ = Graph.configs.get(str(tar_grid))
		if( is_present_ != None ):
			return True, is_present_
		return False, None

	# BFS
	def print():
		print("Graph: ")
		q = Queue()
		q.put(Graph.root)
		while(q.qsize() != 0):
			cur_node = q.get()
			cur_node.print()
			for child in cur_node.children:
				q.put(child)
		print("Nodes: " + str(Graph.node_count))