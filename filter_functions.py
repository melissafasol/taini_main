'''Created November 2021
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all filter functions to apply to EEG taini recordings.'''

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

'this function filters out low-frequency drifts and frequencies above 50Hz'
def highpass(raw_data):
    lowcut = 0.2
    highcut = 100
    order = 3
    sampling_rate = 250.4
    
    'first function defines the variables for the butter bandpass to get coefficient readouts'
    nyq = 125.2
    low = lowcut/nyq
    high = highcut/nyq 
    butter_b, butter_a = signal.butter(order, [low, high], btype='band', analog = False)

    def butter_bandpass_filter(butter_b, butter_a, raw_data):
        butter_y = signal.filtfilt(butter_b, butter_a, raw_data)
        return butter_y

    global filtered_data
    filtered_data = butter_bandpass_filter(butter_b, butter_a, raw_data)

    return filtered_data

'this function removes epochs with data values that exceed 3000'

def channel_data_extraction(timevalues_array, data_file):
    
    extracted_datavalues = []

    for time_value in range(len(timevalues_array)):
        start_time_bin = timevalues_array[time_value]
        end_time_bin = timevalues_array[time_value] + 1252
        extracted_datavalues.append(data_file[start_time_bin:end_time_bin])

    return extracted_datavalues


def remove_noise(extracted_datavalues):
    
    channel_threshold = []

    for i in range(len(extracted_datavalues)):
        for j in range(len(extracted_datavalues[i])):
            if extracted_datavalues[i][j] >= 3000:
                channel_threshold.append(i)
            else:
                pass
    
    unsorted_duplicate_list = list(set(channel_threshold))
    removing_duplicates = sorted(unsorted_duplicate_list)
    channels_withoutnoise = [i for j, i in enumerate(extracted_datavalues) if j not in removing_duplicates]

    return channels_withoutnoise

def hof_filter(raw_data, timevalues_array):
    filtered_data = highpass(raw_data)
    datavalues = channel_data_extraction(timevalues_array, filtered_data)
    withoutartifacts = remove_noise(datavalues)
    print('All filtering complete')
    return withoutartifacts