from sklearn.externals import joblib
from time import time
import pandas
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

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

# Reduce Dimensions
print("Reducing Dimensions...")
pca = PCA(n_components=2)
x_2_dim = pca.fit_transform(x)
print("Post PCA, X : " + str(x_2_dim.shape))

# Plot Data
print("Plotting Data...")
plt.scatter(x_2_dim[:, 0], x_2_dim[:, 1], c=y, s=50)
plt.show()

# Train the model
print("Training Model...")
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train)

# Save Model
print("Saving Model...")
joblib.dump(knn, "model.pkl")

# Predict
print("Predicting...")
y_pred = knn.predict(x_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy : " + str(accuracy))

# Store Predictions
print("Storing Predictions...")
book = open("pred.txt", "a")
count = 1
book.write("ImageId,Label\n")
while(count <= len(y_pred)):
    book.write(str(count) + "," + str(y_pred[count-1]) + "\n")
    count = count+1
book.close()

end_time = time()
elapsed_time = end_time-start_time
print(str(elapsed_time/60) + " minutes!")

