import datetime
import logging

class conf:

	def __init__(self):
		# configure logging
		filename = "../logs/log.txt"
		handlers_ = [logging.FileHandler(filename, mode='a'), logging.StreamHandler()] # print on stdout too.
		logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=handlers_)
		logging.info("----------------------------------------------------------------")
		logging.info("{0} UTC".format(datetime.datetime.utcnow()))

		# cnn parameters
		self.epochs = 100
		self.batch_size = 100
		self.lr = 0.0001
		self.init_bias = 0.05
		self.img_rows = 28
		self.img_cols = 28
		self.img_channels = 1
		self.dim_out = 10