
'''this file applies functions in psd_taini_mainfunctions.py to all datasets'''

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import loading_analysis_files, brainstate_times, highpass
from psd_taini_mainfunctions import channel_data_extraction, loading_analysis_files_onebrainstate, looking_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average
from psd_taini_mainfunctions import starting_times_dict, channels_dict, genotype_per_animal

#other required imports 
import pandas as pd 
import os
import numpy 
import mne 
import matplotlib.pyplot as plt
import scipy
from scipy.fft import fft, fftfreq
from scipy import signal
import re
import statistics
from pandas import ExcelWriter

path = '/home/melissa/preprocessing/numpyformat'

animal_number_two_brainstates = [ 'S7063', 'S7064', 'S7069', 'S7070', 'S7071', 'S7083', 'S7086', 'S7091', 'S7092'] #S7101
animal_number_one_brainstate = ['S7068', 'S7072', 'S7074', 'S7075', 'S7076', 'S7088', 'S7094', 'S7098']
channel_number = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

small_dfs_one_brainstate = []

for i in range(len(animal_number_one_brainstate)-1):
    animal_number = animal_number_one_brainstate[i]
    for i in range(len(channel_number)):
        data_baseline1, brain_state_1, time_1 = loading_analysis_files_onebrainstate(path, animal_number, starting_times_dict, channel_number)
        timevalues = brainstate_times(brain_state_1, 2)
        filtered = highpass(data_baseline1)
        datavalues = channel_data_extraction(timevalues, filtered)
        withoutartifacts = remove_noise(datavalues)
        psd, frequency = psd_per_channel(withoutartifacts)
        intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd, frequency)
        #slopegradient_intercept.append([animal_number, intercept_slope])
        psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
        psd_average_1 = psd_average(psd_cleaned_1, frequency, animal_number)
        list_average_1 = list(psd_average_1)
    
        for x in genotype_per_animal:
            if x == animal_number:
                genotype = genotype_per_animal[x]
        print(genotype)

        sleepstate = ['REM']
        recordingtype = ['baseline']
        results = {'Animal_Number':[animal_number]*627, 'Channel_Number': channel_number[i]*627,
        'Genotype':genotype*627, 'Sleep_State' : sleepstate*627, 'Recording_Type': recordingtype*627,
        'Frequency': frequency, 'Power': list_average_1}

        df_2 = pd.DataFrame(data = results)
        small_dfs_one_brainstate.append(df_2)    
    animal_number = [i+1]


animal_number = animal_number_one_brainstate[-1]
print(animal_number)
for i in range(len(channel_number)):
    data_baseline1, brain_state_1, time_1 = loading_analysis_files_onebrainstate(path, animal_number, starting_times_dict, channel_number[i])
    timevalues = brainstate_times(brain_state_1, 2)
    filtered = highpass(data_baseline1)
    datavalues = channel_data_extraction(timevalues, filtered)
    withoutartifacts = remove_noise(datavalues)
    psd_1, frequency = psd_per_channel(withoutartifacts)
    intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd_1, frequency)
    #slopegradient_intercept.append([animal_number, intercept_slope])
    psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd_1)
    psd_average_1 = psd_average(psd_cleaned_1, frequency, animal_number)
    list_average_1 = list(psd_average_1)

    for x in genotype_per_animal:
        if x == animal_number:
            genotype = genotype_per_animal[x]
    print(genotype)

    sleepstate = ['REM']
    recordingtype = ['baseline'] 
    results = {'Animal_Number':[animal_number]*627, 'Channel_Number' : channel_number[i]*627,
     'Genotype':genotype*627, 'Sleep_State' : sleepstate*627, 'Recording_Type': recordingtype*627,
    'Frequency': frequency, 'Power': list_average_1}

    df_lastvalue = pd.DataFrame(data = results)
    small_dfs_one_brainstate.append(df_lastvalue)


'''checking last df is the last animal in list'''
print(len(small_dfs_one_brainstate))


data_1 = pd.DataFrame(small_dfs_one_brainstate)
data_1.head()

os.chdir('/home/melissa/all_taini_melissa/')
data_1.to_pickle('one_brainstate_REM.pkl')


