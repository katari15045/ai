import tensorflow as tf
from cnn import cnn
from pre_processor import pre_processor
from conf import conf
import logging
from time import time

class train:

	def __init__(self):
		self.conf_ = conf()

		pre_processor_ = pre_processor()
		train_x, train_y, val_x, val_y = pre_processor_.get_data()

		# Build Computation Graph
		self.cnn = cnn()
		self.cnn.forward_prop()
		self.cnn.compute_loss()
		self.cnn.compute_acc()
		self.cnn.back_prop()

		# initialize tensors
		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())
		self.sess.run(tf.local_variables_initializer())

		logging.info("training...")
		self.saver = tf.train.Saver(max_to_keep=1)

		for epoch in range(self.cnn.epochs):

			iters = int( len(train_x) / self.cnn.batch_size )

			for iter_ in range(iters):

				# extract batch data
				batch_x = train_x[iter_*self.cnn.batch_size:(iter_+1)*self.cnn.batch_size, :]
				batch_y = train_y[iter_*self.cnn.batch_size:(iter_+1)*self.cnn.batch_size, :]

				# train
				self.sess.run(self.cnn.tf_train, feed_dict={self.cnn.tf_X: batch_x, self.cnn.tf_y: batch_y})

			# train loss
			_, loss_train, acc_train = self.cnn.analyze_epoch(train_x, train_y, self.sess)

			# val loss
			_, loss_val, acc_val = self.cnn.analyze_epoch(val_x, val_y, self.sess)

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
