

directory_path_saline = '/home/melissa/preprocessing/reformatted_brainstates_saline'
saline_prepare = SalinePrepare2Files(directory_path = directory_path_saline, animal_id = 'S7070', start_time_dict = start_times_saline, channel_number = 7)
concatenate_recordings_saline, concatenated_data_brain_state_saline = saline_prepare.load_ETX_two()
saline_extractbrainstates_2 = ExtractBrainStateIndices(brainstate_file = concatenated_data_brain_state_saline, brainstate_number = 2)
saline_epoch_indices_2 = saline_extractbrainstates_2.load_brainstate_file()
saline_timevalues_array_2 = test_extractbrain_states.get_data_indices(saline_epoch_indices_2)
saline_filter_2 = Filter(concatenate_recordings_saline, saline_timevalues_array_2)
filtered_data_2 = saline_filter_2.butter_bandpass()
saline_power_2 = PowerSpectrum(filtered_data_2)
mean_psd, frequency = saline_power_2.average_psd()
saline_psd_noise = RemoveNoisyEpochs(mean_psd, frequency)
slope, intercept,slope_remove, intercept_remove = saline_psd_noise.lin_reg_spec_slope()
psd = saline_psd_noise.remove_noisy_epochs(mean_psd, slope_remove, intercept_remove)