'''Created March 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all power functions'''


##all required imports 
import pandas as pd
import os
import numpy as np
import mne
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy
from scipy import signal
import re
import itertools


'this function calculates psd via Welch method on data with noise artifacts removed'

def psd_per_channel(data_without_noise):

    welch_channel = []
    for data_array in data_without_noise:
        welch_channel.append(scipy.signal.welch(data_array, fs=250.4, window='hann', nperseg=1252))
    
    power_spectrum_list = [power_array[1] for power_array in welch_channel]

     #save one array of frequency values for plotting 
    frequency = welch_channel[0][0]
        
    return power_spectrum_list, frequency


def psd_average(psd,frequency): 
    
    df_psd = pd.DataFrame(psd)
    mean_values = df_psd.mean(axis = 0)
    mean_psd = mean_values.to_numpy()

    #fig = plt.figure()
    plt.semilogy(frequency, mean_psd)
    plt.xlabel('Frequency [Hz]')
    plt.xlim(1,50)
    plt.ylim(10**-3, 10**4)
    plt.ylabel('Power spectrum')
    #plt.show()


    return mean_values


def hof_psd_nofilter(data_without_noise):
    psd, frequency = psd_per_channel(data_without_noise)
    mean_values = psd_average(psd, frequency)
    return(psd, mean_values)