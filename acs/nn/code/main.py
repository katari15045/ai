from time import time
from pre_processor import pre_processor
from nn import nn

class main:

	@staticmethod
	def main():
		pre_proc = pre_processor()
		train_x, train_y, val_x, val_y, test_x, test_y = pre_proc.get_data()
		model = nn()
		model.train(train_x, train_y, val_x, val_y)
		pred_y = model.test(test_x, test_y)
		print("pred_y: {0}".format(pred_y.shape))

start_time = time()
main.main()
end_time = time()
elapsed_time = end_time - start_time
print("processed in {0} seconds".format(round(elapsed_time)))