import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import ReadCSI
import matlab.engine  # To use matlab *.m

eng = matlab.engine.start_matlab()

# Datasets preprocessing
month = 3
day = 24
scene = [1, 2, 3]
person = [1, 3]
action = [1, 2, 3, 4, 5, 6, 9, 10, 11]
# scene = [1]
# person = [1,3]
# action = [1]

action_seg = 2  # second(s) for an action
split_flag = 2  # 1 for 'proportion', 2 for person1 train& person3 test, 2.5 opposite, 3 for scene 1&2 train, scene3 test
objflag = 'SVM'  # 'SVM' 'csinet' 'LSTM'
# ------------Method 1 :
[train_data, train_label, test_data, test_label] = ReadCSI.csi4svm(month, day, scene, person, action, action_seg,
                                                                   split_flag, objflag)
X_Train = train_data
Y_Train0 = train_label
Y_Train = Y_Train0.squeeze()

X_Test = test_data
Y_Test0 = test_label
Y_Test = Y_Test0.squeeze()

# ------------Method 2 : Drectly Importing the datasets
# data = sio.loadmat('Result//actionseg_3s//svmtrain_single_1//train_data.mat')
# X_Train = data['train_data']
# data = sio.loadmat('Result//actionseg_3s//svmtrain_single_1//train_label.mat')
# Y_Train0 = data['train_label']
# Y_Train = Y_Train0.squeeze()
#
# data = sio.loadmat('Result//actionseg_3s//svmtrain_single_1//test_data.mat')
# X_Test = data['test_data']
# data = sio.loadmat('Result//actionseg_3s//svmtrain_single_1//test_label.mat')
# Y_Test0 = data['test_label']
# Y_Test = Y_Test0.squeeze()


# reshape data: from [num， 30， 3，3，200] to [num, 30*3*3*200]

seg = action_seg * 100  # every second has 100 csi serials
X_Train = np.array(X_Train).reshape([len(Y_Train), 30 * 3 * 3 * seg])
X_Test = np.array(X_Test).reshape([len(Y_Test), 30 * 3 * 3 * seg])

mask = np.all(np.isnan(X_Train) | np.equal(X_Train, 0), axis=1)
X_Train = X_Train[~mask]
X_Train[np.isinf(X_Train)] = 0
Y_Train = Y_Train[~mask]
mask = np.all(np.isnan(X_Test) | np.equal(X_Test, 0) | np.isinf(X_Test), axis=1)
X_Test = X_Test[~mask]
X_Test[np.isinf(X_Test)] = 0
Y_Test = Y_Test[~mask]

# Feature Scaling

from sklearn.preprocessing import StandardScaler

sc_X = StandardScaler()
X_Train = sc_X.fit_transform(X_Train)
X_Test = sc_X.transform(X_Test)

# Fitting the classifier into the Training set

from sklearn.svm import SVC

classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_Train, Y_Train)

# Predicting the test set results

Y_Pred = classifier.predict(X_Test)


# Making the Confusion Matrix

def plot_confusion_matrix(cm, labels_name, title):
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]  # normalization
    plt.imshow(cm, interpolation='nearest')  # Display an image on a specific window
    plt.title(title)
    plt.colorbar()
    num_local = np.array(range(len(labels_name)))
    plt.xticks(num_local, labels_name, rotation=90)
    plt.yticks(num_local, labels_name)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


from sklearn.metrics import confusion_matrix

cm = confusion_matrix(Y_Test, Y_Pred)

labels_name = ["falling_down", "throwing", "pushing", "kicking", "punching", "jumping", "phone_talking", "seating",
               "drinking"]
plot_confusion_matrix(cm, labels_name, "Confusion Matrix")
plt.show()

# Print classification report

from sklearn.metrics import classification_report

print(classification_report(Y_Test, Y_Pred, target_names=labels_name))
