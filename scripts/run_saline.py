
import os 
import numpy as np 
import pandas as pd
from scipy import average, gradient
from scripts.SYNGAP_constants import start_times_saline
from scripts.SYNGAP_constants import start_times_ETX
from preproc1a_preparefiles_ETX_saline import ETXPrepare2Files, PrepareETXSaline1File, SalinePrepare2Files
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter
from preproc4_power_spectrum_analysis import PowerSpectrum
from preproc4_power_spectrum_analysis import RemoveNoisyEpochs
from save_functions import average_power_df, concatenate_files, power_df, save_files, spectral_slope_save

directory_path_saline = '/home/melissa/preprocessing/reformatted_brainstates_saline'
animal_two =  ['S7070', 'S7071', 'S7074', 'S7075']
animal_one =  ['S7094', 'S7098', 'S7101','S7063', 'S7064', 'S7068', 'S7069','S7072', 'S7076', 'S7083', 'S7086', 'S7088', 'S7091', 'S7092', 'S7096']
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
brain_state_number = 2
power_data_list = []
spectral_slope_df = []

for animal in animal_two:
    for channel in channel_number_list:
        saline_prepare = SalinePrepare2Files(directory_path = directory_path_saline, animal_id = animal, start_time_dict = start_times_saline, channel_number = channel)
        concatenate_recordings_saline, concatenated_data_brain_state_saline = saline_prepare.load_ETX_two()
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        saline_extractbrainstates_2 = ExtractBrainStateIndices(brainstate_file = concatenated_data_brain_state_saline, brainstate_number = 2)
        saline_epoch_indices_2 = saline_extractbrainstates_2.load_brainstate_file()
        saline_timevalues_array_2 = saline_extractbrainstates_2.get_data_indices(saline_epoch_indices_2)
        saline_filter_2 = Filter(concatenate_recordings_saline, saline_timevalues_array_2)
        filtered_data_2 = saline_filter_2.butter_bandpass()
        print('filtering complete')
        saline_power_2 = PowerSpectrum(filtered_data_2)
        mean_psd, frequency_2 = saline_power_2.average_psd()
        saline_psd_noise = RemoveNoisyEpochs(mean_psd, frequency_2)
        slope_2, intercept_2,slope_remove, intercept_remove = saline_psd_noise.lin_reg_spec_slope()
        psd = saline_psd_noise.remove_noisy_epochs(mean_psd, slope_remove, intercept_remove)
        power_data_2 = power_df(animal, psd, channel, brain_state_number, frequency=frequency_2)
        print('power calculated and saved')
        spectral_slope_data_2 = spectral_slope_save(animal, channel, brain_state_number, slope_2, intercept_2)
        power_data_list.append(power_data_2)
        spectral_slope_df.append(spectral_slope_data_2)
        print('spectral slope calculated and saved')

power_dataframe, spectral_slope_dataframe = concatenate_files(power_file_to_concatenate=power_data_list, gradient_intercept_to_concatenate= spectral_slope_df)

save_directory = '/home/melissa/Results'
save_files(directory_name = save_directory, concatenated_power_file = power_dataframe, concatenated_slope_file = spectral_slope_dataframe, brain_state_number=brain_state_number, condition = 'saline_concat_')


power_data_one = []
spectral_slope_one = []

for animal in animal_one:
    for channel in channel_number_list:
        saline_prepare = PrepareETXSaline1File(directory_path = directory_path_saline, animal_id = 'S7068', start_time_dict = start_times_saline, channel_number = 7)
        recording, brain_state = saline_prepare.load_one_analysis_file()
        recording_from_start = saline_prepare.load_one_file(recording)
        saline_extractbrainstates = ExtractBrainStateIndices(brainstate_file = brain_state, brainstate_number = 2)
        saline_epoch_indices = saline_extractbrainstates.load_brainstate_file()
        saline_timevalues_array = saline_extractbrainstates.get_data_indices(saline_epoch_indices)
        saline_filter = Filter(recording_from_start, saline_timevalues_array)
        filtered_data = saline_filter.butter_bandpass()
        saline_power = PowerSpectrum(filtered_data)
        mean_psd, frequency = saline_power.average_psd()
        saline_psd_noise = RemoveNoisyEpochs(mean_psd, frequency)
        slope, intercept,slope_remove, intercept_remove = saline_psd_noise.lin_reg_spec_slope()
        psd = saline_psd_noise.remove_noisy_epochs(mean_psd, slope_remove, intercept_remove)
        power_data = power_df(animal, psd, channel, brain_state_number, frequency=frequency)
        print('power calculated and saved')
        spectral_slope_data = spectral_slope_save(animal, channel, brain_state_number, slope, intercept)
        power_data_one.append(power_data)
        spectral_slope_one.append(spectral_slope_data)
        print('spectral slope calculated and saved')

power_dataframe, spectral_slope_dataframe = concatenate_files(power_file_to_concatenate=power_data_one, gradient_intercept_to_concatenate= spectral_slope_one)

save_files(directory_name = save_directory, concatenated_power_file = power_dataframe, concatenated_slope_file = spectral_slope_dataframe, brain_state_number=brain_state_number, condition = 'saline_')