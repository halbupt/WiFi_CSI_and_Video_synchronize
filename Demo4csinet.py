import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import ReadCSI
import matlab.engine # To use matlab *.m

eng = matlab.engine.start_matlab()

# Datasets preprocessing
month = 3
day = 24
scene = [1,2,3]
person = [1,3]
action = [1,2,3,4,5,6,9,10,11]

action_seg = 2 # second(s) for an action
split_flag = 1 # 1 for 'proportion', 2 for person1 train& person3 test, 2.5 opposite, 3 for scene 1&2 train, scene3 test
objflag = 'csinet'

# ------------Method 1 :
[train_data,train_label,test_data,test_label] = ReadCSI.csi4net (month,day,scene,person,action,action_seg,split_flag,objflag)
X_Train = train_data
Y_Train0 = train_label
Y_Train = Y_Train0.squeeze()

X_Test = test_data
Y_Test0 = test_label
Y_Test = Y_Test0.squeeze()

# ------------Method 2 : Drectly Importing the datasets
# data = sio.loadmat('Result//actionseg_3s//csinet_single_1//train_data.mat')
# X_Train = data['train_data']
# data = sio.loadmat('Result//actionseg_3s//csinet_single_1//train_label.mat')
# Y_Train0 = data['train_label']
# Y_Train = Y_Train0.squeeze()
#
# data = sio.loadmat('Result//actionseg_3s//csinet_single_1//test_data.mat')
# X_Test = data['test_data']
# data = sio.loadmat('Result//actionseg_3s//csinet_single_1//test_label.mat')
# Y_Test0 = data['test_label']
# Y_Test = Y_Test0.squeeze()

