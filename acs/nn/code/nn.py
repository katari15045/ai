import tensorflow as tf
import numpy as np

class nn:

	def __init__(self):
		# layers
		self.dim_inp = 28*28
		self.dim_hid_1 = 64
		self.dim_hid_2 = 32
		self.dim_out = 10

		# Network Parameters
		self.batch_size = 32
		self.epochs = 3
		self.lr = 0.001
		self.tf_act = tf.nn.relu
		self.tf_weight_initializer = tf.initializers.random_normal()

	def define_tensors(self):
		# weights
		self.tf_w1 = tf.Variable(self.tf_weight_initializer([self.dim_inp, self.dim_hid_1]), dtype=tf.float32, name="w1")
		self.tf_w2 = tf.Variable(self.tf_weight_initializer([self.dim_hid_1, self.dim_hid_2]), dtype=tf.float32, name="w2")
		self.tf_w3 = tf.Variable(self.tf_weight_initializer([self.dim_hid_2, self.dim_out]), dtype=tf.float32, name="w3")

		# biases
		self.tf_b1 = tf.Variable(tf.zeros(self.dim_hid_1), name="b1")
		self.tf_b2 = tf.Variable(tf.zeros(self.dim_hid_2), name="b2")
		self.tf_b3 = tf.Variable(tf.zeros(self.dim_out), name="b3")

		# input layer
		self.tf_X = tf.placeholder(tf.float32, shape=[None, self.dim_inp], name="X")

		# Ground Truth
		self.tf_y = tf.placeholder(tf.float32, shape=[None, self.dim_out], name="y")

	def restore_tensors(self, sess, meta_filepath, ckpt_filepath):
		saver = tf.train.import_meta_graph(meta_filepath)
		saver.restore(sess, ckpt_filepath)
		graph = tf.get_default_graph()

		# weeights
		self.tf_w1 = graph.get_tensor_by_name("w1:0")
		self.tf_w2 = graph.get_tensor_by_name("w2:0")
		self.tf_w3 = graph.get_tensor_by_name("w3:0")

		# biases
		self.tf_b1 = graph.get_tensor_by_name("b1:0")
		self.tf_b2 = graph.get_tensor_by_name("b2:0")
		self.tf_b3 = graph.get_tensor_by_name("b3:0")

		# input layer
		self.tf_X = graph.get_tensor_by_name("X:0")

		# Ground Truth
		self.tf_y = graph.get_tensor_by_name("y:0")

	def forward_prop(self):
		# Hidden Layers
		self.tf_lyr_hid_1 = self.tf_act(tf.matmul(self.tf_X, self.tf_w1) + self.tf_b1)
		self.tf_lyr_hid_2 = self.tf_act(tf.matmul(self.tf_lyr_hid_1, self.tf_w2) + self.tf_b2)
		self.tf_lyr_out = self.tf_act(tf.matmul(self.tf_lyr_hid_2, self.tf_w3) + self.tf_b3)

	def compute_loss(self):
		# self.tf_loss = tf.reduce_mean(tf.square(self.tf_lyr_out - self.tf_y))
		self.tf_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.tf_lyr_out, labels=self.tf_y))

	def compute_acc(self):
		self.tf_acc_, self.tf_acc = tf.metrics.accuracy(tf.argmax(self.tf_y, axis=1), tf.argmax(self.tf_lyr_out, axis=1), name="tf_acc")

	def back_prop(self):
		# self.tf_optimizer = tf.train.GradientDescentOptimizer(self.lr)
		self.tf_optimizer = tf.train.AdamOptimizer()
		self.tf_train = self.tf_optimizer.minimize(self.tf_loss)

	def analyze_epoch(self, x, y, sess):
		iters = int( len(x) / self.batch_size )
		loss = []
		acc = []
		pred_y = np.array([]).reshape(0, 10)
		for iter_ in range(iters):
			batch_x = x[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			batch_y = y[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			batch_pred_y, batch_loss, batch_acc = sess.run([self.tf_lyr_out, self.tf_loss, self.tf_acc], 
													feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})
			pred_y = np.concatenate((pred_y, batch_pred_y))
			loss.append(batch_loss)
			acc.append(batch_acc)
		loss = sum(loss) / len(loss)
		acc = sum(acc) / len(acc)
		return pred_y, loss, acc