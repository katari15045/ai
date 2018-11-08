class Edge:

	def __init__(self, len_, pheromone):
		self.len_ = len_
		self.pheromone = pheromone

	def __str__(self):
		return "len: " + str(self.len_) + ", pheromone: " + str(self.pheromone)