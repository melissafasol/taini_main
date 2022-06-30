import os 
import numpy as np 
import pandas as pd
from scipy import average, gradient

from constants import start_times_ETX
from preproc1a_preparefiles_ETX_saline import ETXPrepare2Files, PrepareETXSaline1File
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter
from preproc4_power_spectrum_analysis import PowerSpectrum
from preproc4_power_spectrum_analysis import RemoveNoisyEpochs
from save_functions import average_power_df, concatenate_files, power_df, save_files, spectral_slope_save



directory_path_ETX = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
two_brainstates = ['S7063','S7064', 'S7068', 'S7069', 'S7072', 'S7088', 'S7094', 'S7096']
one_brainstate = ['S7070', 'S7071', 'S7075', 'S7076', 'S7083', 'S7086', 'S7087','S7092', 'S7098', 'S7101', 'S7074', 'S7091']
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
brain_state_number = 2
power_data_list = []
spectral_slope_df = []

for animal in two_brainstates:
    for channel in channel_number_list:
        ETX_prepare_2 = ETXPrepare2Files(directory_path = directory_path_ETX, animal_id = animal, start_time_dict = start_times_ETX, channel_number = channel)
        recordings_ETX_2, brain_state_ETX_2 = ETX_prepare_2.load_ETX_two()
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        ETX_extractbrain_states_2 = ExtractBrainStateIndices(brainstate_file = brain_state_ETX_2, brainstate_number = brain_state_number)
        epoch_indices_2 = ETX_extractbrain_states_2.load_brainstate_file()
        timevalues_array_2 = ETX_extractbrain_states_2.get_data_indices(epoch_indices_2)
        ETX_filter = Filter(recordings_ETX_2, timevalues_array_2)
        filtered_data_2 = ETX_filter.butter_bandpass()
        print('filtering complete')
        ETX_power = PowerSpectrum(filtered_data_2)
        mean_psd_2, frequency_2 = ETX_power.average_psd()
        ETX_psd_noise = RemoveNoisyEpochs(mean_psd_2, frequency_2)
        slope_2, intercept_2,slope_remove, intercept_remove = ETX_psd_noise.lin_reg_spec_slope()
        psd = ETX_psd_noise.remove_noisy_epochs(mean_psd_2, slope_remove, intercept_remove)
        power_data_2 = power_df(animal, psd, channel, brain_state_number, frequency=frequency_2)
        print('power calculated and saved')
        spectral_slope_data_2 = spectral_slope_save(animal, channel, brain_state_number, slope_2, intercept_2)
        power_data_list.append(power_data_2)
        spectral_slope_df.append(spectral_slope_data_2)
        print('spectral slope calculated and saved')

power_dataframe, spectral_slope_dataframe = concatenate_files(power_file_to_concatenate=power_data_list, gradient_intercept_to_concatenate= spectral_slope_df)

save_directory = '/home/melissa/Results'
save_files(directory_name = save_directory, concatenated_power_file = power_dataframe, concatenated_slope_file = spectral_slope_dataframe, brain_state_number=brain_state_number, condition = 'ETX_concat_')


power_data_one = []
spectral_slope_one = []

for animal in one_brainstate:
    for channel in channel_number_list:
        ETX_prepare_1 = PrepareETXSaline1File(directory_path = directory_path_ETX, animal_id = animal, start_time_dict = start_times_ETX, channel_number = channel)
        recording_1, brain_state_1 = ETX_prepare_1.load_one_analysis_file()
        recording_from_start = ETX_prepare_1.load_one_file(recording_1)
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        ETX_extractbrainstates = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = brain_state_number)
        ETX_epoch_indices = ETX_extractbrainstates.load_brainstate_file()
        ETX_timevalues_array = ETX_extractbrainstates.get_data_indices(ETX_epoch_indices)
        ETX_filter = Filter(recording_from_start, ETX_timevalues_array)
        filtered_data = ETX_filter.butter_bandpass()
        print('filtering complete')
        ETX_power = PowerSpectrum(filtered_data)
        mean_psd, frequency = ETX_power.average_psd()
        ETX_psd_noise = RemoveNoisyEpochs(mean_psd, frequency)
        slope, intercept,slope_remove, intercept_remove = ETX_psd_noise.lin_reg_spec_slope()
        psd = ETX_psd_noise.remove_noisy_epochs(mean_psd, slope_remove, intercept_remove)
        power_data = power_df(animal, psd, channel, brain_state_number, frequency=frequency)
        print('power calculated and saved')
        spectral_slope_data = spectral_slope_save(animal, channel, brain_state_number, slope, intercept)
        power_data_one.append(power_data)
        spectral_slope_one.append(spectral_slope_data)
        print('spectral slope calculated and saved')

power_dataframe, spectral_slope_dataframe = concatenate_files(power_file_to_concatenate=power_data_one, gradient_intercept_to_concatenate= spectral_slope_one)

save_files(directory_name = save_directory, concatenated_power_file = power_dataframe, concatenated_slope_file = spectral_slope_dataframe, brain_state_number=brain_state_number, condition = 'ETX_')