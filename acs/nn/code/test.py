import tensorflow as tf
from nn import nn

class test:

	def __init__(self):
		self.nn = nn()
		self.sess = tf.Session()

		# Build Computation Graph
		self.nn.restore_tensors(self.sess, "models/sess.ckpt.meta", "models/sess.ckpt")
		self.nn.forward_prop()
		self.nn.compute_loss()
		self.nn.compute_acc()

		self.sess.run(tf.local_variables_initializer())

	def start(self, test_x, test_y):
		pred_y, loss, acc = self.nn.analyze_epoch(test_x, test_y, self.sess)
		self.sess.close()
		return pred_y, acc, loss