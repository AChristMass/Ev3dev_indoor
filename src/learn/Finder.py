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
            self.clf = neighbors.KNeighborsClassifier(n_neighbors=3)

    def save(self):
        dump(self.clf, 'knn_clf.joblib')

    def __call__(self):
        return "ahahahhaha"

    def train(self, data):
        # data[0] = AP1 , AP2, ... , zone
        X = list()
        y = list()
        for e in data:
            X.append(e[:-1])
            y.append(e[-1])

        X = np.asarray(X)
        y = np.asarray(y)
        self.clf.fit(X, y)
        self.trained = True
        print("Finder correctly trained")

    def predict(self, data):
        if self.trained is False:
            print("Can't give localisation without training")
            return
        self.prediction = self.clf.predict(data.reshape(1, -1))
