from sklearn.datasets import load_iris
from sklearn.prep

def stats(arr, tag):
    print(tag + " mean : " + str(arr.mean()))
    print(tag + " std : " + str(arr.std()))
    print(tag + " min : " + str(arr.min()))
    print(tag + " max : " + str(arr.max()))

# Get Data
print("Getting data...")
iris = load_iris()
x = iris.data
y = iris.target
stats(x, "x")
stats(y, "y")


