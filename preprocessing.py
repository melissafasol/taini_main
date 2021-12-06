#convert .dat files to numpy files and reformat brain states

from datetime import date
import os 
import mne 
import numpy as np 
import pandas as pd

#1. function to save .dat files as numpy files 

#path to file with .dat file and other required variables 
os.chdir('/home/melissa/S7094')
og_fn = 'TAINI_1048_S7094-B-2021_06_15-0000.dat'
save_as = 'TAINI_S7094_BASELINE.npy'


def dat_to_numpy(fn, saveas):
    number_of_channels = 16
    sample_rate = 250.4
    display_decimation = 1

    #reshape the 2D per channel data 
    dt = 'int16'
    data_raw = np.fromfile(fn, dtype=dt)
    step = number_of_channels*display_decimation
    dat_chans = [data_raw[c::step] for c in range(number_of_channels)]
    data = np.array(dat_chans)
    os.chdir('/home/melissa/preprocessing/numpyformat')
    np.save(saveas, data)

    return 


#dat_to_numpy(og_fn, save_as)


#2. Reformat brain states


def reformat_brainstates(path):
    #brain_1 = animal_number + '_BL1'
    #brain_2 = animal_number + '_BL2'

    animal_numbers_reformat_brainstates = ['63', '64', '68', '69', '70', '71', '72',
                                        '74', '75', '76', '83', '86', '88', '91',
                                        '92', '94', '96', '98', '101']

    files = []

    for r, d, f in os.walk(path):
        for file in f:
            for animal_number in animal_numbers_reformat_brainstates:
                if animal_number in file:
                    files.append(os.path.join(r, file))

    for f in files:
        print(f)

    for y in files:
        if y.endswith('States-real samp.xls'):
            load_file = pd.read_excel(y)
            print(load_file)
            #load_file.columns = (['brainstate', 'old_start_epoch', 'old_end_epoch']) #rename columns
            #load_file.shift(1, axis = 0) #shift rows down by one
            #load_file.loc[0] = [0, 0, 5] #add new time bin for row one
            #load_file.astype(int) #convert float vlaues to integers
            #load_file.drop(["old_start_epoch", "old_end_epoch"], axis=1, inplace=True) #delete columns
            #x = len(load_file)*5
            #z = x + 5
            #load_file.insert(loc =1, column = 'start_epoch', value=list(range(0, x, 5)))
            #load_file.insert(loc=2, column = 'end_epoch', value=list(range(5,z,5)))
            
            os.chdir('/home/melissa/brain_states')
            #load_file.to_pickle(y)

    return y

os.chdir('/home/melissa/brain_states_unformatted')
path = '/home/melissa/brain_states_unformatted'
reformat_brainstates(path)