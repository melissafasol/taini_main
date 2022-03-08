'''this file applies functions in psd_taini_mainfunctions.py to all datasets'''

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import load_analysis_files, brainstate_times_REM_wake, brain_state_times_nonREM, timevalues_array_nonREM, highpass
from psd_taini_mainfunctions import channel_data_extraction, load_analysis_files_onebrainstate, look_for_outliers, remove_epochs, plot_lin_reg, remove_noise, psd_per_channel, psd_average
from constants import start_times_baseline, channels_dict, genotype_per_animal

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

animal_number_two_brainstates = ['S7063', 'S7064', 'S7069', 'S7071', 'S7086', 'S7091', 'S7092'] #'S7070'
animal_number_one_brainstate = ['S7068', 'S7074', 'S7075', 'S7076','S7088', 'S7094', 'S7098', 'S7068', 'S7101'] #S7072 #S7096 #S7087
seizure_two_brainstates = ['S7063', 'S7064', 'S7069', 'S7072']
seizure_one_brainstate = ['S7074', 'S7075', 'S7088', 'S7092', 'S7094']

channel_numbers = [4,7,10,11]
brain_state_number = 1

'all empty lists below'
small_dfs_two_brainstates = []
small_dfs_one_brainstate = []
slopegradient_intercept_2_brainstate = []
slopegradient_intercept_1_brainstate = []
frequency_values = numpy.arange(0, 125.2, 0.2)
frequency_df = pd.DataFrame({'Frequency': frequency_values})
small_dfs_two_brainstates.append(frequency_df)
small_dfs_one_brainstate.append(frequency_df)

'''
'loop below calculates psd average per channel for every number in two_brainstates list'
for animal in animal_number_two_brainstates:
    for channel in channel_numbers:
        data_baseline1, data_baseline2, brain_state_1, brain_state_2 = load_analysis_files(path, animal, start_times_baseline, channel)
        if brain_state_number == 1:
            time_start_values_1, time_end_values_1 = brain_state_times_nonREM(brain_state_1, brain_state_number)
            time_start_values_2, time_end_values_2 = brain_state_times_nonREM(brain_state_2, brain_state_number)
            timevalues_1 = timevalues_array_nonREM(time_start_values_1, time_end_values_1)
            timevalues_2 = timevalues_array_nonREM(time_start_values_2, time_end_values_2)

        else:
            timevalues_1 = brainstate_times_REM_wake(brain_state_1, brain_state_number)
            timevalues_2 = brainstate_times_REM_wake(brain_state_2, brain_state_number)
        filtered_1 = highpass(data_baseline1)
        filtered_2 = highpass(data_baseline2)
        datavalues_1 = channel_data_extraction(timevalues_1, filtered_1)
        datavalues_2 = channel_data_extraction(timevalues_2, filtered_2)
        withoutartifacts_1 = remove_noise(datavalues_1)
        withoutartifacts_2 = remove_noise(datavalues_2)
        no_artifacts_array_1 = withoutartifacts_1[0]
        no_artifacts_array_2 = withoutartifacts_2[0]
        welch_array_1, psd_1, frequency = psd_per_channel(no_artifacts_array_1)
        welch_array_2, psd_2, frequency = psd_per_channel(no_artifacts_array_2)
        intercept_epochs_remove, slope_epochs_remove = look_for_outliers( psd_1, frequency)
        ##slopegradient_intercept.append([animal_number, intercept_slope])
        intercept_epochs_remove_2, slope_epochs_remove_2 = look_for_outliers(psd_2, frequency)
        ##slopegradient_intercept.append([animal_number, intercept_slope_2])
        psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd_1)
        psd_cleaned_2 = remove_epochs(intercept_epochs_remove_2, slope_epochs_remove_2, psd_2)
        slope_epochs_1, intercept_epochs_1 = plot_lin_reg(psd_cleaned_1, frequency)
        slope_epochs_2, intercept_epochs_2 = plot_lin_reg(psd_cleaned_2, frequency)
        data_1 = pd.DataFrame({str(animal) + '_chan_' + str(channel) + '_slope_'+ str(brain_state_number): slope_epochs_1, 
        str(animal) + '_' + str(channel) + 'intercept' + str(brain_state_number): intercept_epochs_1})
        data_2 = pd.DataFrame({str(animal) + '_chan_' + str(channel) + '_slope_'+ str(brain_state_number): slope_epochs_2, 
        str(animal) + '_' + str(channel) + 'intercept' + str(brain_state_number): intercept_epochs_2})
        psd_average_1 = psd_average(psd_cleaned_1, frequency, animal)
        list_mean_1 = list(psd_average_1)
        psd_average_2 = psd_average(psd_cleaned_2, frequency, animal)
        list_mean_2 = list(psd_average_2)

        results = { 'Power_1': list_mean_1, 'Power_2': list_mean_2}
        df_1 = pd.DataFrame(data = results)
        col = df_1.loc[:, "Power_1":"Power_2"]
        df_1[animal] = col.mean(axis = 1)
        average_p = df_1.loc[:, animal]
        power_dataframe = pd.DataFrame({animal + '_chan_' + str(channel): average_p})
    
        ##fig = plt.figure()
        ##plt.semilogy(frequency, average_p)
        ##plt.xlabel('frequency [Hz]')
        ##plt.xlim(1,100)
        ##plt.ylim(10**-3, 10**4)
        ##plt.ylabel('Power spectrum')
        ##fig.suptitle(animal_number)
        ##fig.savefig(animal_number + 'average')
        ##plt.show()
        #small_dfs_two_brainstates.append(power_dataframe)
        #slopegradient_intercept_2_brainstate.append(data_1)
        #slopegradient_intercept_2_brainstate.append(data_2)
'''

os.chdir('/home/melissa/Results/')

#merged_two_brainstates = pd.concat(small_dfs_two_brainstates, axis=1)
#merged_gradient_intercept = pd.concat(slopegradient_intercept_2_brainstate, axis=1)

#merged_two_brainstates.to_csv('baseline_nonREM_epoch_test_2npyfiles.csv', index = True)
#merged_gradient_intercept.to_csv('baseline_slopeintercept_2_brainstate.csv', index=True)

os.chdir('/home/melissa/preprocessing/numpyformat_baseline')
for animal in animal_number_one_brainstate:
    for channel in channel_numbers:
        data_baseline1, brain_state_1 = load_analysis_files_onebrainstate(path, animal, start_times_baseline, channel)
        if brain_state_number == 1:
            time_start_values, time_end_values = brain_state_times_nonREM(brain_state_1, brain_state_number)
            timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
        else:
            timevalues = brainstate_times_REM_wake(brain_state_1, brain_state_number)
        filtered = highpass(data_baseline1)
        datavalues = channel_data_extraction(timevalues, filtered)
        withoutartifacts, removing_duplicates = remove_noise(datavalues)
        #withoutartifacts = withoutartifacts[0]
        welch_channel, psd, frequency = psd_per_channel(withoutartifacts)
        power_list = [power_array[1] for power_array in welch_channel]
        intercept_epochs_remove, slope_epochs_remove = look_for_outliers(power_list, frequency)
        #slopegradient_intercept.append([animal_number, intercept_slope])
        psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, power_list)
        slope_epochs, intercept_epochs = plot_lin_reg(psd_cleaned_1, frequency)
        psd_average_1 = psd_average(psd_cleaned_1, frequency, animal)
        list_average_1 = list(psd_average_1)
    
        results = pd.DataFrame(data = {animal + '_chan_' + str(channel):list_average_1})
        data = pd.DataFrame({str(animal) + '_chan_' + str(channel) + '_slope_'+ str(brain_state_number): slope_epochs, 
        str(animal) + '_' + str(channel) + 'intercept' + str(brain_state_number): intercept_epochs})
        small_dfs_one_brainstate.append(results)
        slopegradient_intercept_1_brainstate.append(data)


os.chdir('/home/melissa/all_taini_melissa/')
merged_one_brainstate = pd.concat(small_dfs_one_brainstate, axis=1)
merged_gradient_1= pd.concat(slopegradient_intercept_1_brainstate, axis=1)

os.chdir('/home/melissa/Results')
merged_one_brainstate.to_csv('baseline_nonREM_epoch_test_1npyfile.csv', index=True)
merged_gradient_1.to_csv('baseline_slopeintercept_1_brainstate.csv', index=True)
