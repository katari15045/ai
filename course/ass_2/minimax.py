import sys
from graph import Graph
from node import Node
from constants import Constants

'''
Assumptions:
	1st Player: X - user
	2nd Player: O - computer
	Grid: dim x dim matrix
'''

class Minimax:
	def tic_tac_toe():
		Graph.init()
		Graph.print()

Minimax.tic_tac_toe()