from constants import Constants
from edge import Edge
import numpy
from random import randint

# Fully Connected Graph i.e every node is connected to every other node
class Graph:

	@staticmethod
	def init():
		Graph.dist_matrix = []
		# fill with 0s
		row = 0
		while(row < Constants.tot_cities):
			col = 0
			new_row = []
			while(col < Constants.tot_cities):
				new_edge = Edge(0, 0)
				new_row.append(new_edge)
				col = col+1
			Graph.dist_matrix.append(new_row)
			row = row+1
		# Fill lower diagonal cells
		row = 0
		while(row < Constants.tot_cities):
			col = 0
			while(col < row):
				dist = randint(1, Constants.max_dist)
				Graph.dist_matrix[row][col].len_ = dist
				col = col+1
			row = row+1
		# Fill Upper diagonal cells
		row = 0
		while(row < Constants.tot_cities):
			col = row+1
			while(col < Constants.tot_cities):
				Graph.dist_matrix[row][col] = Graph.dist_matrix[col][row]
				col = col+1
			row = row+1

	@staticmethod
	def print():
		row = 0
		while(row < Constants.tot_cities):
			col = 0
			while(col < Constants.tot_cities):
				print(Graph.dist_matrix[row][col])
				col = col+1
			row = row+1