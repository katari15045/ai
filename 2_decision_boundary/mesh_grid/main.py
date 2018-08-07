import numpy
import matplotlib.pyplot as plot

start = 0
end = 3
step = .01

a, b = numpy.meshgrid(numpy.arange(start, end, step), numpy.arange(start, end, step));
plot.scatter(a, b)
plot.xlim(start, end)
plot.ylim(start, end)
plot.show()
