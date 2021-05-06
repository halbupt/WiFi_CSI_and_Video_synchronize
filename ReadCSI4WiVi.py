# -*- coding: utf-8 -*-
# @Time    : 07/08/2020 18:12
# @Author  : Yanling Hao
# @FileName: ReadCSI4WiSPPN.py
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

def csi4WiVi(month, day, scene, person, action, action_seg, split_flag, objflag):
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