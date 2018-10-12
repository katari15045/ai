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
		print("Starting...")
		Graph.init()
		node = Graph.root
		Node.print_grid(node.grid)
		while(True):
			row, col = Minimax.take_input()
			print("User: ")
			grid = Node.get_grid(node.grid, row, col)
			Node.print_grid(grid)
			node = Graph.get_child(node, grid)
			if(Minimax.is_game_over(node) == True):
				return
			print("Computer: ")
			node = Graph.next_move(node)
			Node.print_grid(node.grid)
			if(Minimax.is_game_over(node) == True):
				return
		#Graph.print()
		#print("Nodes: " + str(len(Graph.configs)))

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
Minimax.tic_tac_toe()
end_time = time()
elapsed_time = end_time - start_time
print("Execution time: " + str(elapsed_time) + " Seconds")