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

#Load files, brainstate, starting times per animal and then do analysis together

def load_analysis_files(path, animal_number, start_times_dict, channel_number):
    #specify starting time to use in dictionary 
    starting_1 = animal_number + '_1'
    starting_2 = animal_number + '_2'

    files=[]

    for r, d, f in os.walk(path):
        for file in f:
            if animal_number in file:
                files.append(os.path.join(r, file))
        
    #load numpy file and corresponding brain state 
    for f in files:
        print(f)

    #load data corresponding to animal number
    for x in files:
        if x.endswith('npy'):
            data = np.load(x)

    #finding brain state files 
    for y in files:
        if y.endswith('1_' + animal_number + '.pkl'):
            global brain_state_1
            global brain_state_2
            brain_state_1 = pd.read_pickle(y)
        else:
            if y.endswith('2_' + animal_number + '.pkl'):
                brain_state_2 = pd.read_pickle(y)
    

    #finding start times for specific animal from start_times dictionary 
    global animal_id
    for animal_id in start_times_dict:
        if animal_id == starting_1:
            global time_1
            global time_2
            time_1 = start_times_dict[animal_id]
        else:
            if animal_id ==starting_2:
                time_2 = start_times_dict[animal_id]
            
    x = time_1[0]
    y = time_2[0]
    
    global data_baseline1
    global data_baseline2

    data_baseline1 = data[channel_number, x:]
    data_baseline2 = data[channel_number, y:]
    
    return data_baseline1, data_baseline2, brain_state_1, brain_state_2


def load_analysis_files_onebrainstate(path, animal_number, starting_times_dict, channel_number):

    starting_1 = animal_number + '_1'

    files = []

    for r, d, f in os.walk(path):
        for file in f:
            if animal_number in file:
                files.append(os.path.join(r, file))

    for f in files:
        print(f)

    for x in files:
        if x.endswith('npy'):
            data = np.load(x)

    for y in files:
        if y.endswith('_1' + animal_number + '.pkl'):
            global brain_state_1
            brain_state_1 = pd.read_pickle(y)

    for animal_id in starting_times_dict:
        if animal_id == starting_1:
            global time_1
            time_1 = starting_times_dict[animal_id]

    x = time_1[0]

    global data_baseline1
    data_baseline1 = data[channel_number, x:]

    return data_baseline1, brain_state_1, time_1


#the function below slices out indices from data file that correspond to brainstates


def brainstate_times(brain_state_file, brainstate_number):
    
    #brainstate_number can be 0 - (wake), 1 - (nonREM) or 2 - REM
    
    #functions required for automated script
    #5 second bin definition
    x = int(250.4*5)
    f1 = lambda a,b: list(range(a,b,x))


    query = brain_state_file.iloc[:,0] == brainstate_number #REM is 2
        
        
    #find index values in brain state file that correspond to the wake state
    brain_state_indices = brain_state_file[query]
    all_indices = brain_state_indices.index
        
    #now find where these indices jump to separate into epochs
    epoch_indices = []
    starting_index = all_indices[0]
        
    for i in range(len(all_indices)-1):
        if all_indices[i] + 1 != all_indices[i+1]:
            epoch_indices.append([starting_index, all_indices[i]])
            starting_index = all_indices[i+1]
                
    #need to append the last value outside of the loop as loop is for len -1
    epoch_indices.append([starting_index, all_indices[-1]])
    
    #now go back to brain states file and slice out start and end time values using the indices 
    time_start_values = []
    time_end_values = []

    for i in range(len(epoch_indices)):
        time_start_values.append(brain_state_file.iloc[epoch_indices[i][0],1])
    

    for i in range(len(epoch_indices)):
        time_end_values.append(brain_state_file.iloc[epoch_indices[i][1],2])
        
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

'this function filters out low-frequency drifts and frequencies above 50Hz'
def highpass(raw_data):
    lowcut = 1
    highcut = 50
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
    
    for i in range(len(timevalues_array)):
        a = timevalues_array[i]
        k = timevalues_array[i] + 1252
        extracted_datavalues.append(data_file[a:k])

    return extracted_datavalues



'this function removes epochs with data values that exceed 4000'

def remove_noise(extracted_datavalues):

    artifacts_removed = []
    
    channel_threshold = []

    for i in range(len(extracted_datavalues)):
        for j in range(len(extracted_datavalues[i])):
            if extracted_datavalues[i][j] >= 3000:
                channel_threshold.append(i)
            else:
                pass
                
    removing_duplicates =[]
    for i in range(len(channel_threshold)):
        j = i + 1
        if i == j:
            del[i]
        else:
            removing_duplicates.append(channel_threshold[i])

    global channels_withoutnoise
    channels_withoutnoise = [i for j, i in enumerate(extracted_datavalues) if j not in removing_duplicates]

    return channels_withoutnoise


'this function calculates psd via Welch method on data with noise artifacts removed'

def psd_per_channel(data_without_noise):
    
    global psd
    global frequency
    psd = []
    welch_channel = []
    #save one array of frequency values for plotting 
    frequency = []

    for i in range(len(data_without_noise)):
        welch_channel.append(scipy.signal.welch(data_without_noise[i], fs=250.4, window='hann', nperseg=1252))
    

    #separate psd values from frequency values
    for i in range(len(welch_channel)):
        psd.append(welch_channel[i][1])
    
    
    frequency = welch_channel[0][0]
        
    
    return psd, frequency

'function below calculates line of best fit for psd of each epoch and returns the average slope intercept and gradient'
def look_for_outliers(psd, frequency):

    global slope_list
    global intercept_list
    slope_list = []
    intercept_list = []

    for i in psd:
        plt.semilogy(frequency, i)
        slope, intercept = np.polyfit(frequency, i, 1)
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

    for i in range(len(psd)):
        plt.semilogy(frequency, psd[i])
        slope, intercept = np.polyfit(frequency, psd[i], 1)
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


