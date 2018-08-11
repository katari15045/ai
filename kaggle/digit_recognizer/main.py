import pandas
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# Get data
data_frame = pandas.read_csv("train.csv")
data = data_frame.values
x = data[:, 1:]
y = data[:, 0]
print("x : " + str(x.shape))
print("y : " + str(y.shape))
x_train, x_test, y_train, y_test = train_test_split(x, y)

# Reduce Dimensions
pca = PCA(n_components=2)
x_2_dim = pca.fit_transform(x)
print("Post PCA, X : " + str(x_2_dim.shape))

# Plot Data
plt.scatter(x_2_dim[:, 0], x_2_dim[:, 1], c=y, s=50)
plt.show()

# Train the model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train)

# Predict
y_pred = knn.predict(x_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy : " + str(accuracy))

