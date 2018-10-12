from constants import Constants

class Node:

	def __init__(self, grid, parent, user_turn):
		self.grid = grid
		self.cost = -2
		self.parent = parent
		self.children = []
		self.user_turn = user_turn
		self.children_updated = 0

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
			self.update_cost(player)
			return True, Constants.tie
		return False, Constants.in_progress

	def update_cost(self, player):
		if(player == 'X'):
			self.cost = 1
		elif(player == 'O'):
			self.cost = -1
		self.update_ancestors_cost()


	def update_ancestors_cost(self):
		child = self
		# Update Ancestors' cost
		while(True):
			if(child.parent == None):
				return
			child.parent.children_updated = child.parent.children_updated+1
			if(child.parent.children_updated == len(child.parent.children)):
				iter_1 = True
				for child in child.parent.children:
					if(iter_1 == True):
						iter_1 = False
						min_ = child.cost
						max_ = child.cost
					else:
						min_ = min(min_, child.cost)
						max_ = min(max_, child.cost)
				# User maximizes the cost
				if(child.parent.user_turn == True):
					child.parent.cost = max_
				else:
					child.parent.cost = min_
				child = child.parent
			else:
				break


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

	def print_grid(self):
		row = 0
		while(row < Constants.dim):
			col = 0
			while(col < Constants.dim):
				print(str(self.grid[row][col]), end=" ")
				col = col+1
			print("\n", end="")
			row = row+1