# Transfer the CSI amplitude to the required format
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import Split

import matlab.engine # To use matlab *.m

eng = matlab.engine.start_matlab()

def csi4svm (month,day,scene,person,action,action_seg,split_flag,objflag):
    train_data = []
    train_label = []
    test_data = []
    test_label = []

    for s in scene:
        for p in person:
            for act in action:
                # csi preprocseeing
                [csi_amp, csi_pha] = eng.PDemo4csi(month,day,s,p,act,nargout = 2)
                if csi_amp == 0 :
                    continue
                else:
                    # Make the training data for SVM_python
                    [train, label] = eng.Pcsi4actseg(csi_amp, s, p, act, action_seg, nargout = 2)
                    # split train data
                    [train_d, train_l, test_d, test_l] = Split.split(train, label, s, p, split_flag, objflag)
                    train_data += [train_d]
                    train_label += [train_l]
                    test_data += [test_d]
                    test_label += [test_l]

                    print ("epoch:" + str(s) + "_" + str(p) + "_" + str(act))

    # concatenate all the data together in the format of [num*30*3*3*200]
    train_data = np.array(train_data)
    train_data = list(filter(None, train_data))
    train_data = np.concatenate (train_data [:], axis=0)

    train_label = np.array(train_label)
    train_label = list(filter(None, train_label))
    train_label = np.concatenate (train_label [:], axis=0)

    test_data = np.array(test_data)
    test_data = list(filter(None, test_data))
    test_data = np.concatenate (test_data [:], axis=0)

    test_label = np.array(test_label)
    test_label = list(filter(None, test_label))
    test_label = np.concatenate (test_label [:], axis=0)

    # save the datasets
    dirs = 'Result//actionseg_'+ str(action_seg)+'s'+'//svmtrain_single_'+str(split_flag)
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





def csi4net (month,day,scene,person,action,action_seg,split_flag,objflag):
    # Make the traing data for CSI-net
    train_data = []
    train_label = []
    test_data = []
    test_label = []

    for s in scene:
        for p in person:
            for act in action:

                # # load the csi_amps directly
                # if s == 1:
                #     scene = 'scene1_without_occlusion'
                # elif s == 2:
                #     scene = 'scene2_partial_occlusion'
                # elif s == 3:
                #     scene = 'scene3_full_occlusion'
                #
                # if p == 1:
                #     person = 'person1_female'
                # elif p == 3:
                #     person = 'person3_male'
                #
                # path = os.path.join ('examples\wifiposedata', scene, person)
                # files = os.listdir(path)
                # name = ''.join((str(s), '_', str(p), '_', str(act), '_amp.mat'))
                # dirname = os.path.join(path, files[act - 1], 'csi_res', name)
                # data = sio.loadmat(dirname)
                # csi_amps = data ['csi_amps']
                # csi_amps = matlab.double (csi_amps[:].tolist())
                # # Make the training data for csinet
                # [train, label] = eng.Pcsi4net(csi_amps, act, nargout=2)
                # # Split data for csinet
                # [train_d, train_l, test_d, test_l] = eng.Psplit(train, label, s, p, split_flag, objflag, nargout=4)
                # train_data.append(train_d,axis = 0)
                # train_label.append(train_l,axis = 0)
                # test_data.append(test_d,axis = 0)
                # test_label.append(test_l,axis = 0)
                # # train_data += [train_d]
                # # train_label += [train_l]
                # # test_data += [test_d]
                # # test_label += [test_l]
                #
                # print ("epoch:" + str(s) + "_" + str(p) + "_" + str(act))

                [csi_amp, csi_pha] = eng.PDemo4csi(month, day, s, p, act, nargout=2)
                if csi_amp == 0:
                    continue
                else:
                    # Make the training data for csinet
                    nind = act
                    sn = len(csi_amp)
                    train_d = csi_amp[:, :, 1, 1] # choose t1 R1 antenna
                    #  writing the corresponding the label. Due to we lack action 7, 8, so we move 10, 11 ahead
                    if nind == 10:
                        label_d = 7
                    elif nind == 11:
                        label_d = 8
                    else:
                        label_d = int(nind)
                    label_t = ones(sn, 1) * label_d
                    train = train_d
                    label = label_t

                    # Split data for csinet
                    [train_d, train_l, test_d, test_l] = Split.split(train, label, s, p, split_flag, objflag)
                    train_data += [train_d]
                    train_label += [train_l]
                    test_data += [test_d]
                    test_label += [test_l]

                    print("epoch:" + str(s) + "_" + str(p) + "_" + str(act))

                # concatenate all the data together in the format of [num*30*3*3*200]
                train_data = np.array(train_data)
                train_data = list(filter(None, train_data))
                train_data = np.concatenate(train_data[:], axis=0)

                train_label = np.array(train_label)
                train_label = list(filter(None, train_label))
                train_label = np.concatenate(train_label[:], axis=0)

                test_data = np.array(test_data)
                test_data = list(filter(None, test_data))
                test_data = np.concatenate(test_data[:], axis=0)

                test_label = np.array(test_label)
                test_label = list(filter(None, test_label))
                test_label = np.concatenate(test_label[:], axis=0)

    # save the datasets
    dirs = 'Result//actionseg_' + str(action_seg) + 's' + '//csinet_single_' + str(split_flag)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    sio.savemat(dirs + '//train_data.mat', {'train_data': train_data})
    sio.savemat(dirs + '//train_label.mat', {'train_label': train_label})
    sio.savemat(dirs + '//test_data.mat', {'test_data': test_data})
    sio.savemat(dirs + '//test_label.mat', {'test_label': test_label})

    return train_data, train_label, test_data, test_label

    # # Make the traing data for RSTM
    # eng.PreTrainTest_e(flag)

