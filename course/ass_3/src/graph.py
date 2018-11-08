from constants import Constants
from edge import Edge
import numpy
from random import randint
import networkx
from matplotlib import pyplot

# Fully Connected Graph i.e every node is connected to every other node
class Graph:

	@staticmethod
	def init():
		Graph.dist_matrix = []
		Graph.x_graph = networkx.Graph()
		# fill with 0s
		row = 0
		while(row < Constants.tot_cities):
			col = 0
			new_row = []
			while(col < row):
				dist = randint(1, Constants.max_dist)
				pheromone = col+2
				new_edge = Edge(dist, pheromone)
				new_row.append(new_edge)
				Graph.x_graph.add_edge(row, col, len_=dist, pheromone=pheromone)
				col = col+1
			Graph.dist_matrix.append(new_row)
			row = row+1
		fig = pyplot.figure()
		fig.patch.set_facecolor('#66ff99')
		pyplot.axis('off')
		pos = networkx.circular_layout(Graph.x_graph)
		nodes = Graph.x_graph.nodes()
		edges = Graph.x_graph.edges()
		edge_lens = networkx.get_edge_attributes(Graph.x_graph,'len_')
		edge_pheromones = networkx.get_edge_attributes(Graph.x_graph, 'pheromone')
		edge_pheromones = list(edge_pheromones.values())
		networkx.draw_networkx_nodes(Graph.x_graph, pos=pos, nodelist=nodes, node_color='g', node_size=300)
		networkx.draw_networkx_labels(Graph.x_graph, pos=pos, font_size=7, font_color='white')
		networkx.draw_networkx_edges(Graph.x_graph, pos=pos, edgelist=edges, width=edge_pheromones, edge_color='#00cc44')
		networkx.draw_networkx_edge_labels(Graph.x_graph, pos=pos, edge_labels=edge_lens, font_size=7, label_pos=0.4)
		pyplot.show()

	@staticmethod
	def print():
		row = 0
		while(row < Constants.tot_cities):
			col = 0
			while(col < row):
				print(Graph.dist_matrix[row][col])
				col = col+1
			row = row+1