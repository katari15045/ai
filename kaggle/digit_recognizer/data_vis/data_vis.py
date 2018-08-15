from time import time
import pandas
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

start_time = time()

# Get Data
print("Getting Data...")
data_frame = pandas.read_csv("train.csv")
data = data_frame.values
x = data[:, 1:]
y = data[:, 0]
print("x : " + str(x.shape))
print("y : " + str(y.shape))

# Reduce Dimensions
print("Reducing Dimensions ...")
pca = PCA(n_components=2)
x_2_dim = pca.fit_transform(x)
print("Post PCA x : " + str(x_2_dim.shape))

# Plotting Data
print("Plotting Data ...")
plt.scatter(x_2_dim[:, 0], x_2_dim[:, 1], c=y, s=50)
plt.savefig("plot.png")


end_time = time()
elapsed_time = end_time-start_time
print(str(elapsed_time/60) + " minutes!")
