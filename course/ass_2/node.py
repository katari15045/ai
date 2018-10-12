from constants import Constants

class Node:

	def __init__(self, grid, parent, user_turn):
		self.grid = grid
		self.cost = -2
		self.parent = parent
		self.children = []
		self.user_turn = user_turn
		self.children_updated = 0
		self.other_parents = []

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

	def is_complete(self):
		is_present, player = self.is_hor_line_present()
		if( is_present == True ):
			self.update_cost(player)
			return True, player
		is_present, player = self.is_ver_line_present()
		if( is_present == True ):
			self.update_cost(player)
			return True, player
		is_present, player = self.is_cross_line_present()
		if( is_present == True ):
			self.update_cost(player)
			return True, player
		if( self.all_occupied() == True ):
			self.update_cost(Constants.tie)
			return True, Constants.tie
		return False, Constants.in_progress

	def update_cost(self, player):
		if(player == Constants.user):
			self.cost = 1
		elif(player == Constants.computer):
			self.cost = -1
		elif(player == Constants.tie):
			self.cost = 0
		self.update_ancestors_cost(player)


	def update_ancestors_cost(self, player):
		child = self
		while(True):
			if(child.parent == None):
				return
			child.parent.children_updated = child.parent.children_updated+1
			for other_parent in child.other_parents:
				other_parent.children_updated = other_parent.children_updated+1
			if(child.parent.children_updated == len(child.parent.children)):
				child.parent.update_cost(player)
				for other_parent in child.other_parents:
					if(other_parent.children_updated == len(other_parent.children)):
						other_parent.update_cost(player)
			else:
				break
			child = child.parent

	def update_ancestor_cost(self, parent):
		iter_1 = True
		for child in parent.children:
			if(iter_1 == True):
				iter_1 = False
				min_ = child.cost
				max_ = child.cost
			else:
				min_ = min(min_, child.cost)
				max_ = min(max_, child.cost)
		# User maximizes the cost
		if(parent.user_turn == True):
			parent.cost = max_
		else:
			parent.cost = min_


	def print(self):
		print("\n", end="")
		self.print_grid()
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

	def print_grid(self):
		row = 0
		while(row < Constants.dim):
			col = 0
			while(col < Constants.dim):
				print(str(self.grid[row][col]), end=" ")
				col = col+1
			print("\n", end="")
			row = row+1