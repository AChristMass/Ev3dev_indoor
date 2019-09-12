from sklearn import linear_model
import os.path

import pandas as pd
from sklearn import svm


def main():
    phoneid = 526
    relpos = 525
    space = 524
    bid = 523
    fid = 522
    lat = 521
    lon = 520

    training_file = '../../dataset/TrainingData_b1f1.csv'
    validation_file = '../../dataset/ValidationData.csv'

    # From server path = "../../bdd/fingerPrint.db"
    # From main path = "../bdd/fingerPrint.db"

    if not os.path.isfile(training_file):
        print("Your training file doesn't exist")
        return

    # Assign colum names to the dataset
    training_file = open(training_file, "r")
    # validation_file = open(validation_file, "r")
    # names2 = validation_file.readline().split(",")
    # names2[-1] = names2[-1].split("\n")[0]

    names = training_file.readline().split(",")
    names[-1] = names[-1].split("\n")[0]
    # print(names)

    # Read dataset to pandas dataframe
    dataset = pd.read_csv(training_file, names=names)

    #dataset2 = pd.read_csv(validation_file, names=names2)
    # print(dataset.head())

    # Train Test Split
    X = dataset.iloc[:, :-9].values[:-100]
    y = dataset.iloc[:, 524].values[:-100]

    print("Trained on",len(X), "fingerprints")


    X2 = dataset.iloc[:,: -9].values[1384:]
    y2 = dataset.iloc[:, 524].values[1384:]

    print( "Tested on",len(X2), "fingerprints")

    reg = linear_model.LinearRegression()
    reg.fit(X, y)

    a = 0
    for i in range(len(X2)):
        prediction = int(reg.predict(X2[i].reshape(1, -1)))
        if prediction == y2[i]:
            a += 1

    print("Guessed : ", a)
    print("Accuracy = ", a / len(X2) * 100)

    # print(value_to_predict.shape)

    # print(prediction)


if __name__ == '__main__':
    main()
