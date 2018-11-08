from neuron import Neuron

class Hidden_Layer:

	def __init__(self, neurons, act_func, bias=1):
		self.neurons = neurons
		self.act_func = act_func
		self.bias = bias
		self.init()

	def init(self):
		count_neurons = 0
		while(count_neurons < self.neurons):
			new_neuron = Neuron(None, self)
			count_neurons = count_neurons+1

	def __str__(self):
		return "Hidden Layer..."