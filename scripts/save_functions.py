'''Created March 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file to concatenate and save dataframes and csv files according to brainstate and condition without having to change the name each time'''

import os
import pandas as pd


def average_power_df(power_list_1, power_list_2):
    results = pd.DataFrame(data = {'Power_1' : power_list_1, 'Power_2': power_list_2})
    average = results[['Power_1', 'Power_2']].mean(axis=1)
    return average

def power_df(animal, average_psd, channel, brainstate_number, frequency):
    power_data = {'Animal_ID': [animal]*len(average_psd), 'Channel': [channel]*len(average_psd), 'Brainstate': [brainstate_number]*len(average_psd), 'Frequency' : frequency, 'Power': average_psd}
    data = pd.DataFrame(data = power_data)
    return data

def spectral_slope_save(animal, channel, brainstate_number, gradient, intercept):
    spectral_slope_data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brainstate_number, 'Gradient': gradient, 'Intercept': intercept }
    data = pd.DataFrame(data = spectral_slope_data, index = [0])

    return data

def concatenate_files(power_file_to_concatenate, gradient_intercept_to_concatenate):
    merged_power_file = pd.concat(power_file_to_concatenate, axis=0).drop_duplicates().reset_index(drop=True)
    merged_gradient_file = pd.concat(gradient_intercept_to_concatenate, axis=0).drop_duplicates().reset_index(drop=True)

    return merged_power_file, merged_gradient_file

def save_files(directory_name, concatenated_power_file, concatenated_slope_file, brain_state_number, condition):
    #this function should save concatenated files as cv and save them according to brain state and condition 
    os.chdir(directory_name)

    if brain_state_number == 1:
        concatenated_power_file.to_csv(str(condition)  + '_nonREM_power.csv', index=True)
        concatenated_slope_file.to_csv(str(condition) + '_nonREM_slopeintercept.csv', index=True)

    if brain_state_number == 0:
        concatenated_power_file.to_csv(str(condition)  + '_wake_power.csv', index=True)
        concatenated_slope_file.to_csv(str(condition)  + '_wake_slopeintercept.csv', index=True)

    if brain_state_number == 2:
        concatenated_power_file.to_csv(str(condition)  + '_REM_power.csv', index=True)
        concatenated_slope_file.to_csv(str(condition)  + '_REM_slopeintercept.csv', index=True)

    if brain_state_number == 4:
        concatenated_power_file.to_csv(str(condition)  + '_seizure_power.csv', index=True)
        concatenated_slope_file.to_csv(str(condition)  + '_seizure_slopeintercept.csv', index=True)

