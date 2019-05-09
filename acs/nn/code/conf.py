import datetime
import logging

class conf:

	def __init__(self): 
		self.dim_lyrs = []
		filename = "../logs/log.txt"
		logging.basicConfig(filename=filename, filemode='a', level=logging.INFO, format='%(message)s')
		logging.info("----------------------------------------------------------------")
		logging.info(datetime.datetime.utcnow())

	def get_value_from_line(self, line, numeric=True, decimal=False):
		line = line.rstrip("\n")
		arr = line.split("=")
		value = arr[1]
		if(numeric == False):
			return value
		if(decimal == False):
			return int(value)
		return float(value)

	def start(self):
		# parse conf/conf.txt
		book = open("../conf/conf.txt", "r")
		content = book.readlines()
		tot_lyrs = content.index("---\n")
		# hidden layers = all layers except input layer
		self.tot_hid_lyrs = tot_lyrs - 1
		count = 0
		while(count < tot_lyrs ):
			cur_dim = self.get_value_from_line(content[count])
			self.dim_lyrs.append(cur_dim)
			count = count  + 1
		base_index = tot_lyrs + 1
		self.batch_size = self.get_value_from_line(content[base_index])
		self.epochs = self.get_value_from_line(content[base_index+1])
		self.lr = self.get_value_from_line(content[base_index+2], decimal=True)
		self.act = self.get_value_from_line(content[base_index+3], numeric=False)
		self.weight_initializer = self.get_value_from_line(content[base_index+4], numeric=False)
		self.optimizer = self.get_value_from_line(content[base_index+5], numeric=False)
		self.loss = self.get_value_from_line(content[base_index+6], numeric=False)
		book.close()
		self.update_log()

	def update_log(self):
		logging.info("dim_lyrs: {0}".format(self.dim_lyrs))
		logging.info("batch_size: {0}".format(self.batch_size))
		logging.info("epochs: {0}".format(self.epochs))
		logging.info("lr: {0}".format(self.lr))
		logging.info("act: {0}".format(self.act))
		logging.info("weight_initializer: {0}".format(self.weight_initializer))
