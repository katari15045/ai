from matplotlib import pyplot
import numpy

bfs_iter = [289, 12598, 675]
dfs_iter = [312, 12642, 706]

figure, axes = pyplot.subplots()
index = numpy.arange(len(bfs_iter))
width = 0.44

axes.bar(index, bfs_iter, width, label="BFS")
axes.bar(index+width, dfs_iter, width, label="DFS")
pyplot.xticks(index+(width/2), ["n=3; colors=3", "n=4; colors=3", "n=3; colors=4"])

pyplot.xlabel("Grid details")
pyplot.ylabel("Iterations")
pyplot.title("# of iterations by BFS and DFS for coloring puzzle")
pyplot.legend(loc="best")
pyplot.show()
