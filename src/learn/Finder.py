import os.path

import numpy as np
from joblib import load, dump
from sklearn import neighbors


class Finder:
    def __init__(self):
        self.prediction = None
        self.trained = False
        if os.path.isfile('knn_clf.joblib'):
            self.clf = load('knn_clf.joblib')
        else:
            self.clf = neighbors.KNeighborsClassifier(n_neighbors=1)

    def save(self):
        dump(self.clf, 'knn_clf.joblib')

    def __call__(self):
        return "ahahahhaha"

    def train(self, data):
        # data[0] = AP1 , AP2, ... , zone
        X = list()
        y = list()
        if len(data) <= 1:
            print("Not enough data to train")
            return
        for e in data:
            X.append(e[:-1])
            y.append(e[-1])


        X = np.asarray(X)
        y = np.asarray(y)
        print("_________data for training_________")
        print(X)
        print(y)
        print("_________data for training_________")
        self.clf.fit(X, y)
        self.trained = True
        print("Finder correctly trained")

    def predict(self, data):
        if self.trained is False:
            print("Can't give localisation without training")
            return
        data = np.asarray(data)
        self.prediction = self.clf.predict(data.reshape(1, -1))
