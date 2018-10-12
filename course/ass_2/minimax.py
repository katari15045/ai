import sys
from graph import Graph
from node import Node
from constants import Constants
from time import time

'''
Assumptions:
	1st Player: X - user
	2nd Player: O - computer
	Grid: dim x dim matrix
'''

class Minimax:
	def tic_tac_toe():
		Graph.init()
		#Graph.print()
		print("Nodes: " + str(Graph.node_count))

start_time = time()
Minimax.tic_tac_toe()
end_time = time()
elapsed_time = end_time - start_time
print("Execution time: " + str(elapsed_time) + " Seconds")