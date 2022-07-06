import os 
import numpy as np 
import pandas as pd
from scipy import average, gradient
import antropy as ant
import os

from constants import start_times_ETX
from preproc1a_preparefiles_ETX_saline import ETXPrepare2Files, PrepareETXSaline1File
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter



directory_path_ETX = '/home/melissa/preprocessing/reformatted_brainstates_ETX'
two_brainstates = ['S7063','S7064', 'S7068', 'S7069', 'S7072', 'S7088', 'S7094', 'S7096']
one_brainstate = ['S7070', 'S7071', 'S7075', 'S7076', 'S7083', 'S7086', 'S7087','S7092', 'S7098', 'S7101', 'S7074', 'S7091']
seizure_two_numpy_file =  ['S7088', 'S7063', 'S7064', 'S7068', 'S7069', 'S7072', 'S7094', 'S7096'] #S7088 
seizure_one_numpy_file = ['S7074', 'S7075', 'S7076', 'S7092']
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
brain_state_number = 4
kmax_value = 75
hfd_df_two = []
perm_entr_two = []

for animal in seizure_two_numpy_file:
    for channel in channel_number_list:
        ETX_prepare_2 = ETXPrepare2Files(directory_path = directory_path_ETX, animal_id = animal, start_time_dict = start_times_ETX, channel_number = channel)
        recordings_ETX_2, brain_state_ETX_2 = ETX_prepare_2.load_ETX_two()
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        ETX_extractbrain_states_2 = ExtractBrainStateIndices(brainstate_file = brain_state_ETX_2, brainstate_number = brain_state_number)
        epoch_indices_2 = ETX_extractbrain_states_2.load_brainstate_file()
        timevalues_array_2 = ETX_extractbrain_states_2.get_data_indices(epoch_indices_2)
        ETX_filter = Filter(recordings_ETX_2, timevalues_array_2)
        filtered_data_2 = np.array(ETX_filter.butter_bandpass())
        print('filtering complete')
        int_array = filtered_data_2.astype(int)
        results_1 = np.array([ant.higuchi_fd(epoch, kmax=kmax_value) for epoch in int_array])
        results_perm_entr = np.array([ant.perm_entropy(epoch) for epoch in int_array])
        results_hfd_array = results_1[np.logical_not(np.isnan(np.array(results_1)))]
        results_perm_entr_array = results_1[np.logical_not(np.isnan(np.array(results_perm_entr)))]
        print('Fractal Dimension values calculated')
        results_hfd_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'HGF': (np.mean(results_hfd_array)).flatten()})
        results_perm_entr_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'Entropy': (np.mean(results_perm_entr_array)).flatten()})
        hfd_df_two.append(results_hfd_df)
        perm_entr_two.append(results_perm_entr_df)

       
concat_hfd = pd.concat(hfd_df_two, axis = 0).drop_duplicates().reset_index(drop=True)
concat_perm_entr = pd.concat(perm_entr_two, axis=0).drop_duplicates().reset_index(drop=True)

os.chdir('/home/melissa/class_refactor/FractalDimension')
concat_hfd.to_csv(str(brain_state_number) + '_2br_ETX_hfd.csv')

os.chdir('/home/melissa/class_refactor/PermutationEntropy')
concat_perm_entr.to_csv(str(brain_state_number) + '2br_ETX_permentr.csv')

hfd_df_one = []
perm_entr_one = []

for animal in seizure_one_numpy_file:
    for channel in channel_number_list:
        ETX_prepare_1 = PrepareETXSaline1File(directory_path = directory_path_ETX, animal_id = animal, start_time_dict = start_times_ETX, channel_number = channel)
        recording_1, brain_state_1 = ETX_prepare_1.load_one_analysis_file()
        recording_from_start = ETX_prepare_1.load_one_file(recording_1)
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        ETX_extractbrainstates = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = brain_state_number)
        ETX_epoch_indices = ETX_extractbrainstates.load_brainstate_file()
        ETX_timevalues_array = ETX_extractbrainstates.get_data_indices(ETX_epoch_indices)
        ETX_filter = Filter(recording_from_start, ETX_timevalues_array)
        filtered_data = np.array(ETX_filter.butter_bandpass(), dtype= object)
        print('filtering complete')
        results_hfd = np.array([ant.higuchi_fd(epoch, kmax=kmax_value) for epoch in int_array])
        results_perm_entr = np.array([ant.perm_entropy(epoch) for epoch in int_array])
        results_hfd_array = results_hfd[np.logical_not(np.isnan(np.array(results_hfd)))]
        print('Fractal Dimension values calculated')
        results_perm_entr_array = results_perm_entr[np.logical_not(np.isnan(np.array(results_perm_entr)))]
        print('Permutation Entropy values calculated')
        results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'HGF': (np.mean(results_hfd_array)).flatten()})
        results_perm_entr_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'Entropy': (np.mean(results_perm_entr_array)).flatten()})
        hfd_df_one.append(results_df)
        perm_entr_one.append(results_perm_entr_df)

concat_hfd = pd.concat(hfd_df_one, axis = 0).drop_duplicates().reset_index(drop=True)
concat_perm_entr = pd.concat(perm_entr_one, axis = 0).drop_duplicates().reset_index(drop=True)

os.chdir('/home/melissa/class_refactor/FractalDimension')
concat_hfd.to_csv(str(brain_state_number) + '_1br_ETX_hfd.csv')

os.chdir('/home/melissa/class_refactor/PermutationEntropy')
concat_perm_entr.to_csv(str(brain_state_number) + '_1br_ETX_permentr.csv')
