from hidden_layer import Hidden_Layer

class NN:

	def __init__(self, neuron_count, act_funcs, learning_rate, data):
		self.neuron_count = neuron_count
		self.act_funcs = act_funcs
		# Learning Rate: alpha in Gradient Descent i.e how big the step should be, while searching for minima of loss func
		self.learning_rate = learning_rate
		self.data = data
		self.init()

	def init(self):
		hid_layer_count = 0
		tot_hid_layers = len(self.neuron_count)
		self.hid_layers = []
		while(hid_layer_count < tot_hid_layers):
			# Adds a neuron for Bias
			tot_neurons = self.neuron_count[hid_layer_count]+1
			act_func = self.act_funcs[hid_layer_count]
			new_hid_layer = Hidden_Layer(tot_neurons, act_func)
			self.hid_layers.append(new_hid_layer)
			hid_layer_count = hid_layer_count+1

	def train(self):
		print("training...")
		self.feed_forward()

	def feed_forward(self):
		first_iter = True
		for sample in self.data:
			if(first_iter == True):
				first_iter = False
				input_ = sample[:len(sample)-1]
				print(input_)

	def __str__(self):
		return "NN..."