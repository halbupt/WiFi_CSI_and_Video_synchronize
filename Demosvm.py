import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import ReadCSI
import matlab.engine # To use matlab *.m

eng = matlab.engine.start_matlab()


# Datasets preprocessing
# Method 1 :
month = 3
day = 24
scene = [1,2,3]
person = [1,3]
action = [1,2,3,4,5,6,9,10,11]

action_seg = 2 # 1 second(s) for an action
split_flag = 1 # 1 for 'proportion', 2 for person1 train& person3 test, 2.5 opposite, 3 for scene 1&2 train, scene3 test
#
# [train_data,train_label,test_data,test_label] = ReadCSI.csi4svm (month,day,scene,person,action,action_seg,split_flag)
# X_Train = data['train_data']
# Y_Train0 = data['train_label']
# Y_Train = Y_Train0.squeeze()
#
# X_Test = data['test_data']
# Y_Test0 = data['test_label']
# Y_Test = Y_Test0.squeeze()

# Method 2 : Drectly Importing the datasets
data = sio.loadmat('Result//2s//train_data.mat')
X_Train = data['train_data']
data = sio.loadmat('Result//2s//train_label.mat')
Y_Train0 = data['train_label']
Y_Train = Y_Train0.squeeze()

data = sio.loadmat('Result//2s//test_data.mat')
X_Test = data['test_data']
data = sio.loadmat('Result//2s//test_label.mat')
Y_Test0 = data['test_label']
Y_Test = Y_Test0.squeeze()

# reshape data

#reshape
[X_Train,X_Test]= eng.Preshape(X_Train,X_Test,action_seg,nargout = 2)

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

labels_name = ["falling_down", "throwing", "pushing", "kicking", "punching", "jumping", "drinking", "phone_talking",
               "seating"]
plot_confusion_matrix(cm, labels_name, "Confusion Matrix")
plt.show()

# Print classification report

from sklearn.metrics import classification_report

print (classification_report(Y_Test,Y_Pred, target_names = labels_name))