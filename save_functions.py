'''Created March 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file to concatenate and save dataframes and csv files according to brainstate and condition without having to change the name each time'''

import os
import pandas as pd

os.chdir('/home/melissa/Results')

def concatenate_files(power_file_to_concatenate, gradient_intercept_to_concatenate):
    merged_power_file = pd.concat(power_file_to_concatenate, axis=1)
    merged_gradient_file = pd.concat(gradient_intercept_to_concatenate, axis=1)

    return merged_power_file, merged_gradient_file

def save_files(directory_name, concatenated_power_file, concatenated_slope_file, brain_state_number, condition):
    #this function should save concatenated files as cv and save them according to brain state and condition 
    os.chdir(directory_name)

    if brain_state_number == 1:
        concatenated_power_file.to_csv(str(condition) + 'nonREM_power_1npyfile.csv', index=True)
        concatenated_slope_file.to_csv('baseline_nonREM_slopeintercept_1npyfile.csv', index=True)

    if brain_state_number == 0:
        concatenated_power_file.to_csv(str(condition) + '_wake_epoch_test_1npyfile.csv', index=True)
        concatenated_slope_file.to_csv(str(condition) + '_wake_slopeintercept_1npyfile.csv', index=True)

    if brain_state_number == 2:
        concatenated_power_file.to_csv(str(condition) + '_REM_epoch_test_1npyfile.csv', index=True)
        concatenated_slope_file.to_csv(str(condition) + 'baseline_REM_slopeintercept_1npyfile.csv', index=True)