import csv
import random

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_score
from sklearn.metrics import recall_score
from tqdm import trange
import matplotlib.pyplot as plt

def KMeans(x, k, no_of_iterations):
    cid = np.random.choice(len(x), k, replace=False)
    # choose random centroids
    centroids = x[cid, :]

    # distance between centroids and all the data points
    distances = cdist(x, centroids, 'euclidean')

    # Centroid with the minimum distance
    points = np.array([np.argmin(i) for i in distances])

    for times in trange(no_of_iterations):
        centroids = []
        for cid in range(k):
            # updating centroids by taking mean of cluster it belongs to
            temp_cent = x[points == cid].mean(axis=0)
            centroids.append(temp_cent)

        # updated centroids
        centroids = np.vstack(centroids)
        distances = cdist(x, centroids, 'euclidean')
        points = np.array([np.argmin(distance) for distance in distances])

    return points


def readPoints():
    points = []
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # Complete appending point (row1, row2) to points list
            points.append((row[1], row[2]))
    return points


if __name__ == "__main__":
    # load data
    data = readPoints()
    # Use skikit learns PCA s
    pca = PCA(2)

    # transform the data aka fit the model with X and apply the dimensionality reduction on X
    df = pca.fit_transform(data)

    label = KMeans(df, 4, 2000)
    u_labels = np.unique(label)
    for i in u_labels:
        # Complete the scatter plot

        plt.scatter( df[label == i, 0], df[label == i, 1], label=i)
    plt.legend()
    plt.show()

    preditictions = []

    points = []
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row[0])
            if(row[0] == 'A'):
                preditictions.append(0)
            if(row[0] == 'B' ):
                preditictions.append(1)
            if(row[0] == 'C'):
                preditictions.append(2)
            if(row[0] == 'D'):
                preditictions.append(3)
        # correct predictions / total number of predictions
    print(label)
    print("Accuracy: ", accuracy_score(label, preditictions) * 100)

    # correct positive predictions / all positive predictions
    print("Recall score: ", recall_score(label, preditictions, average="macro"))

    # correct positive predictions/ total positive predictions
    print("Precision: ", precision_score(label, preditictions, average="macro") * 100)