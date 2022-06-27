
'function below calculates line of best fit for psd of each epoch and returns the average slope intercept and gradient'
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
    
    psd = [power_array[1] for power_array in welch_channel]

     #save one array of frequency values for plotting 
    frequency = welch_channel[0][0]
        
    return psd, frequency

'''This function is for baseline brainstate file number 2 as the function psd_per_channel does not work in all channels'''

def psd_per_channel_baseline_2(without_artifacts):
    welch_channel = []
    for data_array in without_artifacts:
        welch_channel.append(scipy.signal.welch(data_array, fs=250.4, window='hann', nperseg=1252))
    
    psd = [power_array[1] for power_array in welch_channel]

    return psd

'function below calculates line of best fit for psd of each epoch and returns the average slope intercept and gradient'
def plot_spectral_slope(psd, frequency):

    slope_list = []
    intercept_list = []

    for epoch in psd:
        slope, intercept = np.polyfit(frequency, epoch, 1)
        slope_list.append(slope)
        intercept_list.append(intercept)

    return slope_list, intercept_list 

def get_outlier_values(slope_list, intercept_list):

    intercept_epochs_remove = []
    slope_epochs_remove = []

    for i, item in enumerate(intercept_list):
        if intercept_list[i] > 8:
            intercept_epochs_remove.append(i)

    for i, item in enumerate(slope_list):
        if slope_list[i] < -0.5:
            slope_epochs_remove.append(i)

    return intercept_epochs_remove, slope_epochs_remove

'function below averages psd calculations per frequency and returns a PSD plot'
 
def remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd):

    if len(intercept_epochs_remove) > len(slope_epochs_remove):
        for i in sorted(intercept_epochs_remove, reverse=True):
            del psd[i]
    else:
        for i in sorted(slope_epochs_remove, reverse=True):
            del psd[i]

    return psd

'this function checks plot of linear regression after epochs removed'

def plot_lin_reg(psd, frequency):

    slope_epochs =[]
    intercept_epochs = []

    for epoch in psd:
        plt.semilogy(frequency, epoch)
        slope, intercept = np.polyfit(frequency, epoch, 1)
        slope_epochs.append(slope)
        intercept_epochs.append(intercept)

    return slope_epochs, intercept_epochs

def psd_average(psd,frequency): 

    df_psd = pd.DataFrame(psd)
    mean_values = df_psd.mean(axis=0)
    mean_psd = mean_values.to_numpy()

    print(mean_psd.shape)
    #fig = plt.figure()
    plt.semilogy(frequency, mean_psd)
    plt.xlabel('Frequency [Hz]')
    plt.xlim(1,50)
    plt.ylim(10**-3, 10**4)
    plt.ylabel('Power spectrum')
    #plt.show()


    return mean_psd



def hof_psd_with_specslope_filter(data_without_artifacts):
    psd, frequency = psd_per_channel(data_without_artifacts)
    slope_list, intercept_list = plot_spectral_slope(psd, frequency)
    intercept_epochs_remove, slope_epochs_remove = get_outlier_values(slope_list, intercept_list)
    psd = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
    '''if all epochs exceed the threshold - save the data only for brainstate 1 for that channel'''
    if len(psd) == 0:
        psd = 'CHANNEL EXCEEDS THRESHOLD'
        slope_epochs = 'EPOCHS EXCEED THRESHOLD'
        intercept_epochs = 'EPOCHS EXCEED THRESHOLD'
        return psd, slope_epochs, intercept_epochs
    else:
        slope_epochs, intercept_epochs = plot_lin_reg(psd, frequency)
        mean_values = psd_average(psd, frequency)
        return mean_values, slope_epochs, intercept_epochs

