import os.path

import numpy as np
from joblib import load, dump
from sklearn import linear_model
from sklearn import neighbors
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor


class Finder:
    """A Finder is an object who can perform machine learning algorithm,
    you can feed it with data, train it and use it to predict one or more values from data"""

    def __init__(self):
        """The Finder is initialized with a classifier using knn"""
        self.prediction = None
        self.trained = False
        if os.path.isfile('knn_alg.joblib'):
            self.alg = load('knn_alg.joblib')
        else:
            self.alg = neighbors.KNeighborsClassifier(n_neighbors=3)

    # ____________ML_algorithm_Setter____________
    # Check out the link in each description for more informations

    def set_classifier_knn(self, k):
        """https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html"""
        self.alg = neighbors.KNeighborsClassifier(n_neighbors=k)

    def set_classifier_RandomForest(self, n):
        """https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html"""
        self.alg = RandomForestClassifier(n_estimators=n)

    def set_classifier_SVC(self):
        """https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html"""
        self.alg = svm.SVC(gamma='scale')

    def set_regressor_knn(self, k):
        """https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html"""
        self.alg = KNeighborsRegressor(n_neighbors=k, weights="uniform")

    def set_regressor_lasso(self, alpha=0.1):
        """https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html"""
        self.alg = linear_model.Lasso(alpha=0.1)

    def set_regressor_ridge(self):
        """https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"""
        self.alg = linear_model.LinearRegression()

    def set_regressor_SVR(self):
        """https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html"""
        self.alg = svm.SVR(gamma="auto")

    # ____________ML_algorithm_Setter____________

    def save(self):
        """Save the trained algorithm in a file, next time the server will be launched the algorithm
        will be restored from the save"""
        dump(self.alg, 'knn_alg.joblib')

    def train(self, data):
        """Data is a list of datacells with each one containing the expected response by the algoirthm as it's last item.
        example : ('a','f','d','j',1) here 1 is the number the algorithm is supposed to find."""
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

        self.alg.fit(X, y)
        self.trained = True
        print("Finder correctly trained")

    def train_multidata(self, X, y) -> None:
        """Same as @self.train(data) but the answer from each datacells can be more than one item, exemple :
        X -> ('a','b','c') and y -> (1,2,3)"""
        if len(X) <= 1:
            print("Not enough data to train")
            return

        X = np.asarray(X)
        y = np.asarray(y)

        self.alg.fit(X, y)
        self.trained = True
        print("Finder correctly trained")

    def predict(self, data):
        """Data is a datacells which don't contain the expect response,
        here the trained algorithm will try to predict it."""
        if self.trained is False:
            print("Can't give localisation without training")
            return
        data = np.asarray(data)
        self.prediction = self.alg.predict(data.reshape(1, -1))
