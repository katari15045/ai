from constants import Constants
import numpy
from random import randint

# Fully Connected Graph i.e every node is connected to every other node
class Graph:

	@staticmethod
	def init():
		Graph.dist_matrix = numpy.zeros((Constants.tot_cities, Constants.tot_cities), dtype='int64')
		# Fill lower diagonal cell
		row = 0
		while(row < Constants.tot_cities):
			col = 0
			while(col < row):
				Graph.dist_matrix[row][col] = randint(1, Constants.max_dist)
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