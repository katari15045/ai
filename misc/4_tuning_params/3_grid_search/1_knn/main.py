from sklearn.datasets import load_iris
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

# Load Data
iris = load_iris()
X = iris.data
y = iris.target
print("Raw Data : " + str(X.shape) + " | " + str(y.shape))

# Make Parametres
params = {}
params["n_neighbors"] = range(1, 31)
params["weights"] = ["uniform", "distance"]

# Perform Grid Search
knn = KNeighborsClassifier()
grid = GridSearchCV(knn, params, cv=10, scoring="accuracy", n_jobs=-1)
grid.fit(X, y)
print("Best Accuracy : " + str(grid.best_score_))
print("Best Params : " + str(grid.best_params_))



