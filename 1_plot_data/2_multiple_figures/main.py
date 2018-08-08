import pandas
import matplotlib.pyplot as plt

# Get Data
print("Getting data....")
data = pandas.read_csv('https://raw.githubusercontent.com/nguyen-toan/ISLR/master/dataset/Advertising.csv', index_col=0)
print("Raw Data : " + str(data.shape))

y = data['Sales']
list_x = ['TV', 'Radio', 'Newspaper']

# Plot Data
count = 1
for x_label in list_x:
	fig = plt.figure(count)
	x = data[x_label]
	plt.scatter(x, y)
	plt.xlabel(x_label)
	plt.ylabel("Sales")
	plt.title(x_label + " Vs Sales")
	count = count+1
plt.show()
