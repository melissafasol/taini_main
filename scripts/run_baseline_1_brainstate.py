import os 
import numpy as np 
import pandas as pd
from scipy import average, gradient

from constants import start_times_baseline
from preparefiles_1 import PrepareFiles, LoadFromStart
from extractbrainstate_2 import ExtractBrainStateIndices
from filter_3 import Filter
from power_spectrum_analysis_4 import PowerSpectrum
from power_spectrum_analysis_4 import RemoveNoisyEpochs
from save_functions import average_power_df, concatenate_files, power_df, save_files, spectral_slope_save

directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
brain_state_number = 1
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
animal_one_brainstate_list = ['S7098', 'S7068', 'S7074','S7076', 'S7071', 'S7075','S7087', 'S7088', 'S7092', 'S7094', 'S7101']
seizure_one_brainstate = ['S7075', 'S7092', 'S7094', 'S7074', 'S7068']
power_data_list = []
spectral_slope_df = []
for animal in animal_one_brainstate_list:
    prepare_files = PrepareFiles(directory_path=directory_path, animal_id = animal)
    recording, brain_state_1 = prepare_files.load_one_analysis_file()
    start_time_1, start_time_2 = prepare_files.get_one_start_time(start_times_baseline)
    for channel in channel_number_list:
        test_load = LoadFromStart(recording = recording, start_time_1 = start_time_1, start_time_2 = start_time_2, channelnumber = channel)
        data_1 = test_load.load_one_file_from_start()
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        extractbrain_states = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = brain_state_number)
        epoch_indices = extractbrain_states.load_brainstate_file()
        timevalues_array = extractbrain_states.get_data_indices(epoch_indices)
        apply_filter = Filter(data_1, timevalues_array)
        filtered_data = apply_filter.butter_bandpass()
        print('filtering complete')
        power = PowerSpectrum(filtered_data)
        mean_psd, frequency = power.average_psd()
        psd_noise = RemoveNoisyEpochs(mean_psd, frequency)
        slope, intercept,slope_remove, intercept_remove = psd_noise.lin_reg_spec_slope()
        psd = psd_noise.remove_noisy_epochs(mean_psd, slope_remove, intercept_remove)
        power_data = power_df(animal, psd, channel, brain_state_number, frequency=frequency)
        print('power calculated and saved')
        spectral_slope_data = spectral_slope_save(animal, channel, brain_state_number, slope, intercept)
        power_data_list.append(power_data)
        spectral_slope_df.append(spectral_slope_data)
        print('spectral slope calculated and saved')

power_dataframe, spectral_slope_dataframe = concatenate_files(power_file_to_concatenate=power_data_list, gradient_intercept_to_concatenate= spectral_slope_df)

save_directory = '/home/melissa/Results/rem'
save_files(directory_name = save_directory, concatenated_power_file = power_dataframe, concatenated_slope_file = spectral_slope_dataframe, brain_state_number=brain_state_number, condition = 'baseline_1br_')