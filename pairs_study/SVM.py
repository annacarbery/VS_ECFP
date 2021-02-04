from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler 
from sklearn import svm
import json
import numpy as np
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

X = json.load(open('pairs_study/x_train.json', 'r'))
y = json.load(open('pairs_study/y_train.json', 'r'))

X_test = json.load(open('pairs_study/x_test.json', 'r'))
y_test = json.load(open('pairs_study/y_test.json', 'r'))

print(len(X), len(X_test))
print(y.count(1), y_test.count(1))

scaler = StandardScaler()  
scaler.fit(X)  
X = scaler.transform(X)  
X_test = scaler.transform(X_test)  

random_state = np.random.RandomState(0)
clf = svm.LinearSVC(random_state=random_state)
clf.fit(X, y)
y_score = clf.decision_function(X_test)

plot_confusion_matrix(clf, X_test, y_test)  
plt.savefig('confusion.png')

from sklearn.metrics import average_precision_score
average_precision = average_precision_score(y_test, y_score)

print('Average precision-recall score: {0:0.2f}'.format(
      average_precision))

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
import matplotlib.pyplot as plt

disp = plot_precision_recall_curve(clf, X_test, y_test)
disp.ax_.set_title('2-class Precision-Recall curve: '
                   'AP={0:0.2f}'.format(average_precision))
plt.savefig('PR_curve')