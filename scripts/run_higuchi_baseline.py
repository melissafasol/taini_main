import antropy as ant 
import numpy as np
import pandas as pd
import stochastic.processes.noise as sn
import os
from statistics import mean

from preproc1_preparefiles import PrepareFiles, LoadFromStart
from constants import start_times_baseline
from preproc2_extractbrainstate import ExtractBrainStateIndices
from preproc3_filter import Filter

os.chdir('/home/melissa/class_refactor/FractalDimension/baseline/REM')

directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
brain_state_number = 2
kmax_range = list(range(2, 100))
channel_list = [0,2,3,4,5,6,7,8,9,10,11,12,13,15]
kmax_value = 75
animal_one_brainstate_list = ['S7098', 'S7068', 'S7074','S7076', 'S7071', 'S7075','S7087', 'S7088', 'S7092', 'S7094', 'S7101']
higuchi_df = []

for animal in animal_one_brainstate_list:
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
        results_1 = [ant.higuchi_fd(epoch, kmax=kmax_value) for epoch in int_array]
        results_array = np.logical_not(np.isnan(np.array(results_1)))
        print('Fractal Dimension values calculated')
        results_df = pd.DataFrame(data = {'Animal_ID': animal, 'Channel': channel, 'Brainstate': brain_state_number, 'HGF': results_array})
        higuchi_df.append(results_df)

concat_hfd = pd.concat(higuchi_df, axis = 0).drop_duplicates().reset_index(drop=True)

os.chdir('/home/melissa/class_refactor/FractalDimension/baseline/REM')
concat_hfd.to_csv(str(brain_state_number) + '_1br_baseline_hfd.csv')
