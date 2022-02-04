'''this file applies functions in psd_taini_mainfunctions.py to all datasets'''

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import loading_analysis_files, brainstate_times, highpass
from psd_taini_mainfunctions import channel_data_extraction, loading_analysis_files_onebrainstate, looking_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average
from psd_taini_mainfunctions import starting_times_dict_baseline, channels_dict, genotype_per_animal

from S7096 import start_times_S7096, concatenate_S7096

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

path = '/home/melissa/preprocessing/numpyformat_baseline'

animal_number_two_brainstates = [ 'S7063', 'S7064', 'S7069', 'S7070', 'S7071', 'S7086', 'S7091', 'S7092']
animal_number_one_brainstate = [ 'S7068', 'S7072', 'S7074', 'S7075', 'S7076', 'S7087','S7088', 'S7094', 'S7098', 'S7068', 'S7101']
seizure_two_brainstates = ['S7063', 'S7064', 'S7069', 'S7072']
seizure_one_brainstate = ['S7074', 'S7075', 'S7088', 'S7092', 'S7094']

channel_number = [4]
brain_state_number = 4

'all empty lists below'
small_dfs_two_brainstates = []
small_dfs_one_brainstate = []
slopegradient_intercept =[]
frequency_values = numpy.arange(0, 125.2, 0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})
small_dfs_two_brainstates.append(frequency_df)
small_dfs_one_brainstate.append(frequency_df)

'loop below calculates psd average per channel for every number in two_brainstates list'
for i in range(len(seizure_two_brainstates)-1):
    animal_number = animal_number_two_brainstates[i]
    print(animal_number)
    for i in range(len(channel_number)):
        data_baseline1, data_baseline2, brain_state_1, brain_state_2 = loading_analysis_files(path, animal_number, starting_times_dict_baseline, channel_number[i])
        timevalues_1 = brainstate_times(brain_state_1, brain_state_number)
        timevalues_2 = brainstate_times(brain_state_2, brain_state_number)
        filtered_1 = highpass(data_baseline1)
        filtered_2 = highpass(data_baseline2)
        datavalues_1 = channel_data_extraction(timevalues_1, filtered_1)
        datavalues_2 = channel_data_extraction(timevalues_2, filtered_2)
        withoutartifacts_1 = remove_noise(datavalues_1)
        withoutartifacts_2 = remove_noise(datavalues_2)
        psd_1, frequency = psd_per_channel(withoutartifacts_1)
        psd_2, frequency = psd_per_channel(withoutartifacts_2)
        intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd_1, frequency)
        #slopegradient_intercept.append([animal_number, intercept_slope])
        intercept_epochs_remove_2, slope_epochs_remove_2 = looking_for_outliers(psd_2, frequency)
        #slopegradient_intercept.append([animal_number, intercept_slope_2])
        psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd_1)
        psd_cleaned_2 = remove_epochs(intercept_epochs_remove_2, slope_epochs_remove_2, psd_2)
        psd_average_1 = psd_average(psd_cleaned_1, frequency, animal_number)
        list_mean_1 = list(psd_average_1)
        psd_average_2 = psd_average(psd_cleaned_2, frequency, animal_number)
        list_mean_2 = list(psd_average_2)
    
     
        for x in genotype_per_animal:
            if x == animal_number:
                genotype = genotype_per_animal[x]
    
        results = { 'Power_1': list_mean_1, 'Power_2': list_mean_2}
        df_1 = pd.DataFrame(data = results)
        col = df_1.loc[:, "Power_1":"Power_2"]
        df_1[animal_number] = col.mean(axis = 1)
        average_p = df_1.loc[:, animal_number]
        df_1.drop(["Power_1", "Power_2"], axis = 1, inplace=True)
        #fig = plt.figure()
        #plt.semilogy(frequency, average_p)
        #plt.xlabel('frequency [Hz]')
        #plt.xlim(1,100)
        #plt.ylim(10**-3, 10**4)
        #plt.ylabel('Power spectrum')
        #fig.suptitle(animal_number)
        os.chdir('/home/melissa/psd_plots_december21')
        #fig.savefig(animal_number + 'average')
        #plt.show()
        small_dfs_two_brainstates.append(df_1)
    animal_number = [i+1]
    

#last animal not included in loop
animal_number = seizure_two_brainstates[-1]
for i in range(len(channel_number)):
    data_baseline1, data_baseline2, brain_state_1, brain_state_2 = loading_analysis_files(path, animal_number, starting_times_dict_baseline, channel_number[i])
    timevalues_1 = brainstate_times(brain_state_1, brain_state_number)
    timevalues_2 = brainstate_times(brain_state_2, brain_state_number)
    filtered_1 = highpass(data_baseline1)
    filtered_2 = highpass(data_baseline2)
    datavalues_1 = channel_data_extraction(timevalues_1, filtered_1)
    datavalues_2 = channel_data_extraction(timevalues_2, filtered_2)
    withoutartifacts_1 = remove_noise(datavalues_1)
    withoutartifacts_2 = remove_noise(datavalues_2)
    psd_1, frequency = psd_per_channel(withoutartifacts_1)
    psd_2, frequency = psd_per_channel(withoutartifacts_2)
    intercept_epochs_remove, slope_epochs_remove = looking_for_outliers(psd_1, frequency)
    #slopegradient_intercept.append([animal_number, intercept_slope])
    intercept_epochs_remove_2, slope_epochs_remove_2 = looking_for_outliers(psd_2, frequency)
    #slopegradient_intercept.append([animal_number, intercept_slope_2])
    psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd_1)
    psd_cleaned_2 = remove_epochs(intercept_epochs_remove_2, slope_epochs_remove_2, psd_2)
    psd_average_1 = psd_average(psd_cleaned_1, frequency, animal_number)
    list_mean_1 = list(psd_average_1)
    psd_average_2 = psd_average(psd_cleaned_2, frequency, animal_number)
    list_mean_2 = list(psd_average_2)


    results = { 'Power_1': list_mean_1, 'Power_2': list_mean_2}
    df_lastvalue = pd.DataFrame(data = results)
    col = df_lastvalue.loc[:, "Power_1":"Power_2"]
    df_lastvalue[animal_number] = col.mean(axis = 1)
    average_p = df_lastvalue.loc[:, animal_number]
    df_lastvalue.drop(["Power_1", "Power_2"], axis = 1, inplace=True)
    
    #fig = plt.figure()
    #plt.semilogy(frequency, average_p)
    #plt.xlabel('frequency [Hz]')
    #plt.xlim(0,100)
    #plt.ylim(10**-3, 10**4)
    #plt.ylabel('Power spectrum')
    #fig.suptitle(animal_number)
    os.chdir('/home/melissa/psd_plots_december21')
    #fig.savefig(animal_number + 'average')
    #plt.show()
    small_dfs_two_brainstates.append(df_lastvalue)


os.chdir('/home/melissa/Results/')

merged_two_brainstates = pd.concat(small_dfs_two_brainstates, axis=1)
merged_two_brainstates.to_csv('baseline_2_brainstates_test.csv', index = True)


for i in range(len(seizure_one_brainstate)-1):
    animal_number = animal_number_one_brainstate[i]
    for i in range(len(channel_number)):
        data_baseline1, brain_state_1, time_1 = loading_analysis_files_onebrainstate(path, animal_number, starting_times_dict_baseline, channel_number[i])
        timevalues = brainstate_times(brain_state_1, brain_state_number)
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

        results = pd.DataFrame(data = {animal_number:list_average_1})
        small_dfs_one_brainstate.append(results)    
    animal_number = [i+1]


animal_number = seizure_one_brainstate[-1]
print(animal_number)
for i in range(len(channel_number)):
    data_baseline1, brain_state_1, time_1 = loading_analysis_files_onebrainstate(path, animal_number, starting_times_dict_baseline, channel_number[i])
    timevalues = brainstate_times(brain_state_1, brain_state_number)
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

    results = pd.DataFrame(data={animal_number:list_average_1})
    small_dfs_one_brainstate.append(results)


os.chdir('/home/melissa/all_taini_melissa/')

merged_one_brainstate = pd.concat(small_dfs_one_brainstate, axis=1)
os.chdir('/home/melissa/Results')
merged_one_brainstate.to_csv('baseline_1_brainstate.csv', index=True)
