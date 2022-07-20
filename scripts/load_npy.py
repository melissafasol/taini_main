import numpy as np 
import pandas as pd
import os 
import mne 
import glob 
from GRIN2B_constants import animal_ID_list

#path to .dat file 
#path to montage 

#load brainstate file 
#delete first column and add 0-5

##variables that change every recording
filename = 'example.dat'
animal_id = 'S7087'
baseline = 2
first_sample = 100000 #sample start time 
sampling_rate = 250.4

#variables that change but not often 
path_to_folder = '/home/melissa/preprocessing/GRIN2B/GRIN2B_dat'
downsampling = 1
montage_name = '/home/melissa/taini_main/scripts/standard_16grid_taini1.elc'
number_electrodes = 16
path_to_save_folder = '/home/melissa/preprocessing/GRIN2B/GRIN2B_numpy'
save_as_name = 'change to file name to save as'

'''load a .dat file by interpreting it as int16 and then de-interlacing the 16 channels'''
def parse_dat(filename, number_of_channels, sample_rate):
    sample_datatype = 'int16'
    display_decimation = 1

    #load the raw (1-D) data
    dat_raw = np.fromfile(filename, dtype = sample_datatype)

    #reshape the (2-D) per channel data
    step = number_of_channels * display_decimation
    dat_chans = [dat_raw[c::step] for c in range(number_of_channels)]

    #build the time array 
    t = np.arange(len(dat_chans[0]), dtype = float) / sample_rate

    return dat_chans, t

def convert_dat_to_npy(filename, path_to_folder, path_to_save_folder, sample_rate, number_electrodes, save_as_name):

    os.chdir(path_to_folder)
    dat_chans, t = parse_dat(filename, number_electrodes, sample_rate)
    data_to_save = np.array(dat_chans)
    
    os.chdir(path_to_save_folder)
    np.save(save_as_name, data_to_save)

    print('data saved for ' + save_as_name)


#test_file_name = 'TAINI_1045_D_Grin2B_402-2022_05_03-0000.dat'
#convert_dat_to_npy(filename = test_file_name, path_to_folder = path_to_folder, path_to_save_folder = path_to_save_folder, sample_rate=1000, #number_electrodes= 16, save_as_name='test_1045_GRIN2B')



for animal in animal_ID_list:
    dat_recording = [GRIN2B_file for GRIN2B_file  in os.listdir(path_to_folder) if GRIN2B_file.endswith(animal + '_baseline.dat')]
    print(dat_recording[0])
    convert_dat_to_npy(filename = dat_recording[0], path_to_folder= path_to_folder, path_to_save_folder=path_to_save_folder, sample_rate=1000,
    number_electrodes=16, save_as_name = animal + '_GRIN2B')

