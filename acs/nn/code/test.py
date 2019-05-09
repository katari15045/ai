from conf import conf
import logging
import tensorflow as tf
from nn import nn

class test:

	def __init__(self, conf_):
		self.nn = nn(conf_)
		self.sess = tf.Session()

		# Build Computation Graph
		self.nn.restore_tensors(self.sess, "models/sess.ckpt.meta", "models/sess.ckpt")
		self.nn.forward_prop(testing=True)
		self.nn.compute_loss()
		self.nn.compute_acc()

		self.sess.run(tf.local_variables_initializer())

	def start(self, test_x, test_y):
		logging.info("testing...")
		pred_y, loss, acc = self.nn.analyze_epoch(test_x, test_y, self.sess)
		self.sess.close()
		logging.info("pred_y: {0}, acc: {1}, loss: {2}".format(pred_y.shape, acc, loss))
		return pred_y, acc, loss