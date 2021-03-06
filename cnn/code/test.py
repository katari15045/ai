from conf import conf
import logging
import tensorflow as tf
from cnn import cnn
from pre_processor import pre_processor
from time import time

class test:

	def __init__(self):
		
		# load network configuration
		self.conf_ = conf()

		# get test data
		pre_proc = pre_processor()
		test_x, test_y = pre_proc.get_data(testing=True)

		self.sess = tf.Session()

		# Build Computation Graph
		self.cnn = cnn()
		meta_filepath = "../models/sess-" + str(self.cnn.epochs) + ".meta"
		ckpt_filepath = "../models/sess-" + str(self.cnn.epochs)
		self.cnn.forward_prop(testing=True, sess=self.sess, meta_filepath=meta_filepath, ckpt_filepath=ckpt_filepath)
		self.cnn.compute_loss()
		self.cnn.compute_acc()

		# Initialize local variables only (not global variables)
		self.sess.run(tf.local_variables_initializer())

		# start testing
		self.start(test_x, test_y)



	def start(self, test_x, test_y):

		# core testing
		logging.info("testing...")
		pred_y, loss, acc = self.cnn.analyze_epoch(test_x, test_y, self.sess)

		# post testing
		self.sess.close()
		if(acc == None and loss == None):
			logging.info("pred_y: {0},  can't compute acc and loss; ground truth is absent".format(pred_y.shape))
		else:
			logging.info("pred_y: {0}, acc: {1}, loss: {2}".format(pred_y.shape, acc, loss))

		return pred_y, acc, loss

start_time = time()

testing = test()

end_time = time()
elapsed_time = end_time - start_time
logging.info("processed in {0} seconds".format(round(elapsed_time)))
print("done")