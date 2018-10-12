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

class Pruning:
	def tic_tac_toe():
		print("Starting...")
		Graph.init()
		print("Unique configs traversed: " + str(len(Graph.configs)))
		print("Nodes in Graph: " + str(Graph.node_count))
		print("1-indexing")
		node = Graph.root
		Node.print_grid(node.grid)
		#Graph.print()
		while(True):
			row, col = Pruning.take_input()
			print("User: ")
			grid = Node.get_grid(node.grid, row, col)
			Node.print_grid(grid)
			node = Graph.get_child(node, grid)
			if(Pruning.is_game_over(node) == True):
				return
			print("Computer: ")
			node = Graph.next_move(node)
			Node.print_grid(node.grid)
			if(Pruning.is_game_over(node) == True):
				return
		

	def is_game_over(node):
		complete, champ = Node.is_complete(node)
		if(complete == True):
			if(Constants.user == champ):
				print("User Won!")
			elif(Constants.computer == champ):
				print("Computer Won!")
			elif(Constants.tie == champ):
				print("Match Tied!")
			return True
		return False

	def take_input():
		row = int(input("\nRow: "))
		col = int(input("Col: "))
		return row, col

start_time = time()
Pruning.tic_tac_toe()
end_time = time()
elapsed_time = end_time - start_time
print("Execution time: " + str(elapsed_time) + " Seconds")