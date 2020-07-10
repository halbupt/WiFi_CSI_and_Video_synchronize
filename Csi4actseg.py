# -*- coding: utf-8 -*-
# @Time    : 09/07/2020 23:03
# @Author  : Yanling Hao
# @FileName: Csi4actseg.py
# @Software: PyCharm

import os
import numpy as np
import scipy.io as sio
import torch


def csi4actseg(csi_amp, scene, person, action, action_seg, train_d=None):
    # function segment csi amplitude into action by time, all save in 'Result/actionseg_*/'
    # train_data[num * 30 * 3 * 3 * 200]  label_data: [num * 1]
    name_action = str(scene) + '_' + str(person) + '_'
    name_dir = 'Result//actionseg_' + str(action_seg) + 's'
    s_dir1 = os.path.join(name_dir, 'train_data')
    s_dir2 = os.path.join(name_dir, 'train_label')

    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    if not os.path.exists(s_dir1):
        os.makedirs(s_dir1)

    if not os.path.exists(s_dir2):
        os.makedirs(s_dir2)

    seg = action_seg * 100  # the number of csi packages for an action
    nind = action
    sum_len = len(csi_amp)
    sn = sum_len // seg  # get the max number
    train_d = np.zeros([sn, 30, 3, 3, seg])
    for s in range(sn):
        csi_mat = csi_amp
        train_g = csi_mat[seg * s:(s * seg + seg), :, :, :]  # an action csi serial
        train_s = np.transpose(train_g, (1, 2, 3, 0))
        train_d[s, :, :, :, :] = train_s

    sio.savemat(s_dir1 + '//train_data_' + name_action + str(nind) + '_' + str(sn) + '.mat', {'train_d': train_d})

    #  writing the corresponding the label. Due to we lack action 7, 8, so we move 10, 11 ahead
    if nind == 10:
        label = 7
    elif nind == 11:
        label = 8
    else:
        label = int(nind)

    label_t = np.ones((sn,)) * label
    sio.savemat(s_dir2 + '//train_label_' + name_action + str(nind) + '_' + str(sn) + '.mat', {'label_t': label_t})

    train_data = train_d
    label_data = label_t

    return train_data, label_data
