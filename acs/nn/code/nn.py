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

		# weights
		self.tf_w1 = tf.Variable(self.tf_weight_initializer([self.dim_inp, self.dim_hid_1]), dtype=tf.float32)
		self.tf_w2 = tf.Variable(self.tf_weight_initializer([self.dim_hid_1, self.dim_hid_2]), dtype=tf.float32)
		self.tf_w3 = tf.Variable(self.tf_weight_initializer([self.dim_hid_2, self.dim_out]), dtype=tf.float32)

		# biases
		self.tf_b1 = tf.Variable(tf.zeros(self.dim_hid_1))
		self.tf_b2 = tf.Variable(tf.zeros(self.dim_hid_2))
		self.tf_b3 = tf.Variable(tf.zeros(self.dim_out))

		# input layer
		self.tf_X = tf.placeholder(tf.float32, shape=[None, self.dim_inp])

		# Hidden Layers
		self.tf_lyr_hid_1 = self.tf_act(tf.matmul(self.tf_X, self.tf_w1) + self.tf_b1)
		self.tf_lyr_hid_2 = self.tf_act(tf.matmul(self.tf_lyr_hid_1, self.tf_w2) + self.tf_b2)
		self.tf_lyr_out = self.tf_act(tf.matmul(self.tf_lyr_hid_2, self.tf_w3) + self.tf_b3)

		# loss
		self.tf_y = tf.placeholder(tf.float32, shape=[None, self.dim_out])
		# self.tf_loss = tf.reduce_mean(tf.square(self.tf_lyr_out - self.tf_y))
		self.tf_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.tf_lyr_out, labels=self.tf_y))

		# accuracy
		self.tf_acc_, self.tf_acc = tf.metrics.accuracy(tf.argmax(self.tf_y, axis=1), tf.argmax(self.tf_lyr_out, axis=1), name="tf_acc")

		# Back Prop
		# self.tf_optimizer = tf.train.GradientDescentOptimizer(self.lr)
		self.tf_optimizer = tf.train.AdamOptimizer()
		self.tf_train = self.tf_optimizer.minimize(self.tf_loss)

	def analyze_epoch(self, x, y):
		iters = int( len(x) / self.batch_size )
		loss = []
		acc = []
		pred_y = np.array([]).reshape(0, 10)
		for iter_ in range(iters):
			batch_x = x[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			batch_y = y[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
			batch_pred_y, batch_loss, batch_acc = self.sess.run([self.tf_lyr_out, self.tf_loss, self.tf_acc], 
													feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})
			pred_y = np.concatenate((pred_y, batch_pred_y))
			loss.append(batch_loss)
			acc.append(batch_acc)
		loss = sum(loss) / len(loss)
		acc = sum(acc) / len(acc)
		return pred_y, loss, acc

	def train(self, train_x, train_y, val_x, val_y):
		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())
		self.sess.run(tf.local_variables_initializer())

		saver = tf.train.Saver()
		for epoch in range(self.epochs):
			iters = int( len(train_x) / self.batch_size )
			for iter_ in range(iters):
				batch_x = train_x[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
				batch_y = train_y[iter_*self.batch_size:(iter_+1)*self.batch_size, :]
				self.sess.run(self.tf_train, feed_dict={self.tf_X:batch_x, self.tf_y:batch_y})
			# train loss
			_, loss_train, acc_train = self.analyze_epoch(train_x, train_y)
			# val loss
			_, loss_val, acc_val = self.analyze_epoch(val_x, val_y)
			print("epoch: {0}, loss_train: {1}, acc_train: {2}, loss_val: {3}, acc_val: {4}"
						.format(epoch+1, loss_train, acc_train, loss_val, acc_val))
		path = saver.save(self.sess, "model.ckpt")
		print("model saved in {0}".format(path))
		self.sess.close()

	def test(self, test_x, test_y):
		self.sess = tf.Session()
		saver = tf.train.Saver()
		saver.restore(self.sess, "model.ckpt")
		print("model restored")
		
		self.sess.run(tf.local_variables_initializer())

		# test
		pred_y, loss, acc = self.analyze_epoch(test_x, test_y)
		print("loss_test: {0}, acc_test: {1}".format(loss, acc))
		self.sess.close()
		return pred_y



