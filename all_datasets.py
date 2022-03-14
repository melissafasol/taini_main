'''this file applies functions in psd_taini_mainfunctions.py to all datasets'''
import psd_taini_mainfunctions
import saline_functions
import ETX_functions
import constants
import save_functions

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
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average

#variables to change 
recording_condition = ['baseline', 'saline', 'ETX']
directory_name = '/home/melissa/Results'
channel_numbers = [4,7,10,11]
brain_state_number = [0,1,2]


for condition in recording_condition:
    print(condition)
    #empty lists
    small_dfs_two_brainstates = []
    small_dfs_one_brainstate = []
    slopegradient_intercept_2_brainstate = []
    slopegradient_intercept_1_brainstate = []
    frequency_values = numpy.arange(0, 125.2, 0.2)
    frequency_df = pd.DataFrame({'Frequency': frequency_values})
    small_dfs_two_brainstates.append(frequency_df)
    small_dfs_one_brainstate.append(frequency_df)
    
    if condition == 'baseline':
        for brain_state in brain_state_number:
            
            for animal in baseline_recording_dictionary['animal_two_brainstates']:
                for channel in channel_numbers:
                    data_baseline1, data_baseline2, brain_state_file_1, brain_state_file_2 = load_analysis_files(baseline_recording_dictionary['path'], animal, start_times_baseline, channel)
                    if brain_state == 1:
                        time_start_values_1, time_end_values_1 = brain_state_times_nonREM(brain_state_file_1, brain_state)
                        time_start_values_2, time_end_values_2 = brain_state_times_nonREM(brain_state_file_2, brain_state)
                        timevalues_1 = timevalues_array_nonREM(time_start_values_1, time_end_values_1)
                        timevalues_2 = timevalues_array_nonREM(time_start_values_2, time_end_values_2)

                    else:
                        timevalues_1 = brainstate_times_REM_wake(brain_state_file_1, brain_state)
                        timevalues_2 = brainstate_times_REM_wake(brain_state_file_2, brain_state)
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
                    intercept_epochs_remove_2, slope_epochs_remove_2 = look_for_outliers(psd_2, frequency)
                    psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd_1)
                    psd_cleaned_2 = remove_epochs(intercept_epochs_remove_2, slope_epochs_remove_2, psd_2)
                    slope_epochs_1, intercept_epochs_1 = plot_lin_reg(psd_cleaned_1, frequency)
                    slope_epochs_2, intercept_epochs_2 = plot_lin_reg(psd_cleaned_2, frequency)
                    data_1 = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs_1, 
                    str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs_1})
                    data_2 = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs_2, 
                    str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs_2})
                    slopegradient_intercept_2_brainstate.append(data_1)
                    slopegradient_intercept_2_brainstate.append(data_2)
                    psd_average_1 = psd_average(psd_cleaned_1, frequency, animal)
                    list_mean_1 = list(psd_average_1)
                    psd_average_2 = psd_average(psd_cleaned_2, frequency, animal)
                    list_mean_2 = list(psd_average_2)

                    results = { 'Power_1': list_mean_1, 'Power_2': list_mean_2}
                    df_1 = pd.DataFrame(data = results)
                    col = df_1.loc[:, "Power_1":"Power_2"]
                    df_1[animal] = col.mean(axis = 1)
                    average_p = df_1.loc[:, animal]
                    power_dataframe = pd.DataFrame( data = {str(brain_state) + animal + '_chan_' + str(channel):average_p})
                    small_dfs_two_brainstates.append(power_dataframe)

            for animal in baseline_recording_dictionary['animal_one_brainstate']:
                for channel in channel_numbers:
                    data_baseline1, brain_state_file = load_analysis_files_onebrainstate(baseline_recording_dictionary['path'], animal, start_times_baseline, channel)
                    if brain_state == 1:
                        time_start_values, time_end_values = brain_state_times_nonREM(brain_state_file, brain_state)
                        timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
                    else:
                        timevalues = brainstate_times_REM_wake(brain_state_file, brain_state)
                    filtered = highpass(data_baseline1)
                    datavalues = channel_data_extraction(timevalues, filtered)
                    withoutartifacts, removing_duplicates = remove_noise(datavalues)
                    #withoutartifacts = withoutartifacts[0]
                    welch_channel, psd, frequency = psd_per_channel(withoutartifacts)
                    power_list = [power_array[1] for power_array in welch_channel]
                    intercept_epochs_remove, slope_epochs_remove = look_for_outliers(power_list, frequency)
                    psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, power_list)
                    slope_epochs, intercept_epochs = plot_lin_reg(psd_cleaned_1, frequency)
                    psd_average_1 = psd_average(psd_cleaned_1, frequency, animal)
                    list_average_1 = list(psd_average_1) 
                    results = pd.DataFrame(data = {str(brain_state) + animal + '_chan_' + str(channel):list_average_1})
                    data = pd.DataFrame({str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs, 
                    str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs})
                    small_dfs_one_brainstate.append(results)
                    slopegradient_intercept_1_brainstate.append(data)

        merged_power_file, merged_gradient_file = concatenate_files(small_dfs_two_brainstates, slopegradient_intercept_2_brainstate)
        save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, condition)
        merged_power_file, merged_gradient_file = concatenate_files(small_dfs_one_brainstate, slopegradient_intercept_1_brainstate)
        save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, condition)

    if condition == 'saline':
        for brain_state in brain_state_number:
            for animal in saline_recording_dictionary['animal_two_numpy_files']:
                for channel in channel_numbers:
                    concatenate_data, brain_state_file = concatenate_saline_data(saline_recording_dictionary['path'], channel, animal, start_times_saline)
                    if brain_state == 1:
                        time_start_values, time_end_values = brain_state_times_nonREM(brain_state_file, brain_state)
                        timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
                    else:
                        timevalues = brainstate_times_REM_wake(brain_state_file, brain_state)
                    filtered_data = highpass(concatenate_data)
                    datavalues = channel_data_extraction(timevalues, filtered_data)
                    withoutartifacts, removing_duplicates = remove_noise(datavalues)
                    withoutartifacts = withoutartifacts[0]
                    welch_channel, psd, frequency = psd_per_channel(withoutartifacts)
                    power_list = [power_array[1] for power_array in welch_channel]
                    intercept_epochs_remove, slope_epochs_remove = look_for_outliers(power_list, frequency)
                    psd_cleaned_1 = remove_epochs(intercept_epochs_remove, slope_epochs_remove, power_list)
                    slope_epochs, intercept_epochs = plot_lin_reg(psd_cleaned_1, frequency)
                    psd_average_1 = psd_average(psd_cleaned_1, frequency, animal)
                    list_average_1 = list(psd_average_1) 
                    results = pd.DataFrame(data = {str(brain_state) + animal + '_chan_' + str(channel):list_average_1})
                    data = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs, 
                    str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs})
                    small_dfs_one_brainstate.append(results)
                    slopegradient_intercept_1_brainstate.append(data)
            
            for animal in saline_recording_dictionary['animal_one_numpy_file']:
                for channel in channel_numbers:
                    concatenate_data, brain_state_file = one_numpy_saline(saline_recording_dictionary['path'], channel, animal, start_times_saline)
                    if brain_state == 1:
                        time_start_values, time_end_values = brain_state_times_nonREM(brain_state_file, brain_state)
                        timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
                    else:
                        timevalues = brainstate_times_REM_wake(brain_state_file, brain_state)
                    filtered_data = highpass(concatenate_data)
                    datavalues = channel_data_extraction(timevalues, filtered_data)
                    without_artifacts = remove_noise(datavalues)
                    without_artifacts = without_artifacts[0]
                    welch_channel, psd, frequency = psd_per_channel(without_artifacts)
                    intercept_epochs_remove, slope_epochs_remove = look_for_outliers(psd, frequency)
                    psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
                    slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
                    psd_average_1 = psd_average(psd_clean, frequency, animal)
                    list_average_1 = list(psd_average_1) 
                    results = pd.DataFrame(data = {str(brain_state) + animal + '_chan_' + str(channel):list_average_1})
                    data = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs, 
                    str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs})
                    small_dfs_one_brainstate.append(results)
                    slopegradient_intercept_1_brainstate.append(data)

        merged_power_file, merged_gradient_file = concatenate_files(small_dfs_two_brainstates, slopegradient_intercept_2_brainstate)
        save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, recording_condition)
        merged_power_file, merged_gradient_file = concatenate_files(small_dfs_one_brainstate, slopegradient_intercept_1_brainstate)
        save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, condition)
    
    if condition == 'ETX':
        for brain_state in brain_state_number:
            for animal in ETX_recording_dictionary['animal_two_numpy_files']:
                for channel in channel_numbers:
                    concatenate_data, brain_state_file = concatenate_ETX_data(ETX_recording_dictionary['path'], channel, animal, start_times_ETX)
                    if brain_state == 1:
                        time_start_values, time_end_values = brain_state_times_nonREM(brain_state_file, brain_state)
                        timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
                    else:
                        timevalues = brainstate_times_REM_wake(brain_state_file, brain_state)
                        filtered_data = highpass(concatenate_data)
                    datavalues = channel_data_extraction(timevalues, filtered_data)
                    without_artifacts = remove_noise(datavalues)
                    without_artifacts = without_artifacts[0]
                    welch_channel, psd, frequency = psd_per_channel(without_artifacts)
                    intercept_epochs_remove, slope_epochs_remove = look_for_outliers(psd, frequency)
                    psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
                    slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
                    psd_average_1 = psd_average(psd_clean, frequency, animal)
                    list_average_1 = list(psd_average_1) 
                    results = pd.DataFrame(data = {str(brain_state) + animal + '_chan_' + str(channel):list_average_1})
                    data = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs, 
                    str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs})
                    small_dfs_one_brainstate.append(results)
                    slopegradient_intercept_1_brainstate.append(data)

            for animal in ETX_recording_dictionary['animal_one_numpy_file']:
                for channel in channel_numbers:
                    oncatenate_data, brain_state_file = one_numpy_ETX(ETX_recording_dictionary['path'], channel, animal, start_times_ETX)
                    if brain_state == 1:
                        time_start_values, time_end_values = brain_state_times_nonREM(brain_state_file, brain_state)
                        timevalues = timevalues_array_nonREM(time_start_values, time_end_values)
                    else:
                        timevalues = brainstate_times_REM_wake(brain_state_file, brain_state)
                        filtered_data = highpass(concatenate_data)
                    datavalues = channel_data_extraction(timevalues, filtered_data)
                    without_artifacts = remove_noise(datavalues)
                    without_artifacts = without_artifacts[0]
                    welch_channel, psd, frequency = psd_per_channel(without_artifacts)
                    intercept_epochs_remove, slope_epochs_remove = look_for_outliers(psd, frequency)
                    psd_clean = remove_epochs(intercept_epochs_remove, slope_epochs_remove, psd)
                    slope_epochs, intercept_epochs = plot_lin_reg(psd_clean, frequency)
                    psd_average_1 = psd_average(psd_clean, frequency, animal)
                    list_average_1 = list(psd_average_1) 
                    results = pd.DataFrame(data = {str(brain_state) + animal + '_chan_' + str(channel):list_average_1})
                    data = pd.DataFrame(data = {str(brain_state) + '_' + str(animal) + '_chan_' + str(channel) + '_slope': slope_epochs, 
                    str(brain_state) + '_' + str(animal) + '_' + str(channel) + '_intercept': intercept_epochs})
                    small_dfs_one_brainstate.append(results)
                    slopegradient_intercept_1_brainstate.append(data)

        merged_power_file, merged_gradient_file = concatenate_files(small_dfs_two_brainstates, slopegradient_intercept_2_brainstate)
        save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, condition)
        merged_power_file, merged_gradient_file = concatenate_files(small_dfs_one_brainstate, slopegradient_intercept_1_brainstate)
        save_files(directory_name, merged_power_file, merged_gradient_file, brain_state, condition)