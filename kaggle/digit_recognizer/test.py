from sklearn.externals import joblib
import pandas
from time import time

start_time = time()

# Load the Trained Model
print("Loading Tained Model...")
model = joblib.load("model.pkl")

# Get the test data
print("Getting Test data...")
data_frame = pandas.read_csv("test.csv")
data = data_frame.values
print(data.shape)

# Predict
print("Predicting...")
pred = model.predict(data)

# Store Predictions
print("Storing Predictions...")
book = open("pred.csv", "a")
count = 1
book.write("ImageId,Label\n")
while(count <= len(pred)):
    book.write(str(count) + "," + str(pred[count-1]) + "\n")
    count = count+1
book.close()

end_time = time()
elapsed_time = end_time-start_time
print(str(elapsed_time/60) + " minutes!")

