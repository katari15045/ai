from constant import constant

class node:
	grid = []
	cost = 0

	def __init__(self, grid):
		self.grid = grid

	def is_hor_line_present(self):
		row = 0
		while(row < constant.dim):
			col = 0
			finished = False
			while(col < constant.dim):
				if(col == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev):
						break
					prev = self.grid[row][col]
				if(col == (constant.dim-1)):
					finished = True
					break
				col = col+1
			if(finished == True):
				return finished, prev
			row = row+1
		return finished, constant.no_player

	def is_ver_line_present(self):
		col = 0
		while(col < constant.dim):
			row = 0
			finished = False
			while(row < constant.dim):
				if(row == 0):
					prev = self.grid[row][col]
				else:
					if(self.grid[row][col] != prev):
						break
					prev = self.grid[row][col]
				if(row == (constant.dim-1)):
					finished = True
				row = row+1
			if(finished == True):
				return finished, prev
			col = col+1
		return finished, constant.no_player

	def is_cross_line_present(self):
		ind = 0
		while(ind < constant.dim):
			if(ind == 0):
				prev = self.grid[ind][ind]
			else:
				if(self.grid[ind][ind] != prev):
					break
				prev = self.grid[ind][ind]
			if(ind == (constant.dim-1)):
				return True, prev
			ind = ind+1
		row = 0
		col = constant.dim-1
		while(row < constant.dim):
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
		return False, constant.no_player

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
		return False, constant.no_player