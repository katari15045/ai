import tensorflow as tf
import numpy as np

class cnn:

	def conv(self, input, filter_rows, filter_cols, in_channels, out_channels, stride_rows, stride_cols):
		shape = [filter_rows, filter_cols, in_channels, out_channels]
		# weights = tf.Variable(self.tf_weight_initializer(shape, dtype=tf.float32))
		weights = tf.Variable(tf.truncated_normal(shape, stddev=0.05))
		biases = tf.Variable(tf.constant(self.conf_.init_bias, shape=[out_channels]))
		layer = tf.nn.conv2d(input, filter=weights, strides=[1, stride_rows, stride_cols, 1], padding="SAME")
		layer = layer + biases
		return layer

	def max_pool(self, input, filter_rows, filter_cols, stride_rows, stride_cols):
		layer = tf.nn.max_pool(value=input, ksize=[1, filter_rows, filter_cols, 1], strides=[1, stride_rows, stride_cols, 1], padding="SAME")
		return layer

	def fc(self, input, num_inputs, num_outputs):
		shape = [num_inputs, num_outputs]
		# weights = tf.Variable(self.tf_weight_initializer(shape, dtype=tf.float32))
		weights = tf.Variable(tf.truncated_normal(shape, stddev=0.05))
		biases = tf.Variable(tf.constant(self.conf_.init_bias, shape=[num_outputs]))
		layer = tf.matmul(input, weights) + biases
		return layer

	def __init__(self, conf):
		self.conf_ = conf

		self.tf_optimizer = tf.train.AdamOptimizer(learning_rate=self.conf_.lr)
		self.tf_weight_initializer = tf.initializers.random_normal()

		# place holders
		self.tf_X = tf.placeholder(tf.float32, shape=[None, self.conf_.img_rows, self.conf_.img_cols, self.conf_.img_channels], name="X")
		self.tf_y = tf.placeholder(tf.float32, shape=[None, self.conf_.dim_out])

		# define computation graph

		# block-1
		self.tf_conv1 = self.conv(input=self.tf_X, filter_rows=5, filter_cols=5, in_channels=1, out_channels=6, stride_rows=1, stride_cols=1)
		self.tf_maxpool1 = self.max_pool(input=self.tf_conv1, filter_rows=2, filter_cols=2, stride_rows=2, stride_cols=2)
		self.tf_relu1 = tf.nn.relu(self.tf_maxpool1)

		# block-2
		self.tf_conv2 = self.conv(input=self.tf_relu1, filter_rows=5, filter_cols=5, in_channels=6, out_channels=16, stride_rows=1, stride_cols=1)
		self.tf_maxpool2 = self.max_pool(input=self.tf_conv2, filter_rows=2, filter_cols=2, stride_rows=2, stride_cols=2)
		self.tf_relu2 = tf.nn.relu(self.tf_maxpool2)

		# flatten
		num_features = self.tf_relu2.shape[1:].num_elements()
		self.tf_flatten = tf.reshape(self.tf_relu2, [-1, num_features])

		# FC-1
		self.tf_fc1 = self.fc(input=self.tf_flatten, num_inputs=num_features, num_outputs=128)
		self.tf_relu3 = tf.nn.relu(self.tf_fc1)

		# FC-2
		self.tf_fc2 = self.fc(input=self.tf_relu3, num_inputs=128, num_outputs=10)
		self.tf_softmax = tf.nn.softmax(self.tf_fc2)

		# loss
		self.tf_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.tf_y, logits=self.tf_softmax))

		# accuracy
		# convert one-hot encoded labels to non-one-hot encoded labels
		self.tf_acc_, self.tf_acc = tf.metrics.accuracy(tf.argmax(self.tf_y, axis=1), tf.argmax(self.tf_softmax, axis=1))

		# Back Prop
		self.tf_train = self.tf_optimizer.minimize(self.tf_loss)

	def analyze_epoch(self, x, y, sess):

		iters = int( len(x) / self.conf_.batch_size )
		if(len(y) != 0):
			# accuracy, loss can only be computed when ground truth is available
			loss = []
			acc = []
		pred_y = np.array([]).reshape(0, self.conf_.dim_out)

		for iter_ in range(iters):
			# extract batch data
			batch_x = x[iter_*self.conf_.batch_size:(iter_+1)*self.conf_.batch_size, :]
			if(len(y) != 0):
				# ground truth is available
				batch_y = y[iter_*self.conf_.batch_size:(iter_+1)*self.conf_.batch_size, :]

			# forward propagation
			if(len(y) == 0):
				# ground truth is absent, can't compute accuracy
				batch_pred_y = sess.run(self.tf_softmax, 
													feed_dict={self.tf_X:batch_x})
			else:
				# ground truth is present, compute accuracy too
				batch_pred_y, batch_loss, batch_acc = sess.run([self.tf_softmax, self.tf_loss, self.tf_acc], 
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






