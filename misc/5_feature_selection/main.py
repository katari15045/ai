import numpy as np
import pandas
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

def eval(X, y):
	lr = LinearRegression()
	mse_list = cross_val_score(lr, X, y, cv=10, scoring='neg_mean_squared_error')
	mse_list = -mse_list
	rmse_list = np.sqrt(mse_list)
	rmse = rmse_list.mean()
	return rmse


# Get Data
print("Getting data....")
data = pandas.read_csv('https://raw.githubusercontent.com/nguyen-toan/ISLR/master/dataset/Advertising.csv', index_col=0)
print("Raw Data : " + str(data.shape))

# Parse data
y = data['Sales']
X_1 = data[['TV', 'Newspaper', 'Radio']]
X_2 = data[['TV', 'Radio']]

# Test 1 : Including all Features
rmse_1 = eval(X_1, y)
print("RMSE : " + str(rmse_1))

# Test 2 : Without the feature - Newspaper
rmse_2 = eval(X_2, y)
print("RMSE without Newspaper Feature : " + str(rmse_2))

print("\nLower the RMSE, better the Model\n")



