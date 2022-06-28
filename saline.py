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

os.chdir('/home/melissa/taini_main/')
from prepare_files_functions import hof_extract_brainstate_REM_wake, hof_extract_brainstate_nonREM
from filter_functions import hof_filter
from spectral_slope import hof_psd_with_specslope_filter
from saline_functions import concatenate_saline_data, one_numpy_saline
import ETX_functions
from scripts.constants import saline_recording_dictionary, start_times_saline
from scripts.save_functions import average_power_df, hof_concatenate_and_save, save_spectral_slope_data, power_df, save_files, concatenate_files
from filter_functions import highpass, channel_data_extraction, remove_noise

path = '/home/melissa/preprocessing/reformatted_brainstates_saline'

#variables to change
channel_number = [11]
brainstate_number = [2,1,0]
directory_name = '/home/melissa/preprocessing/reformatted_brainstates_saline'
recording_condition = ['saline', 'baseline', 'ETX']
save_directory = '/home/melissa/preprocessing/'



for condition in recording_condition: 
    if condition == 'saline':
        for brainstate in brainstate_number:
            saline_2_numpyfiles = []
            saline_slope_intercept_2 = []
            frequency_values = np.arange(0, 100, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            saline_2_numpyfiles.append(frequency_df)
            for animal in saline_recording_dictionary['animal_two_numpy_files']:
                for channel in channel_number:
                    concatenate_data, brain_state_file = concatenate_saline_data(path, channel_number, animal, start_times_saline)
                    #if brainstate == 1:
                     #   timevalues = hof_extract_brainstate_nonREM(brain_state_file, brainstate)
                    #else:
                    timevalues = hof_extract_brainstate_REM_wake(brain_state_file, brainstate)
                    withoutartifacts = hof_filter(concatenate_data,timevalues)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    saline_slope_intercept_2.append(spectral_data)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    saline_2_numpyfiles.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/'
            hof_concatenate_and_save(saline_2_numpyfiles, saline_slope_intercept_2, save_directory, brainstate, condition)
            saline_1_numpyfile = []
            saline_slope_intercept_1 = []
            frequency_values = np.arange(0, 100, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            saline_1_numpyfile.append(frequency_df)
            for animal in saline_recording_dictionary['animal_one_numpy_file']:
                for channel in channel_number:
                    concatenate_data, brain_state = one_numpy_saline(path, channel, animal, start_times_saline)
                    #if brainstate == 1:
                        #timevalues_1 = hof_extract_brainstate_nonREM(brain_state, brainstate)
                    #else:
                    timevalues_1 = hof_extract_brainstate_REM_wake(brain_state,brainstate)
                    #if animal == 'S7094':
                     #   filtered_data = highpass(concatenate_data)
                      #  datavalues = channel_data_extraction(timevalues_1, filtered_data)
                       # withoutartifacts_1 = remove_noise(datavalues)
                    #else:
                    withoutartifacts_1 = hof_filter(concatenate_data, timevalues_1)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts_1)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    saline_slope_intercept_1.append(spectral_data)
                    saline_1_numpyfile.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/'
            hof_concatenate_and_save(saline_1_numpyfile, saline_slope_intercept_1, save_directory, brainstate, condition)

