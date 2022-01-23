'''Created January 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all functions to load and preprocess ETX data (apply 
main functions to ETX data).'''

import pandas as pd
import os 
import numpy as np 
import mne
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy 
from scipy import signal 
import re

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import brainstate_times, highpass
from psd_taini_mainfunctions import channel_data_extraction, looking_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average
from psd_taini_mainfunctions import starting_times_dict_baseline, channels_dict, genotype_per_animal

from ETX_functions import concatenate_ETX_data, one_numpy_ETX

animal_two_numpy_file = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072', 'S7088', 'S7094', 'S7096']
animal_one_numpy_file = ['S7070', 'S7071', 'S7075', 'S7076', 'S7083', 'S7086', 'S7087','S7092', 'S7098', 'S7101', 'S7074', 'S7091']
seizure_two_numpy_file = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072', 'S7088', 'S7094', 'S7096']
seizure_one_numpy_file = ['S7074', 'S7075', 'S7076', 'S7092', 'S7098', 'S7101'] 
channel_number = 4

start_times_ETX = {'S7063_1A': [57121875], 'S7063_2A': [60697836.4],
                       'S7063_1B': [1], 'S7063_2B': [18058597.6],
                       'S7064_1A': [57121875], 'S7064_2A': [60697836.4],
                       'S7064_1B': [1], 'S7064_2B': [18058597.6],
                       'S7068_1A': [54102005], 'S7068_2A': [57016910.4],
                       'S7068_1B': [1], 'S7068_2B': [18719653.6],
                       'S7069_1A': [54102005], 'S7069_2A':[57016910.4],
                       'S7069_1B': [1], 'S7069_2B':[18719653.6],
                       'S7070_1': [59750449], 'S7070_2':[81385008],
                       'S7071_1': [59750449], 'S7071_2':[81385008],
                       'S7072_1A': [38055001], 'S7072_2A':[42442008],
                       'S7072_1B': [1], 'S7072_2B':[17247552],
                       'S7074_1': [14227729], 'S7074_2':[35862288],
                       'S7075_1': [35862289], 'S7075_2':[57496848],
                       'S7076_1': [39212641], 'S7076_2': [60847200],
                       'S7083_1': [18329281], 'S7083_2':[39963840],
                       'S7086_1': [56099617], 'S7086_2': [77734176],
                       'S7087_1': [61358017], 'S7087_2': [82992576],
                       'S7088_1A': [81250043.4], 'S7088_2A': [83683930.4], 
                       'S7088_1B': [1], 'S7088_2B': [19200672], 
                       'S7091_1': [15249361], 'S7091_2': [36883920],
                       'S7092_1': [15249361], 'S7092_2':[36883920],
                       'S7094_1A': [56054795], 'S7094_2A': [61102858],
                       'S7094_1B': [1], 'S7094_2B': [16586496],
                       'S7096_1A': [56054795], 'S7096_2A': [61102858],
                       'S7096_1B':[1], 'S7096_2B': [16586496],
                       'S7098_1': [34419985], 'S7098_2':[56054544],
                       'S7101_1': [34419985], 'S7101_2':[56054544]}

path = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
ETX_2_numpyfiles = []
frequency_values = np.arange(0,125.2,0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})
ETX_2_numpyfiles.append(frequency_df)

for animal in animal_two_numpy_file:
    concatenate_data, brain_state = concatenate_ETX_data(path, channel_number, animal_number= animal, start_ETX_time= start_times_ETX)
    time_values = brainstate_times(brain_state, 0)
    filtered_data = highpass(concatenate_data)
    datavalues = channel_data_extraction(time_values, filtered_data)
    without_artifacts = remove_noise(datavalues)
    psd, frequency = psd_per_channel(without_artifacts)
    intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd, frequency)
    psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
    psd_average_results = psd_average(psd_clean, frequency, animal)
    list_mean = list(psd_average_results)

    results = pd.DataFrame(data = {animal:list_mean})
    ETX_2_numpyfiles.append(results)

merged_2_numpyfiles = pd.concat(ETX_2_numpyfiles, axis = 1)
os.chdir('/home/melissa/Results')
merged_2_numpyfiles.to_csv('testing_ETX_2_numpyfiles.csv', index=True)

path = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
ETX_1_numpyfile = []
frequency_values = np.arange(0,125.2,0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})
ETX_1_numpyfile.append(frequency_df)

for animal in animal_one_numpy_file:
    concatenate_data, brain_state = one_numpy_ETX(path, channel_number, animal_number= animal, start_ETX_time= start_times_ETX)
    time_values = brainstate_times(brain_state, 0)
    filtered_data = highpass(concatenate_data)
    datavalues = channel_data_extraction(time_values, filtered_data)
    without_artifacts = remove_noise(datavalues)
    psd, frequency = psd_per_channel(without_artifacts)
    intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd, frequency)
    psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
    psd_average_results = psd_average(psd_clean, frequency, animal)
    list_mean = list(psd_average_results)

    results = pd.DataFrame(data = {animal:list_mean})
    ETX_1_numpyfile.append(results)

merged_1_numpyfile = pd.concat(ETX_1_numpyfile, axis = 1)
os.chdir('/home/melissa/Results')
merged_1_numpyfile.to_csv('testing_ETX_1_numpyfiles.csv', index=True)
