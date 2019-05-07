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
		self.batch_size = 256
		self.epochs = 30
		self.lr = 0.0001
		self.tf_act = tf.nn.relu
		self.tf_weight_initializer = tf.initializers.random_normal()

		# weights
		self.tf_w1 = tf.Variable(self.tf_weight_initializer([self.dim_inp, self.dim_hid_1]), dtype=tf.float32)
		self.tf_w2 = tf.Variable(self.tf_weight_initializer([self.dim_hid_1, self.dim_hid_2]), dtype=tf.float32)
		self.tf_w3 = tf.Variable(self.tf_weight_initializer([self.dim_hid_2, self.dim_out]), dtype=tf.float32)

		# biases
		self.tf_b1 = tf.Variable(tf.zeros(self.dim_hid_1))
		self.tf_b2 = tf.Variable(tf.zeros(self.dim_hid_2))
		self.tf_b3 = tf.Variable(tf.zeros(self.dim_out))

		self.tf_y = tf.placeholder(tf.float32, shape=[None, self.dim_out])

		# input layer
		self.tf_X = tf.placeholder(tf.float32, shape=[None, self.dim_inp])

		# Hidden Layers
		self.tf_lyr_hid_1 = self.tf_act(tf.matmul(self.tf_X, self.tf_w1) + self.tf_b1)
		self.tf_lyr_hid_2 = self.tf_act(tf.matmul(self.tf_lyr_hid_1, self.tf_w2) + self.tf_b2)
		self.tf_lyr_out = self.tf_act(tf.matmul(self.tf_lyr_hid_2, self.tf_w3) + self.tf_b3)

		# self.tf_loss = tf.reduce_mean(tf.square(self.tf_lyr_out - self.tf_y))
		self.tf_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.tf_lyr_out, labels=self.tf_y))
		# self.tf_optimizer = tf.train.GradientDescentOptimizer(self.lr)
		self.tf_optimizer = tf.train.AdamOptimizer()
		self.tf_train = self.tf_optimizer.minimize(self.tf_loss)

	def compute_loss(self, x, y):
		iters = int( len(x) / self.batch_size )
		losses = []
		for iter_ in range(iters):
			batch_x = x[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			batch_y = y[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			loss = self.sess.run(self.tf_loss, feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})
			losses.append(loss)
		loss = sum(losses) / len(losses)
		return loss

	def train(self, train_x, train_y, val_x, val_y):
		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())
		saver = tf.train.Saver()
		for epoch in range(self.epochs):
			iters = int( len(train_x) / self.batch_size )
			for iter_ in range(iters):
				batch_x = train_x[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
				batch_y = train_y[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
				self.sess.run(self.tf_train, feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})
			# train loss
			loss_train = self.compute_loss(train_x, train_y)
			print("epoch: {0}, loss_train: {1}".format(epoch+1, loss_train))
			# val loss
			loss_val = self.compute_loss(val_x, val_y)
			print("epoch: {0}, loss_val: {1}".format(epoch+1, loss_val))
		path = saver.save(self.sess, "model.ckpt")
		print("model saved in {0}".format(path))
		self.sess.close()

	def test(self, test_x, test_y):
		self.sess = tf.Session()
		saver = tf.train.Saver()
		saver.restore(self.sess, "model.ckpt")
		print("model restored")
		iters = int( len(test_x) / self.batch_size )
		pred_ys = []
		losses = []
		for iter_ in range(iters):
			batch_x = test_x[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			batch_y = test_y[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			loss = self.sess.run(self.tf_loss, feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})
			losses.append(loss)
			pred_y = self.sess.run(self.tf_lyr_out, feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})
			pred_ys.append(pred_y)
		loss = sum(losses) / len(losses)
		print("loss_test: {0}".format(loss))
		self.sess.close()
		return np.array(pred_ys)



