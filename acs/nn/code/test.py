from conf import conf
import logging
import tensorflow as tf
from nn import nn
from pre_processor import pre_processor
from time import time

class test:

	def __init__(self):
		
		# load network configuration
		self.conf_ = conf()
		self.conf_.start()

		# get test data
		pre_proc = pre_processor()
		test_x, test_y = pre_proc.get_data(testing=True)

		self.nn = nn(self.conf_)
		self.sess = tf.Session()

		# Build Computation Graph
		self.nn.restore_tensors(self.sess, "models/sess.ckpt.meta", "models/sess.ckpt")
		self.nn.forward_prop(testing=True)
		self.nn.compute_loss()
		self.nn.compute_acc()

		# Initialize local variables only (not global variables)
		self.sess.run(tf.local_variables_initializer())

		# start testing
		self.start(test_x, test_y)



	def start(self, test_x, test_y):

		# core testing
		logging.info("testing...")
		pred_y, loss, acc = self.nn.analyze_epoch(test_x, test_y, self.sess)

		# post testing
		self.sess.close()
		logging.info("pred_y: {0}, acc: {1}, loss: {2}".format(pred_y.shape, acc, loss))

		return pred_y, acc, loss

start_time = time()

testing = test()

end_time = time()
elapsed_time = end_time - start_time
logging.info("processed in {0} seconds".format(round(elapsed_time)))
print("done")