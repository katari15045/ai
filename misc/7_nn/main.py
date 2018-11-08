from neuron import Neuron
from hidden_layer import Hidden_Layer
from nn import NN
import numpy

# Static Members
class Main:
	def main():
		data = numpy.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]])
		nn_ = NN([8], ['sigmoid'], 0.5, data)
		nn_.train()

Main.main()