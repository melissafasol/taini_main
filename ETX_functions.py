from pickletools import read_unicodestringnl
import pandas as pd
import os 
import numpy as np 
import mne
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy 
from scipy import signal 
import re

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
    print(start_1)
    end_1 = int(end_1[0])
    print(end_1)
    start_2 = int(start_2[0])
    print(start_2)
    end_2 = int(end_2[0])
    print(end_2)

    #extract rows corresponding to channel number and parse out data between start and end times
    recording_1 = numpy_A[channel_number, start_1:end_1]
    print(recording_1[0])
    recording_2 = numpy_A[channel_number, start_2:end_2]
    print(recording_2[0])
    #concatenate recording 1 and 2 into one dataset

    concatenate_dataset = np.concatenate([recording_1[0], recording_2[0]])

    for brain_state_file in files:
        if brain_state_file.endswith('.pkl'):
            brain_state = pd.read_pickle(brain_state_file)

    return concatenate_dataset, brain_state


def one_numpy_ETX(path, channel_number, animal_number, start_ETX_time):

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

    for animal_id in start_ETX_time:
        if animal_id == start_1A:
            start_1 = start_ETX_time[animal_id]
        elif animal_id == end_1A:
            end_1 = start_ETX_time[animal_id]

    start_1 = start_1[0]
    end_1 = end_1[0]
    start_1 = int(start_1)
    end_1 = int(end_1)

    recording_one_numpy = data[channel_number, start_1:end_1]

    for brain_state_file in files:
        if brain_state_file.endswith('.pkl'):
            brain_state = pd.read_pickle(brain_state_file)

    return recording_one_numpy, brain_state

