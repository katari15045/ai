from constants import Constants
from copy import deepcopy

class Node:

	def __init__(self, grid, parent, user_turn):
		self.grid = grid
		self.cost = -2
		self.parent = parent
		self.children = []
		self.user_turn = user_turn
		self.children_updated = 0
		self.other_parents = []
		self.at_least = -2
		self.at_most = -2
		self.at_least_valid = False
		self.at_most_valid = False

	def is_hor_line_present(self):
		row = 0
		while(row < Constants.dim):
			col = 0
			finished = False
			while(col < Constants.dim):
				if(col == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev or self.grid[row][col] == Constants.unoccupied):
						break
					prev = self.grid[row][col]
				if(col == (Constants.dim-1)):
					finished = True
					break
				col = col+1
			if(finished == True):
				return finished, prev
			row = row+1
		return finished, Constants.in_progress

	def is_ver_line_present(self):
		col = 0
		while(col < Constants.dim):
			row = 0
			finished = False
			while(row < Constants.dim):
				if(row == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev or self.grid[row][col] == Constants.unoccupied):
						break
					prev = self.grid[row][col]
				if(row == (Constants.dim-1)):
					finished = True
				row = row+1
			if(finished == True):
				return finished, prev
			col = col+1
		return False, Constants.in_progress

	def is_cross_line_present(self):
		ind = 0
		while(ind < Constants.dim):
			if(ind == 0):
				prev = self.grid[ind][ind]
			else:
				if(self.grid[ind][ind] != prev or self.grid[ind][ind] == Constants.unoccupied):
					break
				prev = self.grid[ind][ind]
			if(ind == (Constants.dim-1)):
				return True, prev
			ind = ind+1
		row = 0
		col = Constants.dim-1
		while(row < Constants.dim):
			if(row == 0):
				prev = self.grid[row][col]
			else:
				if(self.grid[row][col] != prev or self.grid[row][col] == Constants.unoccupied):
					break
				prev = self.grid[row][col]
			if(col == 0):
				return True, prev
			row = row+1
			col = col-1
		return False, Constants.in_progress

	def all_occupied(self):
		row = 0
		while(row < Constants.dim):
			col = 0
			while(col < Constants.dim):
				if(self.grid[row][col] == Constants.unoccupied):
					return False
				col = col+1
			row = row+1
		return True

	def is_complete(node):
		is_present, player = node.is_hor_line_present()
		if( is_present == True ):
			node.update_cost(player)
			return True, player
		is_present, player = node.is_ver_line_present()
		if( is_present == True ):
			node.update_cost(player)
			return True, player
		is_present, player = node.is_cross_line_present()
		if( is_present == True ):
			node.update_cost(player)
			return True, player
		if( node.all_occupied() == True ):
			node.update_cost(Constants.tie)
			return True, Constants.tie
		return False, Constants.in_progress

	def update_cost(self, player):
		if(player == Constants.user):
			self.cost = Constants.user_optimal_cost
		elif(player == Constants.computer):
			self.cost = Constants.computer_optimal_cost
		elif(player == Constants.tie):
			self.cost = Constants.tie_cost
		self.update_ancestors_cost()
		self.update_parent_constraints(self)

	def update_parent_constraints(self, base_node):
		if(base_node.parent == None):
			return
		parent = base_node.parent
		if(parent.user_turn == True):
			# Tries to maximize the cost; constraint = 'at least'; update only if new cost is more than the constraint
			if(parent.at_least_valid == True and base_node.cost > parent.at_least):
				parent.at_least = base_node.cost
			if(parent.at_least_valid == False):
				parent.at_least_valid = True
				parent.at_least = base_node.cost
		else:
			# Tries to minimize the cost; constraint = 'at most'; update only if new cost is less than the constraint
			if(parent.at_most_valid == True and base_node.cost < parent.at_most):
				parent.at_most = base_node.cost
			if(parent.at_most_valid == False):
				parent.at_most_valid = True
				parent.at_most = base_node.cost

	def update_ancestors_cost(self):
		if(self.parent == None):
			return
		self.parent.children_updated = self.parent.children_updated+1
		if(self.parent.children_updated == len(self.parent.children)):
			self.update_ancestor_cost(self.parent)
			self.parent.update_ancestors_cost()
		for other_parent in self.other_parents:
			other_parent.children_updated = other_parent.children_updated+1
			if(other_parent.children_updated == len(other_parent.children)):
				self.update_ancestor_cost(other_parent)
				other_parent.update_ancestors_cost()
				

	def update_ancestor_cost(self, parent):
		iter_1 = True
		for child in parent.children:
			if(iter_1 == True):
				iter_1 = False
				min_ = child.cost
				max_ = child.cost
			else:
				min_ = min(min_, child.cost)
				max_ = max(max_, child.cost)
		# User maximizes the cost
		if(parent.user_turn == True):
			parent.cost = max_
		else:
			parent.cost = min_
		self.update_parent_constraints(parent)

	def print(self):
		print("\n", end="")
		node.print_grid(self.grid)
		if(self.user_turn == True):
			print("Next Turn: " + str(Constants.user))
		else:
			print("Next Turn: " + str(Constants.computer))
		print("Cost: " + str(self.cost))
		if(self.parent != None):
			print("Parent's cost: " + str(self.parent.cost))
		else:
			print("Parent: None")
		print("children updated: " + str(self.children_updated))
		print("Total children: " + str(len(self.children)))

	def print_grid(grid):
		row = 0
		while(row < Constants.dim):
			col = 0
			while(col < Constants.dim):
				print(str(grid[row][col]), end=" ")
				col = col+1
			print("\n", end="")
			row = row+1

	def get_grid(grid, row, col):
		row = row-1
		col = col-1
		grid_copy = deepcopy(grid)
		grid_copy[row][col] = Constants.user
		return grid_copy
