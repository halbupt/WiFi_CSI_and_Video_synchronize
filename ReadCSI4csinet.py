# -*- coding: utf-8 -*-
# @Time    : 24/07/2020 10:41
# @Author  : Yanling Hao
# @FileName: ReadCSI4csinet.py
# @Software: PyCharm
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import Split
import presmooth
import math
import Csi4actseg

import matlab.engine

eng = matlab.engine.start_matlab()

def csi4net(month, day, scene, person, action, action_seg, split_flag, objflag):
    # Make the traing data for CSI-net
    train_data = []
    train_label = []
    test_data = []
    test_label = []

    for s in scene:
        for p in person:
            for act in action:
                # ---------------------csi process method 1: process the data use the matlab function
                # [csi_amps, csi_pha] = eng.PDemo4csi(month, day, s, p, act, nargout=2)
                # if csi_amps == 0:
                #     continue
                # else:
                #     # Make the training data for csinet
                #     csi_amps = matlab.double(csi_amps[:].tolist())
                #     [train, label] = eng.Pcsi4net(csi_amps, act, nargout=2)
                #     # Split data for csinet
                #     [train_d, train_l, test_d, test_l] = Split.split(train, label, s, p, split_flag, objflag)
                #     train_data += [train_d]
                #     train_label += [train_l]
                #     test_data += [test_d]
                #     test_label += [test_l]
                #     print("epoch:" + str(s) + "_" + str(p) + "_" + str(act))


                #  -------------------csi process method 2: load the csi_amps directly
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

                    # Make the training data for csinet
                    sn = len(csi_amps)
                    [csi_ampmedian, csi_ampmean, csi_ampbutter] = presmooth.Presmooth(csi_amps)


                    # ---------average method 1: directly avearge 10 samples
                    # train0 = csi_ampbutter[:, :, 1, 1]  # choose t1 R1 antenna
                    # #  writing the corresponding the label. Due to we lack action 7, 8, so we move 10, 11 ahead
                    # if act == 10:
                    #     label_d = 7
                    # elif act == 11:
                    #     label_d = 8
                    # else:
                    #     label_d = int(act)
                    # label0 = np.ones((sn,)) * label_d
                    #
                    # average 10 packet as a CSi sample
                    #
                    # (sum_len, subcarrier) = train0.shape  # [num, 30]
                    # sel = 10
                    # n = sum_len // sel  # every 10 continuous CSI samples with stride of 10
                    # train = np.zeros([n, 30])
                    # label = np.zeros(n)
                    # for nums in range(n):
                    #     train[nums, :] = np.mean(train0 [sel * nums:(nums * sel + sel), :], axis=0)
                    #     label[nums] = label0 [sel * nums]


                    # -------------average method 2 :actseg choose randam average 10 samples
                    [train0, label0] = Csi4actseg.csi4actseg(csi_ampbutter, s, p, act, action_seg)
                    sel = 10  # average number
                    [trains, labels] = average (train0, label0, sel)
                    train = trains [:, :, 1, 1]
                    label = labels



                    # data augmentation
                    [train_a, label_a] = dataaug(train, label)

                    # Split data for csinet
                    [train_d, train_l, test_d, test_l] = Split.split(train_a, label_a, s, p, split_flag, objflag)
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
    dirs = 'Result//sactionseg_' + str(action_seg) + 's' + '//sscsinet_single_' + str(split_flag)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    sio.savemat(dirs + '//train_data.mat', {'train_data': train_data})
    sio.savemat(dirs + '//train_label.mat', {'train_label': train_label})
    sio.savemat(dirs + '//test_data.mat', {'test_data': test_data})
    sio.savemat(dirs + '//test_label.mat', {'test_label': test_label})

    return train_data, train_label, test_data, test_label


import random

def dataaug(train, label):
    # shuffle the index
    n = len(label)
    index = [i for i in range(n)]
    random.shuffle(index)
    train = train[index,:]
    label = label[index]
    # augmentation
    # traint = np.zeros([train.shape])
    # labelt = np.zeros([len(label)])

    for k in [2, 3, 5, 7]:
        nums = n//k
        traint = np.zeros([nums, 30])
        labelt = np.zeros(nums)
        for i in range(nums):
            traint[i, :] = np.mean(train[k * i:(i * k + k), :], axis=0)
            labelt[i] = label[k * i]

        train = np.concatenate((train,traint), axis = 0)
        label = np.concatenate((label,labelt), axis = 0)


    train_d = train
    label_d = label

    return train_d, label_d


def average (train, label,sel):
    # train_data[num * 30 * 3 * 3 * 200]
    # label_data: [num * 1]
    (sum_len, subcarrier, height, width, seg) = train.shape  # seg = act_seg*100
    if sel > seg:
        print("# num out of length, return train & label:", end=" ")
        return train, label
    else:
        n = seg // sel
        train_ad = []
        averages = []
        for k in range (n):
            average = []
            for i in range (sum_len):
                output = []
                for j in range (n):
                    if sel*(j+1) + k >= seg:
                        output += [train [i, :, :, :, -1]]
                    else:
                        # print(train[i, :, :, :, sel*j + k].shape)
                        output += [train [i, :, :, :, sel*j + k]] #  [  [30 3 3] ]
                output0 = np.array([output]) # expand one more dimension
                # print (output0.shape)
                output1 = np.concatenate(output0[:], axis = 0)
                # print(output1.shape)
                average0 = np.mean(output1, axis = 0) # one average
                # print(average0.shape)
                average += [average0] # sum_len averages
            averages += average # change k and get k*sum_len averages

        train_ad = np.array(averages)

    #  writing the corresponding the label. Due to we lack action 7, 8, so we move 10, 11 ahead
    sn = len(train_ad)
    label_ad = np.ones((sn,)) * label[0]

    return train_ad, label_ad


