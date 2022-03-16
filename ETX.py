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

os.chdir('/home/melissa/taini_main/')
from preparing_files_functions import hof_extract_brainstate_REM_wake, hof_extract_brainstate_nonREM
from filter_functions import hof_filter
from spectral_slope import hof_psd_with_specslope_filter
from ETX_functions import concatenate_ETX_data, one_numpy_ETX
from constants import ETX_recording_dictionary, start_times_ETX
from save_functions import average_power_df, hof_concatenate_and_save, save_spectral_slope_data, power_df, save_files, concatenate_files

#variables to change
channel_number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
brainstate_number = [0,1,2]
path = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
recording_condition = ['ETX']
save_directory = '/home/melissa/Results/'


for condition in recording_condition: 
    if condition == 'ETX':
        for brainstate in brainstate_number:
            ETX_2_numpyfiles = []
            ETX_1_numpyfile = []
            ETX_slope_intercept_2 = []
            ETX_slope_intercept_1 = []
            frequency_values = np.arange(0, 100, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            ETX_2_numpyfiles.append(frequency_df)
            ETX_1_numpyfile.append(frequency_df)
            for animal in ETX_recording_dictionary['animal_two_numpy_files']:
                for channel in channel_number:
                    concatenate_data, brain_state_file = concatenate_ETX_data(path, channel_number, animal, start_times_ETX)
                    if brainstate == 1:
                        timevalues = hof_extract_brainstate_nonREM(brain_state_file, brainstate)
                    else:
                        timevalues = hof_extract_brainstate_REM_wake(brain_state_file, brainstate)
                    withoutartifacts = hof_filter(concatenate_data,timevalues)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    ETX_slope_intercept_2.append(spectral_data)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    ETX_2_numpyfiles.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/all_channels/ETX_results/two_numpy_file'
            hof_concatenate_and_save(ETX_2_numpyfiles, ETX_slope_intercept_2, save_directory, brainstate, condition)
            ETX_1_numpyfile = []
            ETX_slope_intercept_1 = []
            frequency_values = np.arange(0, 100, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            ETX_1_numpyfile.append(frequency_df)
            for animal in ETX_recording_dictionary['animal_one_numpy_file']:
                for channel in channel_number:
                    concatenate_data, brain_state = one_numpy_ETX(path, channel, animal, start_times_ETX)
                    if brainstate == 1:
                        timevalues_1 = hof_extract_brainstate_nonREM(brain_state, brainstate)
                    else:
                        timevalues_1 = hof_extract_brainstate_REM_wake(brain_state,brainstate)
                    withoutartifacts_1 = hof_filter(concatenate_data, timevalues_1)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts_1)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    ETX_slope_intercept_1.append(spectral_data)
                    ETX_1_numpyfile.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/all_channels/ETX_results/one_numpy_file'
            hof_concatenate_and_save(ETX_1_numpyfile, ETX_slope_intercept_1, save_directory, brainstate, condition)

