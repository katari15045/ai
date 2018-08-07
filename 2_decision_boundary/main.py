from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
import matplotlib.pyplot as plot
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
import numpy

# Load Iris Data set 
iris = load_iris()
X = iris.data
responses = iris.target

# Reduce the dimensions to 2
pca = PCA(n_components=2)
X = pca.fit_transform(X);

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X, responses)

# Dimensions of the meshgrid
x_min = X[:, 0].min()-1
x_max = X[:, 0].max()+1
y_min = X[:, 1].min()-1
y_max = X[:, 1].max()+1
step = 0.02

# Create a meshgrid with the above dimensions
xx, yy = numpy.meshgrid(numpy.arange(x_min, x_max, step), numpy.arange(y_min, y_max, step))

# Predict the class of each point in the meshgrid
y_pred = knn.predict(numpy.c_[xx.ravel(), yy.ravel()])
y_pred = y_pred.reshape(xx.shape)

cmap_light = ListedColormap(['#bf634c', '#65bc6b', '#8785e2'])
cmap_dark = ListedColormap(['#e00808', '#087f18', '#12197a'])

# Plot the Background mesh, the light colored background other than the data points
plot.pcolormesh(xx, yy, y_pred, cmap=cmap_light)

# Plot the data points
plot.scatter(X[:, 0], X[:, 1], c=responses, cmap=cmap_dark, s=18)

plot.xlim(xx.min(), xx.max())
plot.ylim(yy.min(), yy.max())
plot.xlabel("Principal Component 1")
plot.ylabel("Principal Component 2")
plot.title("KNN with Iris dataset")
plot.show()
                
