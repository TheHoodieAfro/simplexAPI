import simplexCalsificator as sc
import pandas as pd
import numpy as np
import copy
import sklearn as sk
import os

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def prepareData(data):

    data = pd.read_csv("data/"+ data)

    data_array = data.to_numpy()

    i=0
    for column in data:
      column_type = type(data_array[1][i]).__name__
      if column_type == 'str':
        data[column] = data[column].astype('category')
      elif column_type == 'int':
        data[column] = data[column].astype('uint8')
      i+=1

    X = data[data.columns[:len(data.axes[1])-1]]
    y = data[data.columns[len(data.axes[1])-1]]

    return train_test_split(X, y, test_size=0.4, random_state=0)

def getResults(model, X_test, y_test, good, help, id):

    modelList = []

    for count in range(len(X_test)):
        t = copy.deepcopy(X_test.iloc[[count]])

        if good:
            modelPrediction = model.predict(help.one_hot_encode(t))
            modelList.append(modelPrediction)
        else:
            modelPrediction = model.predict(t)
            modelList.append(modelPrediction)

    total_predict = np.array(modelList)

    y_result = y_test.to_numpy()
    y_result_values = list(set(y_result))
    y_result

    tp= 0
    tn = 0
    fp = 0
    fn = 0
    for n in range(len(y_result)):
        if(y_result[n] == total_predict[n]):
          if y_result[n] == y_result_values[0]:
            tp = tp +1
          else:
            tn = tn + 1
        if(y_result[n] != total_predict[n]):
          if y_result[n] == y_result_values[1]:
            fp = fp + 1
          else:
            fn = fn + 1
       
    try:
        precision = tp/(tp+fp)
    except Exception as e:
        precision = 'ERROR'

    try:
        accuracy = (tp+tn)/(tp+tn+fp+fn)
    except Exception as e:
        accuracy = 'ERROR'

    try:
        f1 = (2*tp)/((2*tp)+fp+fn)
    except Exception as e:
        f1 = 'ERROR'

    try:
        kappa = sk.metrics.cohen_kappa_score(y_result,total_predict)
    except Exception as e:
        kappa = 'ERROR'

    if precision != 'ERROR' and accuracy != 'ERROR' and f1 != 'ERROR' and kappa != 'ERROR':
        totalPoints = precision + accuracy + f1 + kappa
    else:
        totalPoints = 0
    
    return {"id": id,"confusion_matrix": {"tp": tp, "fp": fp, "fn": fn, "tn": tn}, "precision": precision, "accuracy": accuracy, "f1": f1, "kappa": kappa, "total_points": totalPoints}
   
def executeSimplex(data):

    print('[+] Processing data')
    X_train, X_test, y_train, y_test = prepareData(data)

    print('[+] Creating and trainning model')
    simplexDegree = sc.simplexClassificator('concentricity')
    simplexDegree.fit(X_train, y_train)

    print('[+] Validating model')
    filename, shit = os.path.splitext(data)
    return getResults(simplexDegree, X_test, y_test, False, simplexDegree, "simplexDegree-"+ filename)

def executeKNN(data):

    print('[+] Processing data')
    X_train, X_test, y_train, y_test = prepareData(data)

    print('[+] Creating and trainning model')
    simplexDegree = sc.simplexClassificator('concentricity')
    knnHamming = KNeighborsClassifier(n_neighbors=5)
    knnHamming.fit(simplexDegree.one_hot_encode(X_train), y_train)

    print('[+] Validating model')
    filename, shit = os.path.splitext(data)
    return getResults(knnHamming, X_test, y_test, True, simplexDegree, "KNN-"+ filename)

def executeTree(data):

    print('[+] Processing data')
    X_train, X_test, y_train, y_test = prepareData(data)

    print('[+] Creating and trainning model')
    simplexDegree = sc.simplexClassificator('concentricity')
    tree = DecisionTreeClassifier(random_state=0)
    tree.fit(simplexDegree.one_hot_encode(X_train), y_train)

    print('[+] Validating model')
    filename, shit = os.path.splitext(data)
    return getResults(simplexDegree, X_test, y_test, True, simplexDegree, "DecisionTree-"+ filename)