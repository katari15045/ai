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
	#		Graph.is_pruning_possible(cur_node)
			Graph.node_count = Graph.node_count+1
			is_end, player = Node.is_complete(cur_node)
			if(is_end == False):
				nodes_to_expand = Graph.get_next_nodes_to_expand(cur_node)
				Graph.add_nodes_to_expand_to_q(nodes_to_expand, q)

	#def is_pruning_possible(base_node):


	def add_nodes_to_expand_to_q(nodes_to_expand, q):
		for node_ in nodes_to_expand:
			q.put(node_)

	def get_next_nodes_to_expand(parent):
		nodes_to_expand = []
		row = 0
		is_next_turn_user = not parent.user_turn
		while(row < Constants.dim):
			col = 0
			while(col < Constants.dim):
				if(parent.grid[row][col] == Constants.unoccupied):
					grid_copy = deepcopy(parent.grid)
					if( is_next_turn_user == False ):
						# current turn: user
						grid_copy[row][col] = Constants.user
					else:
						grid_copy[row][col] = Constants.computer
					is_present_, node_ = Graph.is_present(grid_copy)
					if( is_present_ == True ):
						new_node = node_
						node_.other_parents.append(parent)
					else:
						new_node = Node(grid_copy, parent, is_next_turn_user)
						Graph.configs[str(grid_copy)] = new_node
						nodes_to_expand.append(new_node)
					parent.children.append(new_node)
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
		configs_2 = dict()
		count = 0
		print("Graph: ")
		q = Queue()
		q.put(Graph.root)
		while(q.qsize() != 0):
			cur_node = q.get()
			cur_config = str(cur_node.grid)
			if(configs_2.get(cur_config) == None):
				configs_2[cur_config] = True
				print(str(count) + " / " + str(len(Graph.configs)))
				count = count+1
				if(cur_node.cost == -2):
					cur_node.print()
				cur_node.print()
				for child in cur_node.children:
					q.put(child)
		print("Unique configs: " + str(len(Graph.configs)))

	def get_child(node, grid):
		for child in node.children:
			if(child.grid == grid):
				return child

	def next_move(node):
		for child in node.children:
			if(child.cost == Constants.computer_optimal_cost):
				return child
		for child in node.children:
			if(child.cost == Constants.tie_cost):
				return child
		for child in node.children:
			if(child.cost == Constants.user_optimal_cost):
				return child
		