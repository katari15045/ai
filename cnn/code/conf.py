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