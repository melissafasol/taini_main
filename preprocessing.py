#plot animals to look for strange artifacts

import os 
import mne 
import numpy as np 
from psd_taini_mainfunctions import starting_times_dict

path =  '/home/melissa/preprocessing/numpyformat'
animal_number = 'S7063'


def plot_all_channels(path, animal_number):
    
    files=[]

    for r, d, f in os.walk(path):
            for file in f:
                if animal_number in file:
                    files.append(os.path.join(r, file))

    print(files)

    for x in files:
        if x.endswith('npy'):
            data = np.load(x)
    
    global time
    for animal_id in starting_times_dict:
        starting_1 = animal_number + '_1'
        if animal_id == starting_1:
            time = starting_times_dict[animal_id]
    
    print(data)

    os.chdir('/home/melissa//Documents/EEG_Coherence-master/EEG_Coherence-master/')
    montage_name = 'standard_16grid_taini1.elc'
    montage = mne.channels.read_custom_montage(montage_name)
    sample_rate = 250.4
    channel_types = ['eeg', 'eeg', 'eeg', 'eeg','eeg', 'eeg', 'eeg', 'eeg',
                    'eeg', 'eeg', 'eeg', 'eeg','eeg', 'eeg', 'emg', 'emg']

    ch_names = ['S1Tr_RIGHT', 'M2_FrA_RIGHT', 'M2_ant_RIGHT', 'M1_ant_RIGHT', 
                'V2ML_RIGHT', 'V1M_RIGHT', 'S1HL_S1FL_RIGHT', 'V1M_LEFT', 
                'V2ML_LEFT','S1HL_S1FL_LEFT', 'M1_ant_LEFT', 'M2_ant_LEFT',
                'M2_FrA_LEFT', 'S1Tr_LEFT', 'EMG_RIGHT', 'EMG_LEFT']
    
    ch_numbers = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    info = mne.create_info(ch_names, sfreq = sample_rate, ch_types = channel_types)
 
    custom_raw = mne.io.RawArray(data, info)
    print(custom_raw)

    return custom_raw