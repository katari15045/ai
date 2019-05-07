from keras.datasets import mnist
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import numpy as np

class pre_processor:

	def get_data(self):
		(train_x, train_y), (test_x, test_y) = mnist.load_data()
		train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1]*train_x.shape[2]))
		test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1]*test_x.shape[2]))
		# Normalization
		scaler = MinMaxScaler()
		train_x = scaler.fit_transform(train_x)
		test_x = scaler.fit_transform(test_x)
		# One-hot encoding
		encoder = OneHotEncoder()
		train_y = np.reshape(train_y, (len(train_y), 1))
		test_y = np.reshape(test_y, (len(test_y), 1))
		train_y = encoder.fit_transform(train_y).toarray()
		test_y = encoder.fit_transform(test_y).toarray()
		# train-val split
		train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.2, random_state=33)
		print("train_x: {0}".format(train_x.shape))
		print("train_y: {0}".format(train_y.shape))
		print("val_x: {0}".format(val_x.shape))
		print("val_y: {0}".format(val_y.shape))
		print("test_x: {0}".format(test_x.shape))
		print("test_y: {0}".format(test_y.shape))
		return train_x, train_y, val_x, val_y, test_x, test_y