from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

iris = load_iris()
X = iris.data
y = iris.target
print("Raw data -> " + str(X.shape))

# PCA : n-dimensional data to 2-dimensional data
pca = PCA(n_components=2)
X = pca.fit_transform(X);
print("Post PCA -> " + str(X.shape))

plt.scatter(X[:, 0], X[:, 1], c=y, s=50)
plt.show()
