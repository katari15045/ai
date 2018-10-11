from node import Node
from queue import Queue
from constants import Constants

# Everything here is STATIC
class Graph:
	root = None

	def init():
		empty_grid = Graph.get_empty_grid()
		Graph.root = Node(empty_grid)

	def get_empty_grid():
		grid = []
		row = 0
		while(row < Constants.dim):
			col = 0
			row_ = []
			while(col < Constants.dim):
				row_.append(Constants.no_player)
				col = col+1
			grid.append(row_)
			row = row+1
		return grid

	# BFS
	def print():
		q = Queue()
		q.put(Graph.root)
		while(True):
			if(q.qsize() == 0):
				break
			cur_node = q.get()
			print(cur_node)
			ind = 0
			while(ind < len(cur_node.children)):
				q.put(cur_node.children[ind])
