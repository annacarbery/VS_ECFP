from sklearn.tree import DecisionTreeClassifier
import json
import numpy as np
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

def make_input(list1, list2):
    X = []
    y = []

    for l in [list1, list2]:
        for ECFPs in l:
            vec = [0]*2048
            for v in range(len(vec)):
                for ECFP in ECFPs:
                    if ECFP[v] > 0:
                        vec[v] += 1
            X.append(vec)
            if l == list1:
                y.append(1)
            else:
                y.append(0)
    return X, y


def make_long_input(list1, list2):

    X = []
    y = []

    for l in [list1, list2]:
        for ECFPs in l:
            full = []
            for ECFP in ECFPs[:3]:
                full += ECFP
            X.append(full)
            if l == list1:
                y.append(1)
            else:
                y.append(0)
    return X, y

X = json.load(open('pairs_study/x_train.json', 'r'))
y = json.load(open('pairs_study/y_train.json', 'r'))

X_test = json.load(open('pairs_study/x_test.json', 'r'))
y_test = json.load(open('pairs_study/y_test.json', 'r'))

print(len(X), len(X_test))
print(y.count(1), y_test.count(1))

# scaler = StandardScaler()  
# scaler.fit(X)  
# X = scaler.transform(X)  
# X_test = scaler.transform(X_test)  

clf = DecisionTreeClassifier(random_state=0)

clf.fit(X, y)
res = clf.predict(X_test)
plot_confusion_matrix(clf, X_test, y_test)  
plt.savefig('confusion.png')


