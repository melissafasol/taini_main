'''Created January 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all functions to load and preprocess saline data (apply main functions to saline data).'''

import pandas as pd
import os 
import numpy as np 
import mne
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy 
from scipy import signal 
import re
from ETX_functions import one_numpy_ETX

from saline_functions import start_saline_dict, concatenate_saline_data, one_numpy_saline

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import brainstate_times, highpass
from psd_taini_mainfunctions import channel_data_extraction, looking_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average
from psd_taini_mainfunctions import starting_times_dict_baseline, channels_dict, genotype_per_animal

saline_two_numpy_file = ['S7070', 'S7071', 'S7074', 'S7075']
saline_one_numpy_file = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072', 'S7076', 'S7083', 'S7086', 'S7087', 'S7088', 'S7091', 'S7092', 'S7094', 'S7096', 'S7098', 'S7101']
seizure_two_numpy_file = ['S7074', 'S7075']
seizure_one_numpy_file = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072','S7088', 'S7092', 'S7094', 'S7096']

channel_number = 11
brain_state_number = 0

path = '/home/melissa/preprocessing/reformatted_brainstates_saline'
saline_2_numpyfiles = []
saline_slope_intercept_2 = []
frequency_values = np.arange(0, 125.2, 0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})
saline_2_numpyfiles.append(frequency_df)


for animal in saline_two_numpy_file:
    concatenate_data, brain_state = concatenate_saline_data(path, channel_number, animal_number= animal, start_saline_dict = start_saline_dict)
    time_values = brainstate_times(brain_state, brain_state_number)
    filtered_data = highpass(concatenate_data)
    datavalues = channel_data_extraction(time_values, filtered_data)
    without_artifacts = remove_noise(datavalues)
    psd, frequency = psd_per_channel(without_artifacts)
    intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd, frequency)
    psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
    slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
    psd_average_results = psd_average(psd_clean, frequency, animal)
    list_mean = list(psd_average_results)
    slope_intercept_df = pd.DataFrame(data = {'animal_number':[animal]*len(slope_epochs), 'slope': slope_epochs, 'Intercept':intercept_epochs})
    saline_slope_intercept_2.append(slope_intercept_df)
    results = pd.DataFrame(data = {animal:list_mean})
    saline_2_numpyfiles.append(results)

merged_2_numpyfiles = pd.concat(saline_2_numpyfiles, axis = 1)
os.chdir('/home/melissa/Results')
merged_2_slope_intercepts = pd.concat(saline_slope_intercept_2, axis=1)
merged_2_numpyfiles.to_csv('wake_saline_power_2.csv', index=False)
merged_2_slope_intercepts.to_csv('wake_slope_intercept_saline_2.csv', index=True)


path = '/home/melissa/preprocessing/reformatted_brainstates_saline'
saline_1_numpyfile = []
saline_slope_intercept_1 = []
frequency_values = np.arange(0,125.2,0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})

for animal in saline_one_numpy_file:
    concatenate_data, brain_state = one_numpy_saline(path, channel_number = 11, animal_number= animal, start_saline_dict = start_saline_dict)
    time_values = brainstate_times(brain_state, brain_state_number)
    filtered_data = highpass(concatenate_data)
    datavalues = channel_data_extraction(time_values, filtered_data)
    without_artifacts = remove_noise(datavalues)
    psd, frequency = psd_per_channel(without_artifacts)
    intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd, frequency)
    psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
    slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
    psd_average_results = psd_average(psd_clean, frequency, animal)
    list_mean = list(psd_average_results)
    slope_intercept_df = pd.DataFrame(data = {'animal_number':[animal]*len(slope_epochs), 'slope': slope_epochs, 'Intercept':intercept_epochs})
    saline_slope_intercept_1.append(slope_intercept_df)
    results = pd.DataFrame(data = {animal:list_mean})
    saline_1_numpyfile.append(results)

merged_1_numpyfile = pd.concat(saline_1_numpyfile, axis = 1)
os.chdir('/home/melissa/Results')
merged_1_slope_intercepts = pd.concat(saline_slope_intercept_1, axis=1)
merged_1_numpyfile.to_csv('_wakesaline_power_1.csv', index=False)
merged_1_slope_intercepts.to_csv('wake_slope_intercept_saline_1.csv', index=True)



