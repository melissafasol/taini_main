'''Created November 2021
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This script is to apply functions to all datasets'''

from prepare_files_functions import hof_load_files, hof_extract_brainstate_REM_wake, hof_extract_brainstate_nonREM
from filter_functions import hof_filter
from spectral_slope import hof_psd_with_specslope_filter
import saline_functions
import ETX_functions
from scripts.constants import baseline_recording_dictionary, start_times_baseline
from save_functions import average_power_df, hof_concatenate_and_save, save_spectral_slope_data, power_df, save_files, concatenate_files

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


directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
channel_number = [11]
recording_condition = ['baseline', 'saline', 'ETX']
brainstate_number = [2, 1, 0]

#empty lists



for condition in recording_condition:
    print(condition)
    #empty lists
    if condition == 'baseline': 
        for brainstate in brainstate_number:
            small_dfs_two_brainstates = []
            small_dfs_one_brainstate = []
            slopegradient_intercept_2_brainstate = []
            slopegradient_intercept_1_brainstate = []
            frequency_values = np.arange(0, 125.2, 0.2)
            frequency_df = pd.DataFrame({'Frequency': frequency_values})
            small_dfs_two_brainstates.append(frequency_df)
            small_dfs_one_brainstate.append(frequency_df)
            for animal in baseline_recording_dictionary['animal_one_brainstate']:
                for channel in channel_number:
                    data_1, data_2, brain_state_1, brain_state_2 = hof_load_files(directory_path, animal, start_times_baseline, channel)
                    if brainstate == 1:
                        timevalues_1 = hof_extract_brainstate_nonREM(brain_state_1, brainstate)
                    else:
                        timevalues_1 = hof_extract_brainstate_REM_wake(brain_state_1,brainstate)
                    os.chdir('/home/melissa/Results/testing_brainstate_extraction')
                    np.save('timevalues' + str(brainstate) + str(animal), timevalues_1)
                    withoutartifacts_1 = hof_filter(data_1, timevalues_1)
                    psd_mean, slope, intercept = hof_psd_with_specslope_filter(withoutartifacts_1)
                    spectral_data = save_spectral_slope_data(slope, intercept, brainstate, animal, channel)
                    power_data = power_df(psd_mean, brainstate, animal, channel)
                    slopegradient_intercept_1_brainstate.append(spectral_data)
                    small_dfs_one_brainstate.append(power_data)
            #save_directory = '/home/melissa/Results/march_refactor_test/baseline_one_numpy_file'
            #hof_concatenate_and_save(small_dfs_one_brainstate, slopegradient_intercept_1_brainstate, save_directory, brainstate, condition)

