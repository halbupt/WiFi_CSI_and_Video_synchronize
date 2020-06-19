# Transfer the CSI amplitude to the required format
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import matlab.engine # To use matlab *.m

eng = matlab.engine.start_matlab()

def csi4svm (month,day,scene,person,action,action_seg,split_flag):
    # flag =1 # 1 for WISPPN, 2 for SVM, 3 for CSI-net, 4 for RSTM

    # produce the CSI amplitude &  phase
    # month = 3
    # day = 24
    # scene = [1,2,3]
    # person = [1,3]
    # action = [1,2,3,4,5,6,9,10,11]
    #
    # action_seg = 3 # 1 second(s) for an action
    # split_flag = 1 # 1 for 'proportion', 2 for person1 train& person3 test, 2.5 opposite, 3 for scene 1&2 train, scene3 test

    train_data = []
    train_label = []
    test_data = []
    test_label = []

    for s in scene:
        for p in person:
            for act in action:
                [csi_amp, csi_pha] = eng.PDemo4csi(month,day,s,p,act,nargout = 2) #csi preprocseeing
                if csi_amp == 0 :
                    continue
                else:
                    [train, label] = eng.Pcsi4svm(csi_amp, s, p, act, action_seg, nargout = 2) # Make the training data for SVM_python
                    [train_d, train_l, test_d, test_l] = eng.Psplit(train, label, s, p, split_flag, nargout = 4) # train data split
                    train_data += [train_d]
                    train_label += [train_l]
                    test_data += [test_d]
                    test_label += [test_l]

    # concatenate all the data together in the format of [num*30*3*3*200]
    train_data = np.array(train_data)
    train_data = np.concatenate (train_data [:], axis=0)

    train_label = np.array(train_label)
    train_label = np.concatenate (train_label [:], axis=0)

    test_data = np.array(test_data)
    test_data = np.concatenate (test_data [:], axis=0)

    test_label = np.array(test_label)
    test_label = np.concatenate (test_label [:], axis=0)

    # save the datasets
    dirs = 'Result//'+ str(action_seg)+'s_-'+str(split_flag)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    sio.savemat(dirs+'//train_data.mat', {'train_data':train_data})
    sio.savemat(dirs+'//train_label.mat', {'train_label': train_label})
    sio.savemat(dirs+'//test_data.mat',{'test_data': test_data})
    sio.savemat(dirs+'//test_label.mat', {'test_label': test_label})

    return train_data,train_label,test_data,test_label

# produce the frame synchronizing with the CSI
# eng.Demo4frame(flag)


# Make the training data for WiSPPN
#eng.prepare_mydata(flag)




# Make the traing data for CSI-net
# eng.PreTrainTest_d(flag)
#
# # Make the traing data for RSTM
# eng.PreTrainTest_e(flag)