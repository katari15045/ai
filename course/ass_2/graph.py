from node import Node
from queue import Queue

class Graph:
	root = None

	def init(root):
		Graph.root = root

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
