# -*- coding: utf-8 -*-
# @Time    : 24/07/2020 01:02
# @Author  : Yanling Hao
# @FileName: presmooth.py
# @Software: PyCharm
import os
import scipy.io as sio
import scipy
from scipy import signal
from scipy import ndimage
from scipy.ndimage import filters
from scipy.signal import sosfiltfilt, butter,medfilt
import matplotlib.pyplot as plt
import numpy as np

def Presmooth(csi_amps):

    (num, subcarrier, height, width) = csi_amps.shape
    # scipy.signal.butter(N, Wn, btype='low', analog=False, output='ba', fs=None)
    # 这里假设采样频率为100hz,信号本身最大的频率为500hz，要滤除5hz以上频率成分，即截至频率为5hz，则wn=2*5/100=0.1
    sos = butter(5, 0.1, output='sos')
    csi_ampmedian = np.zeros([num, subcarrier, height, width])
    csi_ampmean = np.zeros([num, subcarrier, height, width])
    csi_ampbutter = np.zeros([num, subcarrier, height, width])
    x = range(num)
    for ti in range(height):
        for ri in range(width):
            for nd in range(subcarrier):
                # scipy.signal.medfilt(volume, kernel_size=None),
                # a median filter (sliding window size of 20 and stride of 1)
                csi_ampmedian [:, nd, ti, ri] = medfilt(csi_amps[:, nd, ti, ri], kernel_size = 41)
                # scipy.ndimage.filters.uniform_filter1d(input, size, axis=-1, output=None, mode='reflect', cval=0.0, origin=0)
                # a mean filter (sliding window size of 20, stride of 1)
                csi_ampmean [:, nd, ti, ri] = filters.uniform_filter1d (csi_ampmedian[:, nd, ti, ri],41)
                # scipy.signal.butter(N, Wn, btype='low', analog=False, output='ba', fs=None)
                # low-pass Butterworth filter (5th order, passband of 5Hz)
                csi_ampbutter [:, nd, ti, ri] = sosfiltfilt(sos, csi_ampmean [:, nd, ti, ri])

                # # draw the filtered signal
                # fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
                #
                # ax1.plot(x, csi_amps[:, nd, ti, ri])
                # ax1.set_title('Raw CSI for Falling Down')
                # ax1.axis([0, num, 0, 25])
                # ax1.set_xlabel('Packet')
                # ax1.set_ylabel('Amplitude')
                #
                # ax2.plot(x, csi_ampmedian[:, nd, ti, ri])
                # ax2.set_title('CSI after Median Filter')
                # ax2.axis([0, num, 0, 25])
                # ax2.set_xlabel('Packet')
                # ax2.set_ylabel('Amplitude')
                #
                # ax3.plot(x, csi_ampmean[:, nd, ti, ri])
                # ax3.set_title('CSI after Mean Filter')
                # ax3.axis([0, num, 0, 25])
                # ax3.set_xlabel('Packet')
                # ax3.set_ylabel('Amplitude')
                #
                # ax4.plot(x, csi_ampbutter [:, nd, ti, ri])
                # ax4.set_title('CSI after Butterworth Filter')
                # ax4.axis([0, num, 0, 25])
                # ax4.set_xlabel('Packet')
                # ax4.set_ylabel('Amplitude')
                # plt.tight_layout()
                # savepath = os.path.join('Result', 'Prfig')
                # if not os.path.exists(savepath):
                #     os.makedirs(savepath)
                # fig = plt.gcf()
                # fig.savefig(savepath + '//Pre_1_1_1.tif', bbox_inches='tight', dpi=600, format='tiff')
                # plt.show()
                # a = 1

    return csi_ampmedian,csi_ampmean,csi_ampbutter