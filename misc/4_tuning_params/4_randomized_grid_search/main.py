from sklearn.datasets import load_iris
from sklearn.model_selection import RandomizedSearchCV
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
ran_sear = RandomizedSearchCV(knn, params, cv=10, scoring="accuracy", n_iter=10, n_jobs=-1)
ran_sear.fit(X, y)
print("Best Accuracy : " + str(ran_sear.best_score_))
print("Best Params : " + str(ran_sear.best_params_))
print("Means : " + str(ran_sear.cv_results_["mean_test_score"]))
