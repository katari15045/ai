from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# Load Data
iris = load_iris()
x = iris.data
y = iris.target
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=4)

# Train the model
knn = KNeighborsClassifier()
knn.fit(x_train, y_train)

# Predict
y_pred = knn.predict(x_test)
acc = metrics.accuracy_score(y_test, y_pred)
print(acc)






