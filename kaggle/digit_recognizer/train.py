from sklearn.externals import joblib
from time import time
import pandas
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV

start_time = time()

# Get data
print("Getting data...")
data_frame = pandas.read_csv("train.csv")
data = data_frame.values
x = data[:, 1:]
y = data[:, 0]
print("x : " + str(x.shape))
print("y : " + str(y.shape))
x_train, x_test, y_train, y_test = train_test_split(x, y)

'''
# Reduce Dimensions
print("Reducing Dimensions...")
pca = PCA(n_components=2)
x_2_dim = pca.fit_transform(x)
print("Post PCA, X : " + str(x_2_dim.shape))

# Plot Data

print("Plotting Data...")
plt.scatter(x_2_dim[:, 0], x_2_dim[:, 1], c=y, s=50)
plt.savefig("data.png")
'''

# Find Best Parametres
print("Finding best params...")
params = {}
params["n_neighbors"] = range(1, 31)
knn = KNeighborsClassifier()
grid = RandomizedSearchCV(knn, params, cv=10, scoring="accuracy", n_jobs=-1, n_iter=16, verbose=1)
grid.fit(x, y)
print("Best Accuracy : " + str(grid.best_score_))
print("Best Params : " + str(grid.best_params_))
best_model = grid.best_estimator_

# Save Model
print("Saving Model...")
joblib.dump(best_model, "model.pkl")

end_time = time()
elapsed_time = end_time-start_time
print(str(elapsed_time/60) + " minutes!")

