# -*- coding: utf-8 -*-
# @Time    : 24/07/2020 10:43
# @Author  : Yanling Hao
# @FileName: ReadCSi4svm.py
# @Software: PyCharm

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import Split
import presmooth
import Csi4actseg    train_data = []


import matlab.engine

eng = matlab.engine.start_matlab()


def csi4svm(month, day, scene, person, action, action_seg, split_flag, objflag):
    train_label = []
    test_data = []
    test_label = []

    for s in scene:
        for p in person:
            for act in action:
                # # -------------Method 1 Matlab process the Raw CSI.dat file
                # # csi preprocseeing
                # [csi_amp, csi_pha] = eng.PDemo4csi(month, day, s, p, act, nargout = 2)
                # if csi_amp == 0:
                #     continue
                # else:
                #     # Make the training data for SVM_python
                #     # [train, label] = eng.Pcsi4actseg(csi_amp, s, p, act, action_seg, nargout = 2)
                #     csi_amp = np.array(csi_amp)
                #     [train, label] = Csi4actseg.csi4actseg(csi_amp, s, p, act, action_seg)
                #     # split train data
                #     [train_d, train_l, test_d, test_l] = Split.split(train, label, s, p, split_flag, objflag)
                #     train_data += [train_d]
                #     train_label += [train_l]
                #     test_data += [test_d]
                #     test_label += [test_l]
                #
                #     print("epoch:" + str(s) + "_" + str(p) + "_" + str(act))

                # -------------------method 2: load the csi_amps directly
                if s == 1:
                    ss = 'scene1_without_occlusion'
                elif s == 2:
                    ss = 'scene2_partial_occlusion'
                elif s == 3:
                    ss = 'scene3_full_occlusion'

                if p == 1:
                    pp = 'person1_female'
                elif p == 3:
                    pp = 'person3_male'

                path = os.path.join('examples//wifiposedata', ss, pp)
                files = os.listdir(path)
                name = ''.join((str(s), '_', str(p), '_', str(act), '_amp.mat'))
                dname = os.path.join(path, files[act - 1], 'csi_res', name)
                if not os.path.exists(dname):
                    continue
                else:
                    data = sio.loadmat(dname)
                    csi_amps = data['csi_amps']
                    # remove the outliers
                    # matlab not works
                    # csi_a = matlab.double([csi_amps.tolist()])
                    # [csi_ampsr, csi_ampss] = eng.Presmooth(csi_a, nargout=2)
                    # python
                    [csi_ampmedian,csi_ampmean,csi_ampbutter] = presmooth.Presmooth(csi_amps)

                    # Make the training data for SVM_python
                    # csi_ampss = csi_ampss.tolist()
                    [train, label] = Csi4actseg.csi4actseg(csi_ampbutter, s, p, act, action_seg)
                    # [train, label] = Csi4actseg.csi4actseg(csi_amps, s, p, act, action_seg)

                    # Split data
                    [train_d, train_l, test_d, test_l] = Split.split(train, label, s, p, split_flag, objflag)
                    train_data += [train_d]
                    train_label += [train_l]
                    test_data += [test_d]
                    test_label += [test_l]

                    print("epoch:" + str(s) + "_" + str(p) + "_" + str(act))

    # concatenate all the data together in the format of [num*30*3*3*200]
    train_data = [x for x in train_data if x != []]
    train_data = np.array(train_data)
    train_data = np.concatenate(train_data[:], axis=0)

    train_label = [x for x in train_label if x != []]
    train_label = np.array(train_label)
    train_label = np.concatenate(train_label[:], axis=0)
    train_label.shape = (1, len(train_label))
    train_label = np.transpose(train_label)

    test_data = [x for x in test_data if x != []]
    test_data = np.array(test_data)
    test_data = np.concatenate(test_data[:], axis=0)

    test_label = [x for x in test_label if x != []]
    test_label = np.array(test_label)
    test_label = np.concatenate(test_label[:], axis=0)
    test_label.shape = (1, len(test_label))
    test_label = np.transpose(test_label)

    # save the datasets
    dirs = 'Result//actionseg_' + str(action_seg) + 's' + '//svmtrain_single_' + str(split_flag)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    sio.savemat(dirs + '//train_data.mat', {'train_data': train_data})
    sio.savemat(dirs + '//train_label.mat', {'train_label': train_label})
    sio.savemat(dirs + '//test_data.mat', {'test_data': test_data})
    sio.savemat(dirs + '//test_label.mat', {'test_label': test_label})

    return train_data, train_label, test_data, test_label



