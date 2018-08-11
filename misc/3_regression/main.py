from sklearn.decomposition import PCA
import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Get Data
print("Getting data....")
data = pandas.read_csv('https://raw.githubusercontent.com/nguyen-toan/ISLR/master/dataset/Advertising.csv', index_col=0)
print("Raw Data : " + str(data.shape))

y = data['Sales']
X = data[['TV', 'Newspaper', 'Radio']]
print("x : " + str(X.shape))
print("y : " + str(y.shape))

# Reduce Dimensions
pca = PCA(n_components=1)
X = pca.fit_transform(X)
print("Post PCA, X : " + str(X.shape))

# Scatter Data Points
plt.scatter(X, y)

# Train Model
lr = LinearRegression()
lr.fit(X, y)
print("Coef : " + str(lr.intercept_))
print("Intercept : " + str(lr.coef_))

# Plot Regression Line
axes = plt.gca()
x_line = np.array(axes.get_xlim())
slope = lr.coef_
intercept = lr.intercept_
y_line = (slope*x_line)+intercept
plt.plot(x_line, y_line, '-')
plt.show()
