'''Created November 2021
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all functions required to load numpy recordings, 
reformatted brain states per animal and extract data values per brain 
state and then calculate PSD averages.'''


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
import itertools

#Load files, brainstate, starting times per animal and then do analysis together

def load_analysis_files(directory_path, animal_id):
    '''function finds all files for a particular animal'''

    start_1 = '1_' + animal_id + '.pkl' 
    start_2 = '2_' + animal_id + '.pkl'
    
    os.chdir(directory_path)
    animal_recording = [filename for filename in os.listdir(directory_path) if filename.startswith(animal_id)]
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
    start_dict_1 = animal_id + '_1'
    start_dict_2 = animal_id + '_2'
   
    for animal_id in start_times_dict:
        if animal_id == start_dict_1:
            time_1 = start_times_dict[animal_id]
            start_time_1 = time_1[0]
        else:
            if animal_id ==start_dict_2:
                time_2 = start_times_dict[animal_id]
                start_time_2 = time_2[0]
    
    return start_time_1, start_time_2

def load_recording_from_start(recording, channel_number, start_time_1, start_time_2):
    '''function loads recordings using output from previous functions'''
    data_1 = recording[channel_number, start_time_1:]
    data_2 = recording[channel_number, start_time_2:]

    return data_1, data_2


def brainstate_times_REM_wake(brain_state_file, brainstate_number):
    
    #brainstate_number can be 0 - (wake), 1 - (nonREM) or 2 - REM
    
    #functions required for automated script
    #5 second bin definition
    sample_rate = int(250.4*5)
    f1 = lambda a,b: list(range(a,b,sample_rate))


    query = brain_state_file.iloc[:,0] == brainstate_number #REM is 2
        
        
    #find index values in brain state file that correspond to the wake state
    brain_state_indices = brain_state_file[query]
    all_indices = brain_state_indices.index
        
    #now find where these indices jump to separate into epochs
    epoch_indices = []
    starting_index = all_indices[0]
        
    for epoch_index in range(len(all_indices)-1):
        if all_indices[epoch_index] + 1 != all_indices[epoch_index +1]:
            epoch_indices.append([starting_index, all_indices[epoch_index]])
            starting_index = all_indices[epoch_index+1]
                
    #need to append the last value outside of the loop as loop is for len -1
    epoch_indices.append([starting_index, all_indices[-1]])
    
    #now go back to brain states file and slice out start and end time values using the indices 
    time_start_values = []
    time_end_values = []

    for epoch_index in range(len(epoch_indices)):
        time_start_values.append(brain_state_file.iloc[epoch_indices[epoch_index][0],1])
    

    for epoch_index in range(len(epoch_indices)):
        time_end_values.append(brain_state_file.iloc[epoch_indices[epoch_index][1],2])
        
    zipped_timevalues = zip(time_start_values, time_end_values)
    time_values = list(zipped_timevalues)
        
    #multiply each value by sampling rate and convert to integer to be able to access corresponding indices in 
    samplerate_start= [element*250.4 for element in time_start_values]
    samplerate_end = [element*250.4 for element in time_end_values]
    
    int_samplestart = [int(x) for x in samplerate_start]
    int_sampleend = [int(x) for x in samplerate_end]
    
    zipped_timevalues = zip(int_samplestart, int_sampleend)
    time_values = list(zipped_timevalues)
        
    #save map/lambda function to f1 and apply this function to each value in time values variable (separate into 5 second bins)
    timevalues_epochs = list(map(lambda x: f1(x[0], x[1]), (time_values)))
    
    #take them out of list of lists and have one long array with all the time values 
    global timevalues_array
    timevalues_array = np.hstack(timevalues_epochs)
        

    return timevalues_array   

'''This function is only for nonREM epochs'''
def brain_state_times_nonREM(brain_state_file, brain_state_number):
    
    sample_rate = int(250.4*5)
    f1 = lambda a,b: list(range(a,b,sample_rate))

    epoch_indices = []
    epochs_above_five = []
    
    
    if brain_state_number == 1:
        non_REM = brain_state_file.iloc[:,0] == brain_state_number
        nonREM_indices = (brain_state_file[non_REM]).index
        epoch_indices = []
        starting_index = nonREM_indices[0]
        
        for i in range(len(nonREM_indices)-1):
            if nonREM_indices[i] + 1 != nonREM_indices[i+1]:
                epoch_indices.append([starting_index, nonREM_indices[i]])
                starting_index = nonREM_indices[i+1]

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
        
        time_start_values = []
        time_end_values = []

        for time_start_epoch in range(len(new_epochs)):
            time_start_values.append(brain_state_file.iloc[new_epochs[time_start_epoch][0],1])
    
        for time_end_epoch in range(len(new_epochs)):
            time_end_values.append(brain_state_file.iloc[new_epochs[time_end_epoch][1],2])
        
        return time_start_values, time_end_values
        
def timevalues_array_nonREM(time_start_values, time_end_values):
        sample_rate = int(250.4*5)
        f1 = lambda a,b: list(range(a,b,sample_rate))

        zipped_timevalues_1 = zip(time_start_values, time_end_values)
        time_values_1 = list(zipped_timevalues_1)
        
        #multiply each value by sampling rate and convert to integer to be able to access corresponding indices in 
        samplerate_start= [element*250.4 for element in time_start_values]
        samplerate_end = [element*250.4 for element in time_end_values]
    
        int_samplestart = [int(x) for x in samplerate_start]
        int_sampleend = [int(x) for x in samplerate_end]
    
        zipped_timevalues = zip(int_samplestart, int_sampleend)
        time_values = list(zipped_timevalues)
        
        #save map/lambda function to f1 and apply this function to each value in time values variable (separate into 5 second bins)
        timevalues_epochs = list(map(lambda x: f1(x[0], x[1]), (time_values)))

        #take them out of list of lists and have one long array with all the time values 
        global timevalues_array
        timevalues_array_float = np.hstack(timevalues_epochs)
        timevalues_array = [int(value_float) for value_float in timevalues_array_float]
        
        return timevalues_array

'this function filters out low-frequency drifts and frequencies above 50Hz'
def highpass(raw_data):
    lowcut = 0.2
    highcut = 100
    order = 3
    sampling_rate = 250.4
    
    'first function defines the variables for the butter bandpass to get coefficient readouts'
    nyq = 125.2
    low = lowcut/nyq
    high = highcut/nyq 
    butter_b, butter_a = signal.butter(order, [low, high], btype='band', analog = False)

    def butter_bandpass_filter(butter_b, butter_a, raw_data):
        butter_y = signal.filtfilt(butter_b, butter_a, raw_data)
        return butter_y

    global filtered_data
    filtered_data = butter_bandpass_filter(butter_b, butter_a, raw_data)

    return filtered_data

'this function extracts data values which correspond to time values from brain state file'


def channel_data_extraction(timevalues_array, data_file):

    global extracted_datavalues
    extracted_datavalues = []
    
    for time_value in range(len(timevalues_array)):
        start_time_bin = timevalues_array[time_value]
        end_time_bin = timevalues_array[time_value] + 1252
        extracted_datavalues.append(data_file[start_time_bin:end_time_bin])

    return extracted_datavalues


'this function removes epochs with data values that exceed 4000'

def remove_noise(extracted_datavalues):
    
    channel_threshold = []

    for i in range(len(extracted_datavalues)):
        for j in range(len(extracted_datavalues[i])):
            if extracted_datavalues[i][j] >= 3000:
                channel_threshold.append(i)
            else:
                pass
                
    unsorted_duplicate_list = list(set(channel_threshold))
    removing_duplicates = sorted(unsorted_duplicate_list)

    global channels_withoutnoise
    channels_withoutnoise = [i for j, i in enumerate(extracted_datavalues) if j not in removing_duplicates]

    return channels_withoutnoise, removing_duplicates


'this function calculates psd via Welch method on data with noise artifacts removed'

def psd_per_channel(data_without_noise):

    welch_channel = []
    for data_array in data_without_noise:
        welch_channel.append(scipy.signal.welch(data_array, fs=250.4, window='hann', nperseg=1252))
    
    #separate psd values from frequency values
    power_spectrum_list = []

    for power_array in welch_channel:
        power_spectrum_list.append(power_array[1])
    
     #save one array of frequency values for plotting 
    frequency = []
    frequency = welch_channel[0][0]
        
    return welch_channel, power_spectrum_list, frequency

'function below calculates line of best fit for psd of each epoch and returns the average slope intercept and gradient'
def look_for_outliers(psd, frequency):

    global slope_list
    global intercept_list
    slope_list = []
    intercept_list = []

    for epoch in psd:
        plt.semilogy(frequency, epoch)
        slope, intercept = np.polyfit(frequency, epoch, 1)
        slope_list.append(slope)
        intercept_list.append(intercept)

    global average_slope
    global average_intercept

    average_slope = sum(slope_list)/len(slope_list)
    average_intercept = sum(intercept_list)/len(intercept_list)

    intercept_epochs_remove = []
    slope_epochs_remove = []

    for i, item in enumerate(intercept_list):
        if intercept_list[i] > 8:
            intercept_epochs_remove.append(i)

    for i, item in enumerate(slope_list):
        if slope_list[i] < -0.5:
            slope_epochs_remove.append(i)

    return intercept_epochs_remove, slope_epochs_remove

'function below averages psd calculations per frequency and returns a PSD plot'

def remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd):

    if len(intercept_epochs_remove) > len(slope_epochs_remove):
        for i in sorted(intercept_epochs_remove, reverse=True):
            del psd[i]
    else:
        for i in sorted(slope_epochs_remove, reverse=True):
            del psd[i]

    return psd

'this function checks plot of linear regression after epochs removed'

def plot_lin_reg(psd, frequency):

    slope_epochs =[]
    intercept_epochs = []

    for epoch in psd:
        plt.semilogy(frequency, epoch)
        slope, intercept = np.polyfit(frequency, epoch, 1)
        slope_epochs.append(slope)
        intercept_epochs.append(intercept)

#plt.show()
    return slope_epochs, intercept_epochs

def psd_average(psd,frequency, animal_number): 
    
    df_psd = pd.DataFrame(psd)

    global mean_values
    mean_values = df_psd.mean(axis = 0)

    #fig = plt.figure()
    plt.semilogy(frequency, mean_values)
    #plt.xlabel('frequency [Hz]')
    #plt.xlim(1,50)
    #plt.ylim(10**-3, 10**4)
    #plt.ylabel('Power spectrum')
    #fig.suptitle(animal_number)
    #fig.savefig(str(animal_number))
    #plt.show()


    return mean_values


