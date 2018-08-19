from matplotlib import pyplot
import numpy

bfs_max_nodes = [175, 25136]
dfs_max_nodes = [26984, 42913]
a_star_max_nodes = [175, 25136]
sma_max_nodes = [175, 185]

figure, axes = pyplot.subplots()
index = numpy.arange(len(bfs_max_nodes))
width = 0.16

axes.bar(index, bfs_max_nodes, width, label="BFS")
axes.bar(index+width, dfs_max_nodes, width, label="DFS")
axes.bar(index+(2*width), a_star_max_nodes, width, label="A*")
axes.bar(index+(3*width), sma_max_nodes, width, label="SMA*")
pyplot.xticks(index+((3*width)/2), ["[[1, 8, 2][0, 4, 3][7, 6, 5]]", "[[8, 1, 2][0, 4, 3][7, 6, 5]]"])

pyplot.xlabel("Puzzle")
pyplot.ylabel("Max # of Nodes in Memory")
pyplot.title("n-Puzzle  Memory Analysis with different Algo.s")
pyplot.legend(loc="best")
pyplot.show()

