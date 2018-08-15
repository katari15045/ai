from sklearn.externals import joblib
from time import time
import pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

start_time = time()

# Get data
print("Getting data...")
data_frame = pandas.read_csv("train.csv")
data = data_frame.values
x = data[:, 1:]
y = data[:, 0]
print("x : " + str(x.shape))
print("y : " + str(y.shape))

# Find Best Parametres
print("Finding best params...")
params = {}
params["n_neighbors"] = range(1, 31)
knn = KNeighborsClassifier()
grid = GridSearchCV(knn, params, cv=10, scoring="accuracy", n_jobs=-1, verbose=1)
grid.fit(x, y)
print("Grid Scores : " + str(grid.cv_results_["mean_test_score"]))
print("Best Accuracy : " + str(grid.best_score_))
print("Best Params : " + str(grid.best_params_))
best_model = grid.best_estimator_

# Save Model
print("Saving Model...")
joblib.dump(best_model, "model.pkl")

end_time = time()
elapsed_time = end_time-start_time
print(str(elapsed_time/60) + " minutes!")

