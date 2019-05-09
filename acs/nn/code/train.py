from conf import conf
import logging
import tensorflow as tf
from nn import nn

class train:

	def __init__(self, conf_):
		self.nn = nn(conf_)

		# Build Computation Graph
		self.nn.define_tensors()
		self.nn.forward_prop()
		self.nn.compute_loss()
		self.nn.compute_acc()
		self.nn.back_prop()

		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())
		self.sess.run(tf.local_variables_initializer())

	def start(self, train_x, train_y, val_x, val_y):
		logging.info("training...")
		for epoch in range(self.nn.conf_.epochs):
			iters = int( len(train_x) / self.nn.conf_.batch_size )
			for iter_ in range(iters):
				batch_x = train_x[iter_*self.nn.conf_.batch_size:(iter_+1)*self.nn.conf_.batch_size, :]
				batch_y = train_y[iter_*self.nn.conf_.batch_size:(iter_+1)*self.nn.conf_.batch_size, :]
				self.sess.run(self.nn.tf_train, feed_dict={self.nn.tf_X:batch_x, self.nn.tf_y:batch_y})
			# train loss
			_, loss_train, acc_train = self.nn.analyze_epoch(train_x, train_y, self.sess)
			# val loss
			_, loss_val, acc_val = self.nn.analyze_epoch(val_x, val_y, self.sess)
			logging.info("epoch: {0}, loss_train: {1}, acc_train: {2}, loss_val: {3}, acc_val: {4}"
						.format(epoch+1, loss_train, acc_train, loss_val, acc_val))
		self.save_models()
		self.sess.close()

	def save_models(self):
		self.saver = tf.train.Saver()
		path = self.saver.save(self.sess, "models/sess.ckpt")
		logging.info("train session saved in {0}".format(path))