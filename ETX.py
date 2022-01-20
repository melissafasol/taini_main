'''Created January 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all functions to load and preprocess ETX data (apply 
main functions to ETX data).'''


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

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import brainstate_times, highpass, channel_data_extraction, loading_analysis_files_onebrainstate, looking_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average
from psd_taini_mainfunctions import channels_dict, genotype_per_animal

start_times_dict_ETX = {'S7063_1A': [57121875], 'S7063_2A': [60697836.4],
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
                       'S7088_1A': [81250043.4], 'S7088_2A': [83683930.4], 
                       'S7088_2A': [1], 'S7088_2B': [19200672], 
                       'S7091_1': [15249361], 'S7091_2': [36883920],
                       'S7092_1': [15249361], 'S7092_2':[36883920],
                       'S7094_1A': [56054795], 'S7094_2A': [61102858],
                       'S7094_1B': [1], 'S7094_2B': [16586496],
                       'S7098_1': [34419985], 'S7098_2':[56054544],
                       'S7101_1': [34419985], 'S7101_2':[56054544]}





def concatenate_ETX_data(path, channel_number, animal_number, start_ETX_time):

    start_1A = animal_number + '_1A'
    end_1A = animal_number + '_2A'
    start_1B = animal_number + '_1B'
    end_1B = animal_number + '_2B'

    files = []

    for r, d,f in os.walk(path):
        for file in f:
            if animal_number in file:
                files.append(os.path.join(r, file))
    
    print(files)

    for recording in files:
        if recording.endswith('ETX_A.npy'):
            numpy_A = np.load(recording)
        elif recording.endswith('ETX_B.npy'):
            numpy_B = np.load(recording)

    for animal_id in start_ETX_time:
        if animal_id == start_1A:
            start_1 = start_ETX_time[animal_id]
        elif animal_id == end_1A:
            end_1 = start_ETX_time[animal_id]
        elif animal_id == start_1B:
            start_2 = start_ETX_time[animal_id]
        elif animal_id == end_1B:
            end_2 = start_ETX_time[animal_id]
    
    start_1 = int(start_1[0])
    end_1 = int(end_1[0])
    start_2 = int(start_1[0])
    end_2 = int(start_1[0])
    print(start_1, end_1, start_2, end_2)

    #extract rows corresponding to channel number and parse out data between start and end times
    recording_1 = numpy_A[channel_number, start_1:end_1]
    recording_2 = numpy_A[channel_number, start_2:end_2]
    
    #concatenate recording 1 and 2 into one dataset

    concatenate_dataset = np.concatenate((recording_1, recording_2))

    for brain_state_file in files:
        if brain_state_file.endswith('.pkl'):
            brain_state = pd.read_pickle(brain_state_file)

    return concatenate_dataset, brain_state



animal_two_numpy_files = ['S7063', 'S7064', 'S7068', 'S7069', 'S7072', 'S7094']
channel_number = [5,6,8,9]
path = '/home/melissa/preprocessing/reformatted_brainstates_ETX'

#loop below calculates psd average per channel for ETX datasets with 2 numpy files
for i in range(len(animal_two_numpy_files)-1):
    animal_number = i
    for j in range(len(channel_number)):
        concatenate_dataset, brain_state = concatenate_ETX_data(path = path, channel_number = channel_number[j], animal_number=animal_number, start_ETX_time=start_times_dict_ETX)
        time_values = brainstate_times(brain_state, 2)
        filtered_data = highpass(concatenate_dataset)
        datavalues = channel_data_extraction(time_values, filtered_data)
        without_artifacts = remove_noise(datavalues)
        psd, frequency = psd_per_channel(without_artifacts)
        intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd, frequency)
        psd_cleaned = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
        psd_average = (psd_cleaned, frequency, animal_number)
        list_mean = list(psd_average)

        for animal in genotype_per_animal:
            if animal == animal_number:
                genotype = genotype_per_animal[animal]
        print(genotype)

        sleepstate = ['REM']
        recordingtype = ['ETX']
        results_channel_number = [channel_number[j]]
        results = {'Animal_Number':[animal_number]*627,
        'Channel_Number': results_channel_number*627,
        'Genotype':genotype*627, 'Sleep_State' : sleepstate*627, 'Recording_Type': recordingtype*627,
        'Frequency': frequency, 'Power': list_mean}

