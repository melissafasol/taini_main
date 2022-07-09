import antropy as ant 
import numpy as np
import pandas as pd
import stochastic.processes.noise as sn
import os
from statistics import mean

from preproc1_preparefiles import PrepareFiles, LoadFromStart
from scripts.SYNGAP_constants import start_times_baseline
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter


directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
brain_state_number = 4
kmax_range = list(range(2, 100))
channel_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
kmax_value = 75
animal_one_brainstate_list = ['S7098', 'S7068', 'S7074','S7076', 'S7071', 'S7075','S7087', 'S7088', 'S7092', 'S7094', 'S7101']
seizure_one_brainstate = ['S7075', 'S7092', 'S7094', 'S7074', 'S7088']
higuchi_df = []
perm_entr_df = []

for animal in seizure_one_brainstate:
    prepare_files = PrepareFiles(directory_path=directory_path, animal_id = animal)
    recording, brain_state_1 = prepare_files.load_one_analysis_file()
    start_time_1, start_time_2 = prepare_files.get_one_start_time(start_times_baseline)
    for channel in channel_list:
        test_load = LoadFromStart(recording = recording, start_time_1 = start_time_1, start_time_2 = start_time_2, channelnumber = channel)
        data_1 = test_load.load_one_file_from_start()
        print('all data loaded for ' + str(animal) + ' channel number ' + str(channel))
        extractbrain_states = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = brain_state_number)
        epoch_indices = extractbrain_states.load_brainstate_file()
        timevalues_array = extractbrain_states.get_data_indices(epoch_indices)
        apply_filter = Filter(data_1, timevalues_array)
        filtered_data = np.array(apply_filter.butter_bandpass())
        print('filtering complete')
        int_array = filtered_data.astype(int)
        hfd_results = np.array([ant.higuchi_fd(epoch, kmax=kmax_value) for epoch in int_array])
        perm_entr_results = np.array([ant.perm_entropy(epoch)for epoch in int_array])
        hfd_results_array = hfd_results[np.logical_not(np.isnan(np.array(hfd_results)))]
        print('Fractal Dimension values calculated')
        perm_entr_array = perm_entr_results[np.logical_not(np.isnan(np.array(perm_entr_results)))]
        hfd_results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'HGF': (np.mean(hfd_results_array)).flatten()})
        perm_entr_results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'Entropy': (np.mean(perm_entr_array)).flatten()})
        higuchi_df.append(hfd_results_df)
        perm_entr_df.append(perm_entr_results_df)

concat_hfd = pd.concat(higuchi_df, axis = 0).drop_duplicates().reset_index(drop=True)
concat_perm_entr = pd.concat(perm_entr_df, axis = 0).drop_duplicates().reset_index(drop = True)

os.chdir('/home/melissa/class_refactor/FractalDimension/baseline')
concat_hfd.to_csv(str(brain_state_number) + '_1br_baseline_hfd.csv')

os.chdir('/home/melissa/class_refactor/PermutationEntropy/')
concat_perm_entr.to_csv(str(brain_state_number) + '_1br_baseline_perm_entr.csv')

