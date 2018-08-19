from matplotlib import pyplot
import numpy

bfs_iter = [262, 181441]
dfs_iter = [39007, 181441]
a_star_iter = [262, 181441]
sma_iter = [262, 115650]

figure, axes = pyplot.subplots()
index = numpy.arange(len(bfs_iter))
width = 0.16

axes.bar(index, bfs_iter, width, label="BFS")
axes.bar(index+width, dfs_iter, width, label="DFS")
axes.bar(index+(2*width), a_star_iter, width, label="A*")
axes.bar(index+(3*width), sma_iter, width, label="SMA*")
pyplot.xticks(index+((3*width)/2), ["[[1, 8, 2][0, 4, 3][7, 6, 5]]", "[[8, 1, 2][0, 4, 3][7, 6, 5]]"])

pyplot.xlabel("Puzzle")
pyplot.ylabel("Iterations")
pyplot.title("n-Puzzle iterations with different Algo.s")
pyplot.legend(loc="best")
pyplot.show()

