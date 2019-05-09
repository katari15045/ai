
from time import time
from pre_processor import pre_processor
from train import train
from test import test

class main:

	@staticmethod
	def main():
		pre_proc = pre_processor()
		train_x, train_y, val_x, val_y, test_x, test_y = pre_proc.get_data()
		training = train()
		training.start(train_x, train_y, val_x, val_y)
		testing = test()
		pred_y, acc, loss = testing.start(test_x, test_y)
		print("pred_y: {0}, acc: {1}, loss: {2}".format(pred_y.shape, acc, loss))

start_time = time()
main.main()
end_time = time()
elapsed_time = end_time - start_time
print("processed in {0} seconds".format(round(elapsed_time)))