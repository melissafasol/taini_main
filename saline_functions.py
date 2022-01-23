import pandas as pd
import os 
import numpy as np 
import mne
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy 
from scipy import signal 
import re

start_saline_dict = {'S7063_1': [37094257], 'S7063_2': [58728816], 
                       'S7064_1': [15324481], 'S7064_2':[36959040],
                       'S7068_1': [37034161], 'S7068_2':[58668720],
                       'S7069_1': [37034161], 'S7069_2':[58668720],
                       'S7070_1A': [38055001], 'S7070_2A':[42442008],
                       'S7070_1B':[1], 'S7070_2B':[17247552],
                       'S7071_1A': [38055001], 'S7071_2A':[42442008],
                       'S7071_1B':[1], 'S7071_2B':[17247552],
                       'S7072_1': [59750449], 'S7072_2': [81385008],
                       'S7074_1A': [56248286], 'S7074_2A':[63655117],
                       'S7074_1B':[1], 'S7074_2B':[14227728],
                       'S7075_1A': [56248286], 'S7075_2A':[63655117],
                       'S7075_1B':[1], 'S7075_2B':[14227728],
                       'S7076_1': [18284209], 'S7076_2': [39918768],
                       'S7083_1': [60847201], 'S7083_2':[82481760],
                       'S7086_1': [18103921], 'S7086_2': [39738480],
                       'S7087_1': [19200673], 'S7087_2': [40835232],
                       'S7088_1': [19200673], 'S7088_2': [40835232], 
                       'S7091_1': [58638673], 'S7091_2': [80273232],
                       'S7092_1': [58638673], 'S7092_2':[80273232],
                       'S7094_1': [12830497], 'S7094_2': [34465056],
                       'S7096_1': [12840397], 'S7096_2': [34465056],
                       'S7098_1': [13611745], 'S7098_2':[35246304],
                       'S7101_1': [13611745], 'S7101_2':[35246304]}


def concatenate_saline_data(path, channel_number, animal_number, start_saline_dict):

    start_1A = animal_number + '_1A'
    end_1A = animal_number + '_2A'
    start_1B = animal_number + '_1B'
    end_1B = animal_number + '_2B'

    files = []

    for r, d, f in os.walk(path):
        for file in f:
            if animal_number in file:
                files.append(os.path.join(r, file))
    
    print(files)

    for recording in files:
        if recording.endswith('saline_1A.npy'):
            numpy_A = np.load(recording)
        if recording.endswith('saline_1B.npy'):
            numpy_B = np.load(recording)
    
    for animal_id in start_saline_dict:
        if animal_id == start_1A:
            start_1 = start_saline_dict[animal_id]
        elif animal_id == end_1A:
            end_1 = start_saline_dict[animal_id]
        elif animal_id == start_1B:
            start_2 = start_saline_dict[animal_id]
        elif animal_id == end_1B:
            end_2 = start_saline_dict[animal_id]
    
    start_1 = start_1[0]
    end_1 = end_1[0]
    start_2 = start_2[0]
    end_2 = end_2[0]

    start_1 = int(start_1)
    end_1 = int(end_1)
    start_2 = int(start_2)
    end_2 = int(end_2)

#extract rows corresponding to channel number and parse out data between start and end times
    recording_1 = numpy_A[channel_number, start_1:end_1]
    recording_2 = numpy_A[channel_number, start_2:end_2]
    
    #concatenate recording 1 and 2 into one dataset

    concatenate_dataset = np.concatenate((recording_1, recording_2))

    for brain_state_file in files:
        if brain_state_file.endswith('.pkl'):
            brain_state = pd.read_pickle(brain_state_file)

    return concatenate_dataset, brain_state


def one_numpy_saline(path, channel_number, animal_number, start_saline_dict):

    start_1A = animal_number + '_1'
    end_1A = animal_number + '_2'

    files = []

    for r,d,f in os.walk(path):
        for file in f:
            if animal_number in file:
                files.append(os.path.join(r, file))
    
    print(files)

    for recording in files:
        if recording.endswith('npy'):
            data = np.load(recording)

    for animal_id in start_saline_dict:
        if animal_id == start_1A:
            start_1 = start_saline_dict[animal_id]
        elif animal_id == end_1A:
            end_1 = start_saline_dict[animal_id]

    start_1 = start_1[0]
    end_1 = end_1[0]
    start_1 = int(start_1)
    end_1 = int(end_1)

    recording_one_numpy = data[channel_number, start_1:end_1]

    for brain_state_file in files:
        if brain_state_file.endswith('.pkl'):
            brain_state = pd.read_pickle(brain_state_file)

    return recording_one_numpy, brain_state