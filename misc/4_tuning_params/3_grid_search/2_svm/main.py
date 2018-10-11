from sklearn.datasets import load_iris
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# Load Data
iris = load_iris()
X = iris.data
y = iris.target
print("Raw Data : " + str(X.shape) + " | " + str(y.shape))

# Make Parametres
params = {}
params["C"] = [2**(-5), 2**(-3), 2**(-1), 2**1, 2**3, 2**5, 2**7, 2**9, 2**11, 2**13, 2**15]
params["gamma"] = [2**(-15), 2**(-13), 2**(-11), 2**(-9), 2**(-7), 2**(-5), 2**(-3), 2**(-1), 2**1, 2**3]
params["kernel"] = ["linear", "poly", "rbf", "sigmoid"]
params["degree"] = [0, 1, 2, 3, 4, 5, 6]

# Perform Grid Search
model = SVC()
grid = GridSearchCV(model, params, cv=10, scoring="accuracy", n_jobs=-1, verbose=1)
grid.fit(X, y)
print("Best Accuracy : " + str(grid.best_score_))
print("Best Params : " + str(grid.best_params_))



