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
from psd_taini_mainfunctions import brainstate_times, highpass, channel_data_extraction, look_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average
from constants import start_times_ETX, channels_dict, genotype_per_animal

from ETX_functions import concatenate_ETX_data, one_numpy_ETX

animal_two_numpy_file = ['S7063','S7064', 'S7068', 'S7069', 'S7072', 'S7088', 'S7094', 'S7096'] 
animal_one_numpy_file = ['S7070', 'S7071', 'S7075', 'S7076', 'S7083', 'S7086', 'S7087','S7092', 'S7098', 'S7101', 'S7074', 'S7091']
seizure_two_numpy_file = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072', 'S7094', 'S7096'] #S7088
seizure_one_numpy_file = ['S7074', 'S7075', 'S7076', 'S7092'] #S7098, S7101
channel_number = [4,7,10,11]
brain_state_number = 1


path = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
ETX_2_numpyfiles = []
ETX_slope_intercept_2 = []
frequency_values = np.arange(0,50,0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})
ETX_2_numpyfiles.append(frequency_df)

for animal in animal_two_numpy_file:
    for chan in channel_number:
        concatenate_data, brain_state = concatenate_ETX_data(path, chan, animal_number= animal, start_ETX_time= start_times_ETX)
        time_values = brainstate_times(brain_state, brain_state_number)
        filtered_data = highpass(concatenate_data)
        datavalues = channel_data_extraction(time_values, filtered_data)
        without_artifacts = remove_noise(datavalues)
        noartifacts_array = without_artifacts[0]
        psd, frequency = psd_per_channel(noartifacts_array)
        intercept_epochs_remove, slope_epochs_remove = look_for_outliers(psd, frequency)
        psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
        slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
        psd_average_results = psd_average(psd_clean, frequency, animal)
        print(psd_average_results)
        list_mean = list(psd_average_results)
        spectralslope_df = pd.DataFrame(data = {str(animal) + '_chan_' + str(chan) + '_slope': slope_epochs, str(animal) + '_chan_' + str(chan) + '_intercept':intercept_epochs})
        results=pd.DataFrame(data={
            str(animal) + '_chan' + str(chan):list_mean})
        ETX_2_numpyfiles.append(results)
        ETX_slope_intercept_2.append(spectralslope_df)

merged_2_psd = pd.concat(ETX_2_numpyfiles, axis = 1)
merged_2_spectralslope = pd.concat(ETX_slope_intercept_2, axis=1)
os.chdir('/home/melissa/Results/discarding_epoch_test')
merged_2_psd.to_csv(str(brain_state_number) + 
'_psd_ETX_2.csv', index=True)
merged_2_spectralslope.to_csv(str(brain_state_number) + '_spectralslope_ETX.csv', index=True)

path = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
ETX_1_numpyfile = []
ETX_slope_intercept_1 = []
ETX_1_numpyfile.append(frequency_df)

for animal in animal_one_numpy_file:
    for chan in channel_number:
        concatenate_data, brain_state = one_numpy_ETX(path, chan, animal_number= animal, start_ETX_time= start_times_ETX)
        time_values = brainstate_times(brain_state, brain_state_number)
        filtered_data = highpass(concatenate_data)
        datavalues = channel_data_extraction(time_values, filtered_data)
        without_artifacts = remove_noise(datavalues)
        noartifacts = without_artifacts[0]
        psd, frequency = psd_per_channel(noartifacts)
        print(psd)
        intercept_epochs_remove, slope_epochs_remove = look_for_outliers(psd, frequency)
        psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
        slope_epochs, intercept_epochs = plot_lin_reg(
                                    psd_clean, frequency)
        psd_average_results = psd_average(psd_clean, frequency, animal)
        list_mean = list(psd_average_results)
        slope_intercept_df = pd.DataFrame(
        data = {str(animal) + '_chan_' + str(chan) + '_slope_'
        + str(brain_state_number): slope_epochs, 
        str(animal) + '_' + str(chan) + 'intercept'
        + str(brain_state_number): intercept_epochs})
        results = pd.DataFrame(data = {str(animal) + '_chan_' + 
        str(chan) :list_mean})
        ETX_1_numpyfile.append(results)
        ETX_slope_intercept_1.append(slope_intercept_df)

merged_1_spectralslope = pd.concat(
    ETX_slope_intercept_1, axis = 1)
merged_1_psd = pd.concat(
    ETX_1_numpyfile, axis = 1)

os.chdir('/home/melissa/Results/discarding_epoch_test')
merged_1_psd.to_csv(str(brain_state_number) 
            + '_psd_ETX_1.csv', index=True)
merged_1_spectralslope.to_csv(str(brain_state_number)             + '_spectralslope_ETX.csv', index=True)
