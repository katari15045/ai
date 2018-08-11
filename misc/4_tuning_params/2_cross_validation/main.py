from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

# Import Data
iris = load_iris()
X = iris.data
y = iris.target
print("Raw data -> " + str(X.shape))

# Cross Validation
neigh_list = range(1, 31)
scores_list = []
for neigh in neigh_list:
	knn = KNeighborsClassifier(n_neighbors=neigh)
	scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
	scores_list.append(scores.mean())

# Plot Results
plt.plot(neigh_list, scores_list)
plt.xlabel("Nearest Neighbors")
plt.ylabel("Score")
plt.show()





                                                                                                                                                                            
