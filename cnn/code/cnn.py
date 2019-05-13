import tensorflow as tf
import numpy as np

class cnn:

	def conv(self, input, filter_rows, filter_cols, in_channels, out_channels, stride_rows, stride_cols, name, testing=False, graph=None):
		shape = [filter_rows, filter_cols, in_channels, out_channels]
		w_name = "w_" + name
		b_name = "b_" + name
		if(testing == True):
			weights = graph.get_tensor_by_name(w_name + ":0")
			biases = graph.get_tensor_by_name(b_name + ":0")
		else:
			weights = tf.Variable(tf.truncated_normal(shape, mean=self.init_weight_mean, stddev=self.init_weight_std), name=w_name)
			biases = tf.Variable(tf.constant(self.init_bias, shape=[out_channels]), name=b_name)
		layer = tf.nn.conv2d(input, filter=weights, strides=[1, stride_rows, stride_cols, 1], padding="SAME")
		layer = layer + biases
		return layer

	def max_pool(self, input, filter_rows, filter_cols, stride_rows, stride_cols):
		layer = tf.nn.max_pool(value=input, ksize=[1, filter_rows, filter_cols, 1], strides=[1, stride_rows, stride_cols, 1], padding="SAME")
		return layer

	def fc(self, input, num_inputs, num_outputs, name, testing=False, graph=None):
		shape = [num_inputs, num_outputs]
		w_name = "w_" + name
		b_name = "b_" + name
		if(testing == True):
			weights = graph.get_tensor_by_name(w_name + ":0")
			biases = graph.get_tensor_by_name(b_name + ":0")
		else:
			weights = tf.Variable(tf.truncated_normal(shape, mean=self.init_weight_mean, stddev=self.init_weight_std), name=w_name)
			biases = tf.Variable(tf.constant(self.init_bias, shape=[num_outputs]), name=b_name)
		layer = tf.matmul(input, weights) + biases
		return layer

	def __init__(self):

		self.tf_lyrs = []
		
		# parse conf/conf.txt
		book = open("../conf/conf.txt", "r")
		self.content = book.readlines()

		# collect network parameters from conf.txt
		self.conf_ind = 0
		self.img_rows = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
		self.conf_ind = self.conf_ind + 1
		self.img_cols = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
		self.conf_ind = self.conf_ind + 1
		self.img_channels = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
		self.conf_ind = self.conf_ind + 1
		self.classes = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
		self.conf_ind = self.conf_ind + 1
		self.epochs = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
		self.conf_ind = self.conf_ind + 1
		self.batch_size = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
		self.conf_ind = self.conf_ind + 1
		self.lr = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=True)
		self.conf_ind = self.conf_ind + 1
		self.init_bias = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=True)
		self.conf_ind = self.conf_ind + 1
		self.init_weight_mean = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=True)
		self.conf_ind = self.conf_ind + 1
		self.init_weight_std = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=True)
		self.conf_ind = self.conf_ind + 1
		self.optimizer_str = self.get_value_from_line(self.content[self.conf_ind], numeric=False, decimal=False)
		self.conf_ind = self.conf_ind + 1
		self.loss_str = self.get_value_from_line(self.content[self.conf_ind], numeric=False, decimal=False)
		# read "---"
		self.conf_ind = self.conf_ind + 1
		self.get_value_from_line(self.content[self.conf_ind], numeric=False, decimal=False)

		# initialize optimizer
		if(self.optimizer_str == "gd"):
			self.tf_optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.lr)
		else:
			# default optimizer; optimizer=adam
			self.tf_optimizer = tf.train.AdamOptimizer(learning_rate=self.lr)

		# place holders
		self.tf_X = tf.placeholder(tf.float32, shape=[None, self.img_rows, self.img_cols, self.img_channels], name="X")
		self.tf_y = tf.placeholder(tf.float32, shape=[None, self.classes])

	def forward_prop(self, testing=False, sess=None, meta_filepath=None, ckpt_filepath=None):

		if(testing == True):
			# restore from files
			saver = tf.train.import_meta_graph(meta_filepath)
			saver.restore(sess, ckpt_filepath)
			graph = tf.get_default_graph()
		else:
			graph = None

		# add input layer
		self.tf_lyrs.append(self.tf_X)
		first_fc = True
		conv_count = 0
		fc_count = 0

		while(True):

			self.conf_ind = self.conf_ind + 1
			layer = self.get_value_from_line(self.content[self.conf_ind], numeric=False)

			if(layer == "conv"):

				# parse conf.txt
				self.conf_ind = self.conf_ind + 1
				filter_rows_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				filter_cols_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				in_channels_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				out_channels_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				stride_rows_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				stride_cols_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				act = self.get_value_from_line(self.content[self.conf_ind], numeric=False)

				# prepare name
				conv_count = conv_count + 1
				name = "conv_" + str(conv_count)

				# define layer
				lyr = self.conv(input=self.tf_lyrs[-1], filter_rows=filter_rows_, filter_cols=filter_cols_, in_channels=in_channels_, out_channels=out_channels_, stride_rows=stride_rows_, stride_cols=stride_cols_, name=name, testing=testing, graph=graph)


			elif(layer == "max_pool"):

				# parse conf.txt
				self.conf_ind = self.conf_ind + 1
				filter_rows_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				filter_cols_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				stride_rows_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				stride_cols_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				act = self.get_value_from_line(self.content[self.conf_ind], numeric=False)

				# define layer
				lyr = self.max_pool(input=self.tf_lyrs[-1], filter_rows=filter_rows_, filter_cols=filter_cols_, stride_rows=stride_rows_, stride_cols=stride_cols_)

			elif(layer == "fc"):

				if(first_fc == True):
					# 1st FC layer
					first_fc = False
					# flatten data
					num_features = self.tf_lyrs[-1].shape[1:].num_elements()
					self.tf_lyrs[-1] = tf.reshape(self.tf_lyrs[-1], [-1, num_features])
					num_inputs_ = num_features
				else:
					# 1 or more FC layers are behind this layer
					num_inputs_ = neurons_ # the value of neurons_ in the previous iteration

				# parse conf.txt
				self.conf_ind = self.conf_ind + 1
				neurons_ = self.get_value_from_line(self.content[self.conf_ind], numeric=True, decimal=False)
				self.conf_ind = self.conf_ind + 1
				act = self.get_value_from_line(self.content[self.conf_ind], numeric=False)

				# prepare name
				fc_count = fc_count + 1
				name = "fc_" + str(fc_count)

				# define layer
				lyr = self.fc(input=self.tf_lyrs[-1], num_inputs=num_inputs_, num_outputs=neurons_, name=name, testing=testing, graph=graph)

			elif(layer == "none"):
				break

			# handle activation
			if(act == "relu"):
				lyr = tf.nn.relu(lyr)
			elif(act == "softmax"):
				lyr = tf.nn.softmax(lyr)

			# add current layer to existing layers
			self.tf_lyrs.append(lyr)

			# read "---"
			self.conf_ind = self.conf_ind + 1
			self.get_value_from_line(self.content[self.conf_ind], numeric=False, decimal=False)


	def compute_loss(self):

		if(self.loss_str == "mse"):
			self.tf_loss = tf.reduce_mean(tf.square(self.tf_lyrs[-1] - self.tf_y))
		else:
			# default loss; loss=softmax_crossentropy	
			self.tf_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.tf_y, logits=self.tf_lyrs[-1]))

	def compute_acc(self):
		# convert one-hot encoded labels to non-one-hot encoded labels
		self.tf_acc_, self.tf_acc = tf.metrics.accuracy(tf.argmax(self.tf_y, axis=1), tf.argmax(self.tf_lyrs[-1], axis=1))

	def back_prop(self):
		self.tf_train = self.tf_optimizer.minimize(self.tf_loss)

	def analyze_epoch(self, x, y, sess):

		iters = int( len(x) / self.batch_size )
		if(len(y) != 0):
			# accuracy, loss can only be computed when ground truth is available
			loss = []
			acc = []
		pred_y = np.array([]).reshape(0, self.classes)

		for iter_ in range(iters):
			# extract batch data
			batch_x = x[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			if(len(y) != 0):
				# ground truth is available
				batch_y = y[iter_*self.batch_size:(iter_+1)*self.batch_size, :]

			# forward propagation
			if(len(y) == 0):
				# ground truth is absent, can't compute accuracy
				batch_pred_y = sess.run(self.tf_lyrs[-1], 
													feed_dict={self.tf_X:batch_x})
			else:
				# ground truth is present, compute accuracy too
				batch_pred_y, batch_loss, batch_acc = sess.run([self.tf_lyrs[-1], self.tf_loss, self.tf_acc], 
													feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})

			# store epoch stats
			pred_y = np.concatenate((pred_y, batch_pred_y))

			if(len(y) != 0):
				# append only if ground truth is present; accuracy, loss can only be computed when ground truth is available
				loss.append(batch_loss)
				acc.append(batch_acc)

		# compute mean loss and mean accuracy
		if(len(y) != 0):
			# accuracy, loss can only be computed when ground truth is available
			acc = sum(acc) / len(acc)
			loss = sum(loss) / len(loss)
		else:
			# return acc=None, loss=None when ground truth is absent
			acc = None
			loss = None

		return pred_y, loss, acc

	def get_value_from_line(self, line, numeric=True, decimal=False):

		# remove newline character at the end of the line
		line = line.rstrip("\n")
		arr = line.split("=")

		# handle a case where there's no "="
		if(len(arr) <= 1):
			return None

		# ignore key (index 0) and extract value (index 1)
		value = arr[1]
		if(numeric == False):
			return value
		if(decimal == False):
			return int(value)
		return float(value)






