from sklearn import tree
import os
import random
import numpy as np
import json

DATA_DIR = '/Users/tyt15771/Documents/VS_ECFP/data/input/'

data_train = []
class_train = []

data_test = []
class_test = []

hits = os.listdir(f'{DATA_DIR}/hit')
random.shuffle(hits)

miss = os.listdir(f'{DATA_DIR}/miss')
random.shuffle(miss)

hits_train, hits_test = hits[:int(len(hits)*0.9)], hits[int(len(hits)*0.9):]
miss_train, miss_test = miss[:len(hits_train)], miss[len(hits_train):len(hits_train)+len(hits_test)]

print(len(hits_train), len(miss_train))
print(len(hits_test), len(miss_test))

for pair in hits_train:
    array = np.load(f'{DATA_DIR}/hit/{pair}/array.npy')
    data_train.append([int(array[0][i]+array[1][i]) for i in range(len(array[0]))])
    # data_train.append([list(array[0]), list(array[1])])
    class_train.append(1)

print(len(data_train))

for pair in miss_train:
    array = np.load(f'{DATA_DIR}/miss/{pair}/array.npy')
    data_train.append([int(array[0][i]+array[1][i]) for i in range(len(array[0]))])
    # data_train.append([list(array[0]), list(array[1])])
    class_train.append(0)

print(len(data_train))

for pair in hits_test:
    array = np.load(f'{DATA_DIR}/hit/{pair}/array.npy')
    data_test.append([int(array[0][i]+array[1][i]) for i in range(len(array[0]))])
    class_test.append(1)

print(len(data_test))

for pair in miss_test:
    array = np.load(f'{DATA_DIR}/miss/{pair}/array.npy')
    data_test.append([int(array[0][i]+array[1][i]) for i in range(len(array[0]))])
    class_test.append(0)

print(len(data_test))

json.dump(data_train, open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/data_train.json', 'w'))
json.dump(class_train, open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/class_train.json', 'w'))
json.dump(data_test, open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/data_test.json', 'w'))
json.dump(class_test, open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/class_test.json', 'w'))
