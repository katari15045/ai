from time import time
from pre_processor import pre_processor
from train import train
from test import test
from conf import conf
import logging

class main:

	@staticmethod
	def main():
		conf_ = conf()
		conf_.start()
		pre_proc = pre_processor()
		train_x, train_y, val_x, val_y, test_x, test_y = pre_proc.get_data()
		training = train(conf_)
		training.start(train_x, train_y, val_x, val_y)
		testing = test(conf_)
		pred_y, acc, loss = testing.start(test_x, test_y)

start_time = time()
main.main()
end_time = time()
elapsed_time = end_time - start_time
logging.info("processed in {0} seconds".format(round(elapsed_time)))
print("done")