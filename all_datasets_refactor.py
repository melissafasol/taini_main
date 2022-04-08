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
from constants import baseline_recording_dictionary, start_times_baseline, saline_recording_dictionary, start_times_saline, ETX_recording_dictionary, start_times_ETX, start_times_S7096_baseline
from save_functions import average_power_df, hof_concatenate_and_save, save_spectral_slope_data, power_df, save_files, concatenate_files
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



channel_number = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
recording_condition = ['baseline', 'saline', 'ETX']
brainstate_number = [0]

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
             #for animal in baseline_recording_dictionary['animal_two_brainstates']:
                # for channel in channel_number:
                  #   data_1, data_2, brain_state_1, brain_state_2 = hof_load_files(directory_path, animal, start_times_baseline, channel)
                   #  timevalues_1 = hof_extract_brainstate_REM_wake(brain_state_1,brainstate)
                    # timevalues_2 = hof_extract_brainstate_REM_wake(brain_state_2,brainstate)
                    # withoutartifacts_1 = hof_filter(data_1,timevalues_1)
                     #withoutartifacts_2 = hof_filter(data_2,timevalues_2)        
                    # psd_mean_1, slope_1, intercept_1 =  #hof_psd_with_specslope_filter(withoutartifacts_1)
                   #  psd_mean_2, slope_2, intercept_2 = hof_psd_with_specslope_filter(withoutartifacts_2)
                    # '''the following if statements are for noisy datasets in which all datapoints exceed the threshold'''
                  #   if type(psd_mean_1) and type(psd_mean_2) == str:
                    #     continue
                  #   elif type(psd_mean_1) == str:
                   #      spectral_data = save_spectral_slope_data(slope_2, intercept_2, brainstate, animal, channel)
                    #     power_data = power_df(psd_mean_2, brainstate, animal, channel)
                    #     slopegradient_intercept_1_brainstate.append(spectral_data)
                    #     small_dfs_one_brainstate.append(power_data)
                  #   elif type(psd_mean_2) == str:
                   #      spectral_data = save_spectral_slope_data(slope_1, intercept_1, brainstate, animal, channel)
                   #      power_data = power_df(psd_mean_1, brainstate, animal, channel)
                    #     slopegradient_intercept_1_brainstate.append(spectral_data)
                    #     small_dfs_one_brainstate.append(power_data)
                     #else:
                      #   spectral_data_1 = save_spectral_slope_data(slope_1, intercept_1, brainstate, animal, channel)
                      #   spectral_data_2 = save_spectral_slope_data(slope_2, intercept_2, brainstate, animal, channel)
                      #   slopegradient_intercept_2_brainstate.append(spectral_data_1)
                     #    slopegradient_intercept_2_brainstate.append(spectral_data_2)
                     #    average_power = average_power_df(psd_mean_1, psd_mean_2)
                     #    power_data = power_df(average_power, brainstate, animal, channel)
                     #    small_dfs_two_brainstates.append(power_data)
             #save_directory = '/home/melissa/Results/march_refactor_test/all_channels/baseline/two_numpy_file'
             #hof_concatenate_and_save(small_dfs_two_brainstates, slopegradient_intercept_2_brainstate, save_directory, brainstate, condition)
            for animal in baseline_recording_dictionary['animal_one_brainstate_1']:
                for channel in channel_number:
                    data_1, data_2, brain_state_1, brain_state_2 = hof_load_files(directory_path, animal, start_times_baseline, channel)
                    timevalues_1 = hof_extract_brainstate_REM_wake(brain_state_1,brainstate)
                    withoutartifacts_1 = hof_filter(data_1, timevalues_1)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts_1)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    slopegradient_intercept_1_brainstate.append(spectral_data)
                    small_dfs_one_brainstate.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/all_channels/baseline/one_numpy_file'
            hof_concatenate_and_save(small_dfs_one_brainstate, slopegradient_intercept_1_brainstate, save_directory, brainstate, condition)
    if condition == 'saline':
        path = '/home/melissa/preprocessing/reformatted_brainstates_saline'
        for brainstate in brainstate_number:
            saline_2_numpyfiles = []
            saline_slope_intercept_2 = []
            frequency_values = np.arange(0, 100, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            saline_2_numpyfiles.append(frequency_df)
            for animal in saline_recording_dictionary['animal_two_numpy_files']:
                for channel in channel_number:
                    concatenate_data, brain_state_file = concatenate_saline_data(path, channel_number, animal, start_times_saline)
                    timevalues = hof_extract_brainstate_REM_wake(brain_state_file, brainstate)
                    withoutartifacts = hof_filter(concatenate_data,timevalues)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    saline_slope_intercept_2.append(spectral_data)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    saline_2_numpyfiles.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/all_channels/saline/two_numpy_file'
            hof_concatenate_and_save(saline_2_numpyfiles, saline_slope_intercept_2, save_directory, brainstate, condition)
            saline_1_numpyfile = []
            saline_slope_intercept_1 = []
            frequency_values = np.arange(0, 100, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            saline_1_numpyfile.append(frequency_df)
            for animal in saline_recording_dictionary['animal_one_numpy_file']:
                for channel in channel_number:
                    concatenate_data, brain_state = one_numpy_saline(path, channel, animal, start_times_saline)
                    timevalues_1 = hof_extract_brainstate_REM_wake(brain_state,brainstate)
                    withoutartifacts_1 = hof_filter(concatenate_data, timevalues_1)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts_1)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    saline_slope_intercept_1.append(spectral_data)
                    saline_1_numpyfile.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/all_channels/saline/one_numpy_file'
            hof_concatenate_and_save(saline_1_numpyfile, saline_slope_intercept_1, save_directory, brainstate, condition)
    if condition == 'ETX':
        path = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
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
                    timevalues = hof_extract_brainstate_REM_wake(brain_state_file, brainstate)
                    withoutartifacts = hof_filter(concatenate_data,timevalues)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    ETX_slope_intercept_2.append(spectral_data)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    ETX_2_numpyfiles.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/all_channels/ETX/two_numpy_file'
            hof_concatenate_and_save(ETX_2_numpyfiles, ETX_slope_intercept_2, save_directory, brainstate, condition)
            ETX_1_numpyfile = []
            ETX_slope_intercept_1 = []
            frequency_values = np.arange(0, 100, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            ETX_1_numpyfile.append(frequency_df)
            for animal in ETX_recording_dictionary['animal_one_numpy_file']:
                for channel in channel_number:
                    concatenate_data, brain_state = one_numpy_ETX(path, channel, animal, start_times_ETX)
                    timevalues_1 = hof_extract_brainstate_REM_wake(brain_state,brainstate)
                    withoutartifacts_1 = hof_filter(concatenate_data, timevalues_1)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts_1)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    ETX_slope_intercept_1.append(spectral_data)
                    ETX_1_numpyfile.append(power_data)
            save_directory = '/home/melissa/Results/march_refactor_test/all_channels/ETX/one_numpy_file'
            hof_concatenate_and_save(ETX_1_numpyfile, ETX_slope_intercept_1, save_directory, brainstate, condition)



