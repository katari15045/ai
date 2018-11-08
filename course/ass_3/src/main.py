from constants import Constants
from graph import Graph

class Main:

	@staticmethod
	def main():
		Graph.init()
		print(Graph.dist_matrix)

Main.main()