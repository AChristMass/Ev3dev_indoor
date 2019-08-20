import ssl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# Assign colum names to the dataset
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']

# Read dataset to pandas dataframe
dataset = pd.read_csv(url, names=names)

print(dataset.head())

#Train Test Split
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 4].values

print(X)
print("second : ")
print(y)
print("end")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)


#Feature Scaling
"""Since the range of values of raw data varies widely, 
in some machine learning algorithms, objective functions 
will not work properly without normalization. For example, 
the majority of classifiers calculate the distance between 
two points by the Euclidean distance. If one of the features 
has a broad range of values, the distance will be governed by this particular 
feature. Therefore, the range of all features should be normalized so that each 
feature contributes approximately proportionately to the final distance."""
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#Training and Predictions
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))











