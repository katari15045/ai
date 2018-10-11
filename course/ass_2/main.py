import sys
from graph import Graph
from node import Node

'''
Assumptions:
	1st Player: X - user
	2nd Player: O - computer
	Grid: dim x dim matrix
'''

class Main:
	def main():
		grid = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'X']]
		root = Node(grid)
		is_complete_, player = root.is_complete()
		print(str(is_complete_) + " : " + player)
		Graph.init(root)
		Graph.print()
Main.main()