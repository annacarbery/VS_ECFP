from sklearn import tree
from sklearn import metrics
import json
import matplotlib.pyplot as plt
import pandas as pd

X_train = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/X_train.json', 'r'))
y_train = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/Y_train.json', 'r'))
X_test = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/X_test.json', 'r'))
y_test = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/Y_test.json', 'r'))

print('data loaded', len(X_train), len(y_train), len(X_test), len(y_test))


clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
(print('trained'))
res = clf.predict(X_test, y_test)
print('predicted')
correct = 0
incorrect = 0
for i in range(len(y_test)):
    if res[i] == y_test[i]:
        correct += 1
    else:
        incorrect += 1

print(correct, incorrect)

# print(f"Classification report for classifier {clf}:\n"
#       f"{metrics.classification_report(class_test, res)}\n")

    
disp = metrics.plot_confusion_matrix(clf, X_test, y_test)
disp.figure_.suptitle("Confusion Matrix")
print(f"Confusion matrix:\n{disp.confusion_matrix}")

plt.savefig('DT_conf_matrix.png')

# disp = metrics.plot_roc_curve(clf, data_test, class_test)
# # disp.figure_.suptitle("ROC Curve")
# # print(f"Confusion matrix:\n{disp.confusion_matrix}")

# plt.show()


