from matplotlib import pyplot
import numpy

bfs_nodes = [103, 2876, 236]
dfs_nodes = [7, 12, 9]

figure, axes = pyplot.subplots()
index = numpy.arange(len(bfs_nodes))
width = 0.44

axes.bar(index, bfs_nodes, width, label="BFS")
axes.bar(index+width, dfs_nodes, width, label="DFS")
pyplot.xticks(index+(width/2), ["n=3; colors=3", "n=4; colors=3", "n=3; colors=4"])

pyplot.xlabel("Grid details")
pyplot.ylabel("Max # of Nodes stored in Memory")
pyplot.title("Max # of Nodes stored by BFS and DFS for coloring puzzle")
pyplot.legend(loc="best")
pyplot.show()

