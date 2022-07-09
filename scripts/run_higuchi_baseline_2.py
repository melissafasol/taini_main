import numpy as np
import pandas as pd 
import antropy as ant 
from scipy import average, gradient
import stochastic.processes.noise as sn
import os

from preproc1_preparefiles import PrepareFiles, LoadFromStart
from constants import start_times_baseline
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter


#test commands for baseline two animals 
directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
brain_state_number = 4
channel_number_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
animal_two_brainstates = ['S7070', 'S7072', 'S7083', 'S7063','S7064', 'S7069', 'S7086', 'S7091']
seizure_two_brainstates = ['S7063', 'S7064', 'S7069', 'S7072']
higuchi_df = []
kmax_value = 75
perm_entr_df = []

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
        filtered_data_1 = np.array(filter_1.butter_bandpass())
        filtered_data_2 = np.array(filter_2.butter_bandpass())
        print('filtering complete')
        int_array_1 = filtered_data_1.astype(int)
        int_array_2 = filtered_data_2.astype(int)
        int_array = np.concatenate((int_array_1, int_array_2), axis = 0)
        hfd_results = np.array([ant.higuchi_fd(epoch, kmax=kmax_value) for epoch in int_array])
        hfd_results_array= hfd_results[np.logical_not(np.isnan(np.array(hfd_results)))]
        print('Fractal Dimension values calculated')
        perm_entr_results = np.array([ant.perm_entropy(epoch) for epoch in int_array])
        perm_entr_array = perm_entr_results[np.logical_not(np.isnan(np.array(perm_entr_results)))]
        hfd_results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'HGF': (np.mean(hfd_results_array)).flatten()})
        perm_entr_results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'Entropy': (np.mean(perm_entr_array)).flatten()})
        higuchi_df.append(hfd_results_df)
        perm_entr_df.append(perm_entr_results_df)

concat_hfd = pd.concat(higuchi_df, axis = 0).drop_duplicates().reset_index(drop=True)
concat_perm_entr = pd.concat(perm_entr_df, axis = 0).drop_duplicates().reset_index(drop=True)

os.chdir('/home/melissa/class_refactor/FractalDimension/baseline')
concat_hfd.to_csv(str(brain_state_number) + '_2br_baseline_hfd.csv')

os.chdir('/home/melissa/class_refactor/PermutationEntropy')
concat_perm_entr.to_csv(str(brain_state_number) + '_2br_baseline_perm_entr.csv')