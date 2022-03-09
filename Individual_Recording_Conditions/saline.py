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
from Individual_Recording_Conditions.ETX_functions import one_numpy_ETX

from Individual_Recording_Conditions.saline_functions import start_saline_dict, concatenate_saline_data, one_numpy_saline

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import  brainstate_times_REM_wake, brain_state_times_nonREM, timevalues_array_nonREM
from psd_taini_mainfunctions import highpass, channel_data_extraction, look_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average

from constants import start_times_saline, channels_dict
from save_functions import concatenate_files, save_files

#variables specific for saline datasets
saline_two_numpy_file = ['S7070', 'S7071', 'S7074', 'S7075']
saline_one_numpy_file = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072', 'S7076', 'S7083', 'S7086', 'S7087', 'S7088', 'S7091', 'S7092', 'S7094', 'S7096', 'S7098', 'S7101']
seizure_two_numpy_file = ['S7074', 'S7075']
seizure_one_numpy_file = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072','S7088', 'S7092', 'S7094', 'S7096']
path = '/home/melissa/preprocessing/reformatted_brainstates_saline'

#variables to change
channel_number = [4,7,10,11]
brain_state_number = 2
directory_name = '/home/melissa/Results'

#empty lists 
saline_2_numpyfiles = []
saline_1_numpyfile = []
saline_slope_intercept_2 = []
saline_slope_intercept_1 = []
frequency_values = np.arange(0, 100, 0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})
saline_2_numpyfiles.append(frequency_df)



for animal in saline_two_numpy_file:
    for channel in channel_number:
        concatenate_data, brain_state = concatenate_saline_data(path, channel_number, animal, start_times_saline)
        if brain_state_number == 1:
            time_start_values, time_end_values = brain_state_times_nonREM(brain_state, brain_state_number)
            timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
        else:
            timevalues = brainstate_times_REM_wake(brain_state, brain_state_number)
        filtered_data = highpass(concatenate_data)
        datavalues = channel_data_extraction(timevalues, filtered_data)
        without_artifacts = remove_noise(datavalues)
        psd, frequency = psd_per_channel(without_artifacts)
        intercept_epochs_remove, slope_epochs_remove = look_for_outliers(psd, frequency)
        psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
        slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
        psd_average_results = psd_average(psd_clean, frequency, animal)
        list_mean = list(psd_average_results)
        results = pd.DataFrame(data = {str(brain_state) + animal + '_chan_' + str(channel):list_mean})
        data = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs, 
                str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs})
        saline_2_numpyfiles.append(results)
        saline_slope_intercept_2.append(data)

merged_power_file, merged_gradient_file = concatenate_files(saline_2_numpyfiles, saline_slope_intercept_2)
save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, recording_condition = 'saline')


path = '/home/melissa/preprocessing/reformatted_brainstates_saline'
saline_1_numpyfile = []
saline_slope_intercept_1 = []
frequency_values = np.arange(0,125.2,0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})

for animal in saline_one_numpy_file:
    for channel in channel_number:
        concatenate_data, brain_state = one_numpy_saline(path, channel, animal, start_times_saline)
        if brain_state_number == 1:
                time_start_values, time_end_values = brain_state_times_nonREM(brain_state, brain_state_number)
                timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
        else:
            timevalues = brainstate_times_REM_wake(brain_state, brain_state_number)
        filtered_data = highpass(concatenate_data)
        datavalues = channel_data_extraction(timevalues, filtered_data)
        without_artifacts = remove_noise(datavalues)
        psd, frequency = psd_per_channel(without_artifacts)
        intercept_epochs_remove, slope_epochs_remove = look_for_outliers(psd, frequency)
        psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
        slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
        psd_average_results = psd_average(psd_clean, frequency, animal)
        list_mean = list(psd_average_results)
        results = pd.DataFrame(data = {str(brain_state) + animal + '_chan_' + str(channel):list_mean})
        data = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs, 
                str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs})
        saline_1_numpyfile.append(results)
        saline_slope_intercept_1.append(data)

merged_power_file, merged_gradient_file = concatenate_files(saline_1_numpyfile, saline_slope_intercept_1)
save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, recording_condition = 'saline')
