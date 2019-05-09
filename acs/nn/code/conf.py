import datetime
import logging

class conf:

	def __init__(self): 

		self.dim_lyrs = []
		self.dropout_rates = []

		# configure logging
		filename = "../logs/log.txt"
		handlers_ = [logging.FileHandler(filename, mode='a'), logging.StreamHandler()] # print on stdout too.
		logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=handlers_)
		logging.info("----------------------------------------------------------------")
		logging.info("{0} UTC".format(datetime.datetime.utcnow()))

	def get_value_from_line(self, line, numeric=True, decimal=False):

		# remove newline character at the end of the line
		line = line.rstrip("\n")
		arr = line.split("=")
		# ignore key (index 0) and extract value (index 1)
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

		# extract dimensions of each layer
		while(count < tot_lyrs ):
			cur_dim = self.get_value_from_line(content[count])
			self.dim_lyrs.append(cur_dim)
			count = count  + 1

		# extract parameters after first "---"
		base_index = tot_lyrs + 1
		self.batch_size = self.get_value_from_line(content[base_index])
		self.epochs = self.get_value_from_line(content[base_index+1])
		self.lr = self.get_value_from_line(content[base_index+2], decimal=True)
		self.act = self.get_value_from_line(content[base_index+3], numeric=False)
		self.last_layer_act = self.get_value_from_line(content[base_index+4], numeric=False)
		self.optimizer = self.get_value_from_line(content[base_index+5], numeric=False)
		self.loss = self.get_value_from_line(content[base_index+6], numeric=False)
		
		# dropout_rates
		arr = self.get_value_from_line(content[base_index+7], numeric=False)
		arr = arr.split(",")
		count = 0
		while(count < len(arr)):
			cur_rate = float(arr[count])
			self.dropout_rates.append(cur_rate)
			count = count + 1

		book.close()
		self.update_log()

	def update_log(self):
		logging.info("dim_lyrs: {0}".format(self.dim_lyrs))
		logging.info("batch_size: {0}".format(self.batch_size))
		logging.info("epochs: {0}".format(self.epochs))
		logging.info("lr: {0}".format(self.lr))
		logging.info("act: {0}".format(self.act))
		logging.info("last_layer_act: {0}".format(self.last_layer_act))
		logging.info("optimizer: {0}".format(self.optimizer))
		logging.info("loss: {0}".format(self.loss))
		logging.info("dropout_rates: {0}".format(self.dropout_rates))
