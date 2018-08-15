import matplotlib.pyplot as plt

scores = [0.96738095, 0.96190476, 0.9682619, 0.96714286, 0.96733333, 0.96666667,
            0.96642857, 0.96571429, 0.96511905, 0.96440476, 0.96347619, 0.96290476,
            0.96214286, 0.96128571, 0.96097619, 0.96014286, 0.95978571, 0.95883333,
            0.95883333, 0.95816667, 0.95759524, 0.95652381, 0.95592857, 0.95535714,
            0.9547619, 0.95442857, 0.95371429, 0.95328571, 0.95252381, 0.95207143]
k = range(1, 31)

plt.plot(k, scores)
plt.xlabel("K in KNN")
plt.ylabel("Accuracy")
plt.savefig('knn.png')