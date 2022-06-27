import os 
import numpy as np 
import pandas as pd

from constants import start_times_baseline
from preparefiles_1 import PrepareFiles, LoadFromStart
from extractbrainstate_2 import ExtractBrainStateIndices
from filter_3 import Filter
from power_spectrum_analysis_4 import PowerSpectrum
from power_spectrum_analysis_4 import RemoveNoisyEpochs

#test commands for baseline two animals 
directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
animal_2_brainstates = 'S7063'
test_prepare_2 = PrepareFiles(directory_path=directory_path, animal_id=animal_2_brainstates)
recording, brain_state_1, brain_state_2 = test_prepare_2.load_two_analysis_files()
start_time_1, start_time_2 = test_prepare_2.get_two_start_times(start_times_baseline)
test_load_2 = LoadFromStart(recording = recording, start_time_1 = start_time_1, start_time_2 = start_time_2, channelnumber = 7)
data_1, data_2 = test_load_2.load_two_files_from_start()
test_extractbrain_states_2 = ExtractBrainStateIndices(brainstate_file = brain_state_1, brainstate_number = 2)
epoch_indices = test_extractbrain_states_2.load_brainstate_file()
timevalues_array = test_extractbrain_states_2.get_data_indices(epoch_indices)
test_filter_2 = Filter(data_1, timevalues_array)
filtered_data = test_filter_2.butter_bandpass()
test_power_2 = PowerSpectrum(filtered_data)
mean_psd, frequency = test_power_2.average_psd()
test_psd_noise_2 = RemoveNoisyEpochs(mean_psd, frequency)
slope, intercept,slope_remove, intercept_remove = test_psd_noise_2.lin_reg_spec_slope()
psd = test_psd_noise_2.remove_noisy_epochs(mean_psd, slope_remove, intercept_remove)