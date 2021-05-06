# -*- coding: utf-8 -*-
# @Time    : 30/07/2020 23:53
# @Author  : Yanling Hao
# @FileName: CMdraw.py
# @Software: PyCharm
import os
import numpy as np
import pandas as pd
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def CMdraw(X_Train,X_Test,objflag):

    sc_X = StandardScaler()
    X_Train = sc_X.fit_transform(X_Train)
    X_Test = sc_X.transform(X_Test)

    # Fitting the classifier into the Training set
    classifier = SVC(kernel='linear', random_state=0)
    classifier.fit(X_Train, Y_Train)

    # Predicting the test set results
    Y_Pred = classifier.predict(X_Test)


    # Making the Confusion Matrix
    cm = confusion_matrix(Y_Test, Y_Pred)
    labels_name = ["falling", "throwing", "pushing", "kicking", "punching", "jumping", "phonetalk", "seating",
                   "drinking"]
    plot_confusion_matrix(cm, labels_name, "Confusion Matrix")
    # plt.savefig('Result//fig//SVM_1_1.eps',dpi=600,format='eps')
    # plt.savefig('Result//fig//SVM_1_1.eps',dpi=600,format='png')

    fig = plt.gcf()
    savepath = os.path.join ('Result','fig')
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    fig.savefig(savepath+'//'+objflag+'_'+str(action_seg)+'.tif', bbox_inches='tight',dpi=600,format='tiff')
    plt.show()

    # Print classification report
    print(classification_report(Y_Test, Y_Pred, target_names=labels_name))
    return Y_Test, Y_Pred

def plot_confusion_matrix(cm, labels_name, title):
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]  # normalization
    plt.imshow(cm, interpolation='nearest')  # Display an image on a specific window
    plt.title(title)
    plt.colorbar()
    num_local = np.array(range(len(labels_name)))
    plt.xticks(num_local, labels_name, rotation=30)
    plt.yticks(num_local, labels_name)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()