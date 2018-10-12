from node import Node
from queue import Queue
from constants import Constants
from copy import deepcopy

# Everything here is STATIC
class Graph:
	root = None
	node_count = 0

	def init():
		# init Root Node
		empty_grid = Graph.get_empty_grid()
		Graph.root = Node(empty_grid)
		q = Queue()
		q.put(Graph.root)
		while(q.qsize() != 0):
			cur_node = q.get()
			Graph.node_count = Graph.node_count+1
			is_end, player = cur_node.is_complete()
			if(is_end == False):
				next_moves = Graph.get_next_moves(cur_node)
				cur_node.children = next_moves
				Graph.add_children_to_q(cur_node.children, q)

	def add_children_to_q(children, q):
		for child in children:
			q.put(child)

	def get_next_moves(node):
		moves = []
		row = 0
		while(row < Constants.dim):
			col = 0
			while(col < Constants.dim):
				if(node.grid[row][col] == Constants.unoccupied):
					grid_copy_1 = deepcopy(node.grid)
					grid_copy_2 = deepcopy(node.grid)
					grid_copy_1[row][col] = Constants.user
					grid_copy_2[row][col] = Constants.computer
					new_node_1 = Node(grid_copy_1)
					new_node_2 = Node(grid_copy_2)
					moves.append(new_node_1)
					moves.append(new_node_2)
				col = col+1
			row = row+1
		return moves

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

	# BFS
	def print():
		print("Graph: ")
		q = Queue()
		q.put(Graph.root)
		while(True):
			if(q.qsize() == 0):
				break
			cur_node = q.get()
			print(cur_node)
			for child in cur_node.children:
				q.put(child)
		print("Nodes: " + str(Graph.node_count))