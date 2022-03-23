
##all required imports 
import pandas as pd
import os
import numpy as np
import mne
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os
import scipy
from scipy import signal
import re
import numpy as np
import itertools

#Load files, brainstate, starting times per animal and then do analysis together


def load_analysis_files(directory_path, animal_id):
    '''function finds all files for a particular animal'''

    start_1 = '1_' + animal_id + '.pkl' 
    start_2 = '2_' + animal_id + '.pkl'
        
    os.chdir(directory_path)
    animal_recording = [filename for filename in os.listdir(directory_path) if filename.startswith(animal_id)]
    print(animal_recording)
    recording = np.load(animal_recording[0])
    brain_file_1 = [filename for filename in os.listdir(directory_path) if filename.endswith(start_1)]
    brain_state_1 = pd.read_pickle(brain_file_1[0])
    brain_file_2 = [filename for filename in os.listdir(directory_path) if filename.endswith(start_2)]
    if len(brain_file_2) > 0:
        brain_state_2 = pd.read_pickle(brain_file_2[0])
    else:
        brain_state_2 = None
        
    return recording, brain_state_1, brain_state_2

def get_start_times(start_times_dict, animal_id):
    '''function finds corresponding start times for animal, brainstate and recording condition'''
    
    check_keys = [k for k, v in start_times_dict.items() if animal_id in k]
    print(check_keys)
    if len(check_keys) == 2:
        start_time_1 = start_times_dict[check_keys[0]]
        print(start_time_1)
        start_time_1 = start_time_1[0]
        start_time_2 = start_times_dict[check_keys[1]]
        print(start_time_2)
        start_time_2 = start_time_2[0]
    if len (check_keys) == 1:
        start_time_1 = start_times_dict[check_keys[0]]
        start_time_1 = start_time_1[0]
        start_time_2 = None
    return start_time_1, start_time_2

def load_recording_from_start(recording, channel, start_time_1, start_time_2):
    '''function loads recordings using output from previous functions'''
    data_1 = recording[channel, start_time_1:]
    
    if start_time_2 == None:
        data_2 = None
    else:
        data_2 = recording[channel, start_time_2:]

    return data_1, data_2

def hof_load_files(directory_path, animal_id, start_times_dict, channel):
    recording, brain_state_1, brain_state_2 = load_analysis_files(directory_path, animal_id)
    start_time_1, start_time_2 = get_start_times(start_times_dict, animal_id)
    data_1, data_2 = load_recording_from_start(recording, channel, start_time_1, start_time_2)
    print('all_data_loaded for_' + str(animal_id))
    return data_1, data_2, brain_state_1, brain_state_2

def brainstate_indices(brainstate_file, brainstate_number):
    #function to find indices in brainstate file which correspond to brainstate_number
    index_brainstate = brainstate_file.loc[brainstate_file['brainstate'] == brainstate_number]
    all_indices = index_brainstate.index

    return all_indices

def find_index_jumps(all_indices):
    #now find where these indices jump into separate epochs
    epoch_indices = []
    starting_index = all_indices[0]
        
    for epoch_index in range(len(all_indices)-1):
        if all_indices[epoch_index] + 1 != all_indices[epoch_index +1]:
            epoch_indices.append([starting_index, all_indices[epoch_index]])
            starting_index = all_indices[epoch_index+1]
                
    #need to append the last value outside of the loop as loop is for len -1
    epoch_indices.append([starting_index, all_indices[-1]])
    
    return epoch_indices

def get_data_indices(brainstate_file, epoch_indices):
    sample_rate = 250.4
    time_start_values = []
    time_end_values = []

    for epoch_index in range(len(epoch_indices)):
        time_start_values.append(brainstate_file.iloc[epoch_indices[epoch_index][0],1])
    
    for epoch_index in range(len(epoch_indices)):
        time_end_values.append(brainstate_file.iloc[epoch_indices[epoch_index][1],2])

    samplerate_start = [int(element*sample_rate) for element in time_start_values]
    samplerate_end = [int(element*sample_rate) for element in time_end_values]
    zipped_timevalues = list(zip(samplerate_start, samplerate_end))

    return zipped_timevalues

def separate_data_timebins(zipped_timevalues):
    epoch_length = int(250.4*5)
    function_timebins = lambda epoch_start, epoch_end: list(range(epoch_start, epoch_end, epoch_length))

    timevalues_epochs = list(map(lambda x: function_timebins(x[0], x[1]), (zipped_timevalues)))
    timevalues_array = np.hstack(timevalues_epochs)
    return timevalues_array

def hof_extract_brainstate_REM_wake(brainstate_file, brainstate_number):
    all_indices = brainstate_indices(brainstate_file, brainstate_number)
    epoch_indices = find_index_jumps(all_indices)
    zipped_timevalues = get_data_indices(brainstate_file, epoch_indices)
    timevalues_array = separate_data_timebins(zipped_timevalues)
    print('timevalues extracted')
    return timevalues_array

def non_REM_epoch_deletion(epoch_indices):
    epochs_above_five = []
    for epoch in epoch_indices:
            epoch_length = epoch[1] - epoch[0]
            if epoch_length >= 5:
                epochs_above_five.append(epoch)
                
    new_epochs = []
    for epoch in epochs_above_five:
            start_epoch = epoch[0] + 2
            end_epoch = epoch[1] - 2
            new_epoch_pair = start_epoch, end_epoch
            new_epochs.append(new_epoch_pair)
            
    return new_epochs

def hof_extract_brainstate_nonREM(brainstate_file, brainstate_number):
    all_indices = brainstate_indices(brainstate_file, brainstate_number)
    epoch_indices = find_index_jumps(all_indices)
    new_epochs = non_REM_epoch_deletion(epoch_indices)
    zipped_timevalues = get_data_indices(brainstate_file, new_epochs)
    timevalues_array = separate_data_timebins(zipped_timevalues)
    print('timevalues extracted')
    return timevalues_array


