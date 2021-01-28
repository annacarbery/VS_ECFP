from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import json
import matplotlib.pyplot as plt

data_train = json.load(open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/data_train.json', 'r'))
class_train = json.load(open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/class_train.json', 'r'))
data_test = json.load(open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/data_test.json', 'r'))
class_test = json.load(open('/Users/tyt15771/Documents/VS_ECFP/src/scoring/class_test.json', 'r'))

print('data loaded ')
scaler = StandardScaler()  
# Don't cheat - fit only on training data
scaler.fit(data_train)  
data_train = scaler.transform(data_train)  
# apply same transformation to test data
data_test = scaler.transform(data_test)
print('scaled')
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                   hidden_layer_sizes=(5, 2), random_state=1)


clf.fit(data_train, class_train)
print('trained')
res = clf.predict(data_test)
print('predicted')
correct = 0
incorrect = 0
for i in range(len(res)):
    if res[i] == class_test[i]:
        correct += 1
    else:
        incorrect += 1

print(correct, incorrect)

print(f"Classification report for classifier {clf}:\n"
      f"{metrics.classification_report(class_test, res)}\n")

    
disp = metrics.plot_confusion_matrix(clf, data_test, class_test)
disp.figure_.suptitle("Confusion Matrix")
print(f"Confusion matrix:\n{disp.confusion_matrix}")

plt.show()