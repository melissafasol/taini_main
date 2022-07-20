import os 
import numpy as np 
import pandas as pd
from scipy import average, gradient

from S7096 import concatenate_S7096
from scripts.SYNGAP_constants import start_times_baseline, start_times_S7096_baseline
from preproc1_preparefiles import PrepareFiles, LoadFromStart
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter
from preproc4_power_spectrum_analysis import PowerSpectrum
from preproc4_power_spectrum_analysis import RemoveNoisyEpochs
from save_functions import average_power_df, concatenate_files, power_df, save_files, spectral_slope_save

#test commands for baseline two animals 
directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
brain_state_number = 4
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
animal_two_brainstates = ['S7096', 'S7070', 'S7072', 'S7083', 'S7063','S7064', 'S7069', 'S7086', 'S7091']
seizure_two_brainstates = ['S7063', 'S7064', 'S7069', 'S7072']
power_two_brainstate_df = []
spectral_slope_two_brainstate_df = [] 

for animal in seizure_two_brainstates:
    test_prepare_2 = PrepareFiles(directory_path=directory_path, animal_id=animal)
    recording, brain_state_1, brain_state_2 = test_prepare_2.load_two_analysis_files()
    start_time_1, start_time_2 = test_prepare_2.get_two_start_times(start_times_baseline)
    for channel in channel_number_list:
        test_load_2 = LoadFromStart(recording = recording, start_time_1 = start_time_1, start_time_2 = start_time_2, channelnumber = channel)
        data_1, data_2 = test_load_2.load_two_files_from_start()
        extract_brain_state_1 = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = brain_state_number)
        extract_brain_state_2 = ExtractBrainStateIndices(brainstate_file = brain_state_2, brainstate_number = brain_state_number)
        epoch_indices_1 = extract_brain_state_1.load_brainstate_file()
        epoch_indices_2 = extract_brain_state_2.load_brainstate_file()
        timevalues_array_1 = extract_brain_state_1.get_data_indices(epoch_indices_1)
        timevalues_array_2 = extract_brain_state_2.get_data_indices(epoch_indices_2)
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        filter_1 = Filter(data_1, timevalues_array_1)
        filter_2 = Filter(data_2, timevalues_array_2)
        filtered_data_1 = filter_1.butter_bandpass()
        filtered_data_2 = filter_2.butter_bandpass()
        print('filtering complete')
        power_1 = PowerSpectrum(filtered_data_1)
        power_2 = PowerSpectrum(filtered_data_2)
        mean_psd_1, frequency_1 = power_1.average_psd()
        mean_psd_2, frequency_2 = power_2.average_psd()
        psd_noise_1 = RemoveNoisyEpochs(mean_psd_1, frequency_1)
        psd_noise_2 = RemoveNoisyEpochs(mean_psd_2, frequency_2)
        slope_1, intercept_1, slope_remove_1, intercept_remove_1 = psd_noise_1.lin_reg_spec_slope()
        slope_2, intercept_2,slope_remove_2, intercept_remove_2 = psd_noise_2.lin_reg_spec_slope()
        psd_1 = psd_noise_1.remove_noisy_epochs(mean_psd_1, slope_remove_1, intercept_remove_1)
        psd_2 = psd_noise_2.remove_noisy_epochs(mean_psd_2, slope_remove_2, intercept_remove_2)
        average_psd = average_power_df(psd_1, psd_2)
        power_data = power_df(animal, average_psd, channel, brain_state_number, frequency=frequency_1)
        print('power calculated and saved')
        spectral_slope_data_1 = spectral_slope_save(animal, channel, brain_state_number, slope_1, intercept_1)
        spectral_slope_data_2 = spectral_slope_save(animal, channel, brain_state_number, slope_2, intercept_2)
        power_two_brainstate_df.append(power_data)
        spectral_slope_two_brainstate_df.append(spectral_slope_data_1)
        spectral_slope_two_brainstate_df.append(spectral_slope_data_2)
        print('spectral slope calculated and saved')

power_dataframe, spectral_slope_dataframe = concatenate_files(power_file_to_concatenate=power_two_brainstate_df, gradient_intercept_to_concatenate=spectral_slope_two_brainstate_df)

print(power_dataframe)

save_directory = '/home/melissa/Results/seizure_data'
save_files(directory_name = save_directory, concatenated_power_file = power_dataframe, concatenated_slope_file = spectral_slope_dataframe, brain_state_number=brain_state_number, condition = 'baseline')