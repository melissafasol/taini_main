import numpy as np
import pandas as pd 
import antropy as ant 
from scipy import average, gradient
import stochastic.processes.noise as sn

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
power_two_brainstate_df = []
spectral_slope_two_brainstate_df = [] 

for animal in animal_two_brainstates:
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