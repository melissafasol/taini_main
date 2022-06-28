'''Created November 2021
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This script is to apply functions to all datasets'''

from power_functions import hof_psd_nofilter
from prepare_files_functions import hof_load_files, hof_extract_brainstate_REM_wake, hof_extract_brainstate_nonREM
from filter_functions import hof_filter
from spectral_slope import hof_psd_with_specslope_filter
import saline_functions
import ETX_functions
from scripts.constants import baseline_recording_dictionary, start_times_baseline, saline_recording_dictionary, start_times_saline, ETX_recording_dictionary, start_times_ETX, start_times_S7096_baseline
from scripts.save_functions import average_power_df, hof_concatenate_and_save, save_spectral_slope_data, power_df, save_files, concatenate_files
from saline_functions import concatenate_saline_data, one_numpy_saline
from ETX_functions import concatenate_ETX_data, one_numpy_ETX
from S7096 import concatenate_S7096
from filter_functions import highpass, channel_data_extraction, remove_noise





#other required imports 
import pandas as pd 
import os
import numpy as np
import mne 
import matplotlib.pyplot as plt
import scipy
from scipy.fft import fft, fftfreq
from scipy import signal
import re
import statistics
from pandas import ExcelWriter
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average



channel_number = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
recording_condition = ['saline', 'ETX', 'baseline']
brainstate_number = [4]

#empty lists 
for condition in recording_condition:
    print(condition)
    #empty lists
    if condition == 'baseline':
        directory_path = '/home/melissa/preprocessing/numpyformat_baseline' 
        for brainstate in brainstate_number:
            small_dfs_two_brainstates = []
            small_dfs_one_brainstate = []
            slopegradient_intercept_2_brainstate = []
            slopegradient_intercept_1_brainstate = []
            frequency_values = np.arange(0, 125.2, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            small_dfs_two_brainstates.append(frequency_df)
            small_dfs_one_brainstate.append(frequency_df)
            for animal in baseline_recording_dictionary['seizure_two_brainstates']:
                 for channel in channel_number:
                    data_1, data_2, brain_state_1, brain_state_2 = hof_load_files(directory_path, animal, start_times_baseline, channel)
                    timevalues_1 = hof_extract_brainstate_REM_wake(brain_state_1,brainstate)
                    timevalues_2 = hof_extract_brainstate_REM_wake(brain_state_2,brainstate)
                    withoutartifacts_1 = hof_filter(data_1,timevalues_1)
                    withoutartifacts_2 = hof_filter(data_2,timevalues_2)        
                    psd_mean_1, slope_1, intercept_1 =  hof_psd_with_specslope_filter(withoutartifacts_1)
                    psd_mean_2, slope_2, intercept_2 = hof_psd_with_specslope_filter(withoutartifacts_2)
                    '''the following if statements are for noisy datasets in which all datapoints exceed the threshold'''
                    if type(psd_mean_1) and type(psd_mean_2) == str:
                         continue
                    elif type(psd_mean_1) == str:
                         spectral_data = save_spectral_slope_data(slope_2, intercept_2, brainstate, animal, channel)
                         power_data = power_df(psd_mean_2, brainstate, animal, channel)
                         slopegradient_intercept_1_brainstate.append(spectral_data)
                         small_dfs_one_brainstate.append(power_data)
                    elif type(psd_mean_2) == str:
                         spectral_data = save_spectral_slope_data(slope_1, intercept_1, brainstate, animal, channel)
                         power_data = power_df(psd_mean_1, brainstate, animal, channel)
                         slopegradient_intercept_1_brainstate.append(spectral_data)
                         small_dfs_one_brainstate.append(power_data)
                    else:
                         spectral_data_1 = save_spectral_slope_data(slope_1, intercept_1, brainstate, animal, channel)
                         spectral_data_2 = save_spectral_slope_data(slope_2, intercept_2, brainstate, animal, channel)
                         slopegradient_intercept_2_brainstate.append(spectral_data_1)
                         slopegradient_intercept_2_brainstate.append(spectral_data_2)
                         average_power = average_power_df(psd_mean_1, psd_mean_2)
                         power_data = power_df(average_power, brainstate, animal, channel)
                         small_dfs_two_brainstates.append(power_data)
            os.chdir('/home/melissa/Results/test_2')
            merged_power_file_2 = pd.concat(small_dfs_two_brainstates, axis=1)
            merged_power_file_2.to_csv('seizures_baseline_2_file.csv')
            os.chdir('/home/melissa/preprocessing/numpyformat_baseline') 
            for animal in baseline_recording_dictionary['seizure_one_brainstate']:
                  for channel in channel_number:
                      data_1, data_2, brain_state_1, brain_state_2 = hof_load_files(directory_path, animal, start_times_baseline, channel)
                      timevalues_1 = hof_extract_brainstate_REM_wake(brain_state_1,brainstate)
                      withoutartifacts_1 = hof_filter(data_1, timevalues_1)
                      psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts_1)
                      spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                      power_data = power_df(psd_mean, brainstate, animal, channel)
                      slopegradient_intercept_1_brainstate.append(spectral_data)
                      small_dfs_one_brainstate.append(power_data)
            os.chdir('/home/melissa/Results/test_1')
            merged_power_file_1 = pd.concat(small_dfs_one_brainstate, axis=1)
            merged_power_file_1.to_csv('seizures_baseline_1_file.csv')
    