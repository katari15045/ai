import tensorflow as tf
import numpy as np

class nn:

	def __init__(self, conf_):

		self.conf_ = conf_

		# activation
		if(self.conf_.act == "sigmoid"):
			self.tf_act = tf.nn.sigmoid
		elif(self.conf_.act == "tanh"):
			self.tf_act = tf.nn.tanh
		else:
			# default activation; act=relu
			self.tf_act = tf.nn.relu 

		# last layer activation
		if(self.conf_.last_layer_act == "sigmoid"):
			self.tf_last_lyr_act = tf.nn.sigmoid
		elif(self.conf_.last_layer_act == "tanh"):
			self.tf_last_lyr_act = tf.nn.tanh
		elif(self.conf_.last_layer_act == "relu"):
			self.tf_last_lyr_act = tf.nn.relu
		else:
			# default activation; last_layer_act=softmax
			self.tf_last_lyr_act = tf.nn.softmax

		# weight initializer
		self.tf_weight_initializer = tf.initializers.random_normal()

		# optimizer
		if(self.conf_.optimizer == "adam"):
			self.tf_optimizer = tf.train.AdamOptimizer(learning_rate=self.conf_.lr)
		else:
			# default optimizer; optimizer=gd
			self.tf_optimizer = tf.train.GradientDescentOptimizer(self.conf_.lr) 

		# loss: refer self.compute_loss()


	def define_tensors(self):

		# weights
		self.tf_weights = []
		ind = 0
		while(ind < self.conf_.tot_hid_lyrs):
			cur_dim = [self.conf_.dim_lyrs[ind], self.conf_.dim_lyrs[ind+1]]
			cur_name = "w" + str(ind+1)
			cur_tensor = tf.Variable(self.tf_weight_initializer(cur_dim, dtype=tf.float32), name=cur_name)
			self.tf_weights.append(cur_tensor)
			ind = ind + 1
		
		# biases
		self.tf_biases = []
		ind = 1
		while(ind <= self.conf_.tot_hid_lyrs):
			cur_dim = self.conf_.dim_lyrs[ind]
			cur_name = "b" + str(ind)
			cur_tensor = tf.Variable(tf.zeros(cur_dim), name=cur_name)
			self.tf_biases.append(cur_tensor)
			ind = ind + 1

		# input layer
		dim_inp = self.conf_.dim_lyrs[0]
		self.tf_X = tf.placeholder(tf.float32, shape=[None, dim_inp], name="X")

		# Ground Truth
		dim_out = self.conf_.dim_lyrs[-1]
		self.tf_y = tf.placeholder(tf.float32, shape=[None, dim_out], name="y")

	def restore_tensors(self, sess, meta_filepath, ckpt_filepath):

		# restore from files
		saver = tf.train.import_meta_graph(meta_filepath)
		saver.restore(sess, ckpt_filepath)
		graph = tf.get_default_graph()

		# weights
		self.tf_weights = []
		count = 1
		while(count <= self.conf_.tot_hid_lyrs):
			cur_name = "w" + str(count) + ":0"
			cur_tensor = graph.get_tensor_by_name(cur_name)
			self.tf_weights.append(cur_tensor)
			count = count + 1

		# biases
		self.tf_biases = []
		count = 1
		while(count <= self.conf_.tot_hid_lyrs):
			cur_name = "b" + str(count) + ":0"
			cur_tensor = graph.get_tensor_by_name(cur_name)
			self.tf_biases.append(cur_tensor)
			count = count + 1

		# input layer
		self.tf_X = graph.get_tensor_by_name("X:0")

		# Ground Truth
		self.tf_y = graph.get_tensor_by_name("y:0")

	def forward_prop(self, testing=False):

		# traverse through each layer
		self.tf_lyrs = []
		count = 0
		while(count < self.conf_.tot_hid_lyrs):
			# Extract Input
			if(count == 0):
				# input layer
				cur_inp = self.tf_X
			else:
				# take previous layer's output as input
				cur_inp = self.tf_lyrs[-1]

			# Extract Weights and Biases
			cur_weight = self.tf_weights[count]
			cur_bias = self.tf_biases[count]


			if(count == (self.conf_.tot_hid_lyrs-1)):
				# last layer: tf_last_lyr_act, no dropout
				cur_tensor = self.tf_last_lyr_act(tf.matmul(cur_inp, cur_weight) + cur_bias)
			else:
				# no tf_act, dropout  
				cur_tensor = self.tf_act(tf.matmul(cur_inp, cur_weight) + cur_bias)
				# dropout during training
				if(testing == False):
					cur_dropout_rate = self.conf_.dropout_rates[count]
					cur_tensor = tf.nn.dropout(cur_tensor, rate=cur_dropout_rate)
			self.tf_lyrs.append(cur_tensor)
			count = count + 1

	def compute_loss(self):

		if(self.conf_.loss == "softmax_crossentropy"):
			self.tf_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.tf_y, logits=self.tf_lyrs[-1]))
		elif(self.conf_.loss == "sigmoid_crossentropy"):
			self.tf_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=self.tf_y, logits=self.tf_lyrs[-1]))
		else:
			# default loss; loss=mse
			self.tf_loss = tf.reduce_mean(tf.square(self.tf_lyrs[-1] - self.tf_y))

	def compute_acc(self):

		# convert one-hot encoded labels to non-one-hot encoded labels
		self.tf_acc_, self.tf_acc = tf.metrics.accuracy(tf.argmax(self.tf_y, axis=1), tf.argmax(self.tf_lyrs[-1], axis=1), name="tf_acc")

	def back_prop(self):

		self.tf_train = self.tf_optimizer.minimize(self.tf_loss)

	def analyze_epoch(self, x, y, sess):

		iters = int( len(x) / self.conf_.batch_size )
		loss = []
		acc = []
		pred_y = np.array([]).reshape(0, self.conf_.dim_lyrs[-1])

		for iter_ in range(iters):
			# extract batch data
			batch_x = x[iter_*self.conf_.batch_size:(iter_+1)*self.conf_.batch_size, :]
			batch_y = y[iter_*self.conf_.batch_size:(iter_+1)*self.conf_.batch_size, :]

			# forward propagation
			batch_pred_y, batch_loss, batch_acc = sess.run([self.tf_lyrs[-1], self.tf_loss, self.tf_acc], 
													feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})

			# store epoch stats
			pred_y = np.concatenate((pred_y, batch_pred_y))
			loss.append(batch_loss)
			acc.append(batch_acc)

		# compute mean loss and mean accuracy
		loss = sum(loss) / len(loss)
		acc = sum(acc) / len(acc)
		return pred_y, loss, acc