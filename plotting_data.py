import matplotlib
import matplotlib.pyplot as plt
from preprocessing import plot_all_channels
import os 
import mne 
import numpy as np
import matplotlib
import pandas as pd

#required variables
path =  '/home/melissa/preprocessing/numpyformat'
sample_rate = 250.4

os.chdir(path)
file = np.load('TAINI_S7072_BASELINE.npy')

os.chdir('/home/melissa//Documents/EEG_Coherence-master/EEG_Coherence-master/')
montage_name = 'standard_16grid_taini1.elc'
montage = mne.channels.read_custom_montage(montage_name)
    
channel_types = ['eeg', 'eeg', 'eeg', 'eeg','eeg', 'eeg', 'eeg', 'eeg',
                    'eeg', 'eeg', 'eeg', 'eeg','eeg', 'eeg', 'emg', 'emg']

ch_names_1 = ['S1Tr_RIGHT', 'M2_FrA_RIGHT', 'M2_ant_RIGHT', 'M1_ant_RIGHT', 
                'V2ML_RIGHT', 'V1M_RIGHT', 'S1HL_S1FL_RIGHT', 'V1M_LEFT', 
                'V2ML_LEFT','S1HL_S1FL_LEFT', 'M1_ant_LEFT', 'M2_ant_LEFT',
                'M2_FrA_LEFT', 'S1Tr_LEFT', 'EMG_RIGHT', 'EMG_LEFT']
    
ch_numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

info = mne.create_info(ch_names = ch_names_1, sfreq = sample_rate, ch_types = channel_types)
 
custom_raw = mne.io.RawArray(file, info)


starting_time = 16481329.0/250.4
mne.viz.plot_raw(custom_raw, n_channels = 16, scalings = 'auto')