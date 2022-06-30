import os 
import numpy as np 
import pandas as pd
from scipy import average, gradient
import antropy as ant
import os

from constants import start_times_saline
from preproc1a_preparefiles_ETX_saline import PrepareETXSaline1File, SalinePrepare2Files
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter



directory_path_saline = '/home/melissa/preprocessing/reformatted_brainstates_saline'
animal_two =  ['S7070', 'S7071', 'S7074', 'S7075']
animal_one =  ['S7094', 'S7098', 'S7101','S7063', 'S7064', 'S7068', 'S7069','S7072', 'S7076', 'S7083', 'S7086', 'S7088', 'S7091', 'S7092', 'S7096']
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
brain_state_number = 2
kmax_value = 75
hfd_df_two = []

for animal in animal_two:
    for channel in channel_number_list:
        saline_prepare = SalinePrepare2Files(directory_path = directory_path_saline, animal_id = animal, start_time_dict = start_times_saline, channel_number = channel)
        concatenate_recordings_saline, concatenated_data_brain_state_saline = saline_prepare.load_ETX_two()
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        saline_extractbrainstates_2 = ExtractBrainStateIndices(brainstate_file = concatenated_data_brain_state_saline, brainstate_number = brain_state_number)
        saline_epoch_indices_2 = saline_extractbrainstates_2.load_brainstate_file()
        saline_timevalues_array_2 = saline_extractbrainstates_2.get_data_indices(saline_epoch_indices_2)
        saline_filter_2 = Filter(concatenate_recordings_saline, saline_timevalues_array_2)
        filtered_data_2 = np.array(saline_filter_2.butter_bandpass())
        print('filtering complete')
        int_array = filtered_data_2.astype(int)
        results_1 = np.array([ant.higuchi_fd(epoch, kmax=kmax_value) for epoch in int_array])
        results_array = results_1[np.logical_not(np.isnan(np.array(results_1)))]
        print('Fractal Dimension values calculated')
        results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'HGF': (np.mean(results_array)).flatten()})
        hfd_df_two.append(results_df)
       
concat_hfd = pd.concat(hfd_df_two, axis = 0).drop_duplicates().reset_index(drop=True)

os.chdir('/home/melissa/class_refactor/FractalDimension/saline')
concat_hfd.to_csv(str(brain_state_number) + '_2br_saline_hfd.csv')

hfd_df_one = []

for animal in animal_one:
    for channel in channel_number_list:
        ETX_prepare_1 = PrepareETXSaline1File(directory_path = directory_path_saline, animal_id = animal, start_time_dict = start_times_saline, channel_number = channel)
        recording_1, brain_state_1 = ETX_prepare_1.load_one_analysis_file()
        recording_from_start = ETX_prepare_1.load_one_file(recording_1)
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        ETX_extractbrainstates = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = brain_state_number)
        ETX_epoch_indices = ETX_extractbrainstates.load_brainstate_file()
        ETX_timevalues_array = ETX_extractbrainstates.get_data_indices(ETX_epoch_indices)
        ETX_filter = Filter(recording_from_start, ETX_timevalues_array)
        filtered_data = ETX_filter.butter_bandpass()
        print('filtering complete')
        int_array = filtered_data.astype(int)
        results_1 = np.array([ant.higuchi_fd(epoch, kmax=kmax_value) for epoch in int_array])
        results_array = results_1[np.logical_not(np.isnan(np.array(results_1)))]
        print('Fractal Dimension values calculated')
        results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'HGF': (np.mean(results_array)).flatten()})
        hfd_df_one.append(results_df)

concat_hfd = pd.concat(hfd_df_one, axis = 0).drop_duplicates().reset_index(drop=True)

os.chdir('/home/melissa/class_refactor/FractalDimension/saline')
concat_hfd.to_csv(str(brain_state_number) + '_1br_saline_hfd.csv')
