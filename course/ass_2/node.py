from constants import Constants

class Node:

	def __init__(self, grid):
		self.grid = grid
		self.cost = 0
		self.parent = None
		self.children = []

	def __str__(self):
		return str(self.cost) + "\n" + str(self.grid) + "\n-------------"

	def is_hor_line_present(self):
		row = 0
		while(row < Constants.dim):
			col = 0
			finished = False
			while(col < Constants.dim):
				if(col == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev):
						break
					prev = self.grid[row][col]
				if(col == (Constants.dim-1)):
					finished = True
					break
				col = col+1
			if(finished == True):
				return finished, prev
			row = row+1
		return finished, Constants.no_player

	def is_ver_line_present(self):
		col = 0
		while(col < Constants.dim):
			row = 0
			finished = False
			while(row < Constants.dim):
				if(row == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev):
						break
					prev = self.grid[row][col]
				if(row == (Constants.dim-1)):
					finished = True
				row = row+1
			if(finished == True):
				return finished, prev
			col = col+1
		return finished, Constants.no_player

	def is_cross_line_present(self):
		ind = 0
		while(ind < Constants.dim):
			if(ind == 0):
				prev = self.grid[ind][ind]
			else:
				if(self.grid[ind][ind] != prev):
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
				if(self.grid[row][col] != prev):
					break
				prev = self.grid[row][col]
			if(col == 0):
				return True, prev
			row = row+1
			col = col-1
		return False, Constants.no_player

	def is_complete(self):
		is_present, player = self.is_hor_line_present()
		if( is_present == True ):
			return is_present, player
		is_present, player = self.is_ver_line_present()
		if( is_present == True ):
			return is_present, player
		is_present, player = self.is_cross_line_present()
		if( is_present == True ):
			return is_present, player
		return False, Constants.no_player