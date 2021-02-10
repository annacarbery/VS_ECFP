from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import json
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve


X_train = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/X_train.json', 'r'))
y_train = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/Y_train.json', 'r'))
# X_test = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/X_control.json', 'r'))
# y_test = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/Y_control.json', 'r'))
# X_control = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/X_control.json', 'r'))
# y_control = json.load(open('/dls/science/users/tyt15771/DPhil/VS_ECFP/Y_control.json', 'r'))

# print('data loaded', len(X_train), len(y_train), len(X_test), len(y_test))

X = []
y = []

for pair in X_train:
    X += X_train[pair]
    y += y_train[pair]
print(len(X))
scaler = StandardScaler()  
# Don't cheat - fit only on training data
scaler.fit(X)  
data_train = scaler.transform(X)  
# apply same transformation to test data
# data_test = scaler.transform(X_test)

print('scaled')

clf = svm.SVC()

clf.fit(X, y)
print('trained')
# res = clf.predict(X_test)
# print('predicted')
# correct = 0
# incorrect = 0
# maybe = []
# for i in range(len(res)):
#     if res[i] == y_test[i]:
#         correct += 1
#     elif y_test[i] != 0.5:
#         incorrect += 1
#     else:
#         maybe.append(res[i])

# print(correct, incorrect)
# print(maybe.count(0), maybe.count(1))

# json.dump([int(i) for i in res], open('SVM_res.json', 'w'))

# art_y_test = []
# for i in y_test:
#     if i != 0.5:
#         art_y_test.append(i)
#     else:
#         art_y_test.append(0)


# y_score = clf.decision_function(X_test)       
# from sklearn.metrics import average_precision_score
# average_precision = average_precision_score(art_y_test, y_score)

# print('Average precision-recall score: {0:0.2f}'.format(
#       average_precision))


# disp = plot_precision_recall_curve(clf, X_test, art_y_test)
# disp.ax_.set_title('2-class Precision-Recall curve: '
#                    'AP={0:0.2f}'.format(average_precision))
# plt.savefig('SVM_PR.png')
# print(f"Classification report for classifier {clf}:\n"
#       f"{metrics.classification_report(y_test, res)}\n")

    
# disp = metrics.plot_confusion_matrix(clf, X_test, y_test)
# disp.figure_.suptitle("Confusion Matrix")
# print(f"Confusion matrix:\n{disp.confusion_matrix}")

# plt.savefig('SVM_conf_matrix.png')