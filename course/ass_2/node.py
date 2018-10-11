from constant import Constant

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
		while(row < Constant.dim):
			col = 0
			finished = False
			while(col < Constant.dim):
				if(col == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev):
						break
					prev = self.grid[row][col]
				if(col == (Constant.dim-1)):
					finished = True
					break
				col = col+1
			if(finished == True):
				return finished, prev
			row = row+1
		return finished, Constant.no_player

	def is_ver_line_present(self):
		col = 0
		while(col < Constant.dim):
			row = 0
			finished = False
			while(row < Constant.dim):
				if(row == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev):
						break
					prev = self.grid[row][col]
				if(row == (Constant.dim-1)):
					finished = True
				row = row+1
			if(finished == True):
				return finished, prev
			col = col+1
		return finished, Constant.no_player

	def is_cross_line_present(self):
		ind = 0
		while(ind < Constant.dim):
			if(ind == 0):
				prev = self.grid[ind][ind]
			else:
				if(self.grid[ind][ind] != prev):
					break
				prev = self.grid[ind][ind]
			if(ind == (Constant.dim-1)):
				return True, prev
			ind = ind+1
		row = 0
		col = Constant.dim-1
		while(row < Constant.dim):
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
		return False, Constant.no_player

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
		return False, Constant.no_player