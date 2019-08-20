import os.path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import preprocessing
from sklearn import utils






def main() :
    relpos = 525
    space = 524
    bid = 523
    fid = 522
    lat = 521
    lon = 520


    training_file = '../../dataset/TrainingData_b1f1test.csv'
    validation_file = '../../dataset/ValidationData.csv'

    #From server path = "../../bdd/fingerPrint.db"
    #From main path = "../bdd/fingerPrint.db"

    if not os.path.isfile(training_file):
        print("Your training file doesn't exist")
        return

    # Assign colum names to the dataset
    training_file = open(training_file, "r")
    names = training_file.readline().split(",")
    names[-1] = names[-1].split("\n")[0]
    #print(names)



    #Read dataset to pandas dataframe
    dataset = pd.read_csv(training_file, names=names)
    #print(dataset.head())

    #Train Test Split
    X = dataset.iloc[:, :-9].values
    y = dataset.iloc[:, 520].values



    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)



    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    lab_enc = preprocessing.LabelEncoder()
    training_scores_encoded = lab_enc.fit_transform(y_train)

    #print(y_train)
    #print(utils.multiclass.type_of_target(y_train))
    #print(utils.multiclass.type_of_target(y_train.astype('int')))
    #print(utils.multiclass.type_of_target(training_scores_encoded))

    #Training and Predictions
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X_train, training_scores_encoded)

    y_pred = classifier.predict(X_test)
    #y_pred = classifier.predict(X[-1].reshape(-1, 1))

    #print(y_pred)
    #print(y_test)

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    #print("prediction : ", y_pred)
    #print("taile de la pred ", len(y_pred))





if __name__ == '__main__':
    main()
