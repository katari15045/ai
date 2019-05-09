from conf import conf
import logging
import tensorflow as tf
from nn import nn
from pre_processor import pre_processor
from time import time

class train:

	def __init__(self):

		# load network configuration
		self.conf_ = conf()
		self.conf_.start()

		# get train data
		pre_proc = pre_processor()
		train_x, train_y, val_x, val_y = pre_proc.get_data()

		self.nn = nn(self.conf_)

		# Build Computation Graph
		self.nn.define_tensors()
		self.nn.forward_prop()
		self.nn.compute_loss()
		self.nn.compute_acc()
		self.nn.back_prop()

		# initialize tensors
		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())
		self.sess.run(tf.local_variables_initializer())

		# start training
		self.start(train_x, train_y, val_x, val_y)



	def start(self, train_x, train_y, val_x, val_y):

		logging.info("training...")
		self.saver = tf.train.Saver(max_to_keep=1)

		# core training
		for epoch in range(self.conf_.epochs):
			iters = int( len(train_x) / self.conf_.batch_size )

			for iter_ in range(iters):
				batch_x = train_x[iter_*self.conf_.batch_size:(iter_+1)*self.conf_.batch_size, :]
				batch_y = train_y[iter_*self.conf_.batch_size:(iter_+1)*self.conf_.batch_size, :]
				self.sess.run(self.nn.tf_train, feed_dict={self.nn.tf_X:batch_x, self.nn.tf_y:batch_y})

			# train loss
			_, loss_train, acc_train = self.nn.analyze_epoch(train_x, train_y, self.sess)

			# val loss
			_, loss_val, acc_val = self.nn.analyze_epoch(val_x, val_y, self.sess)

			# save model
			_ = self.saver.save(self.sess, "../models/sess", global_step=int(epoch+1))

			# log the performance at each epoch
			logging.info("epoch: {0}, loss_train: {1}, acc_train: {2}, loss_val: {3}, acc_val: {4}"
						.format(epoch+1, loss_train, acc_train, loss_val, acc_val))

		self.sess.close()

start_time = time()

training = train()

end_time = time()
elapsed_time = end_time - start_time
logging.info("processed in {0} seconds".format(round(elapsed_time)))
print("done")