from sklearn import tree
import os
import random
import numpy as np

DATA_DIR = '/Users/tyt15771/Documents/VS_ECFP/data/input/'

X = []
Y = []
hits = os.listdir(f'{DATA_DIR}/hit')
random.shuffle(hits)

miss = os.listdir(f'{DATA_DIR}/miss')
random.shuffle(miss)

hits_train, hits_test = hits[:int(len(hits)*0.9)], hits[int(len(hits)*0.9):]
miss_train, miss_test = miss[:len(hits_train)], miss[len(hits_train):len(hits_train)+len(hits_test)]

print(len(hits_train), len(miss_train))
print(len(hits_test), len(miss_test))

for pair in hits_train:
    print(pair)
    X.append(list(np.load(f'{DATA_DIR}/hit/{pair}/array.npy')))
    Y.append(1)

for pair in miss_train:
    X.append(list(np.load(f'{DATA_DIR}/hit/{pair}/array.npy')))
    Y.append(0)

print(X)
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(X, Y)

# res = clf.predict([[2., 2.], [0., 0.]])
# print(res)