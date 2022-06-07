import os 
import numpy as np
import pandas as pd



class ExtractBrainStateIndices:

    sample_rate = 250.4
    epoch_length = int(250.4 * 5)

    def __init__(self, brainstate_file, brainstate_number):
        self.brainstate_file = brainstate_file
        self.brainstate_number = brainstate_number
        self.epoch_indices = []
        self.time_start_values = []
        self.time_end_values = []


    def load_brainstate_file(self):
        brainstate_indices = self.brainstate_file.loc[self.brainstate_file['brainstate'] == self.brainstate_number]
        all_indices = brainstate_indices.index
        starting_index = all_indices[0]

        for epoch_index in range(len(all_indices)-1):
            if all_indices[epoch_index] + 1 != all_indices[epoch_index + 1]:
                self.epoch_indices.append([starting_index, all_indices[epoch_index]])
                starting_index = all_indices[epoch_index + 1]

        #append last value outside of the loop as the loop is for len -1
        self.epoch_indices.append([starting_index, all_indices[-1]])

        return self.epoch_indices

    def get_data_indices(self, epoch_indices):
        
        for epoch_index in range(len(self.epoch_indices)):
            self.time_start_values.append(self.brainstate_file.iloc[self.epoch_indices[epoch_index][0], 1]) 

        for epoch_index in range(len(self.epoch_indices)):
            self.time_end_values.append(self.brainstate_file.iloc[self.epoch_indices[epoch_index][1], 2])
 
        sample_rate_start = [int(element*self.sample_rate) for element in self.time_start_values]
        sample_rate_end = [int(element*self.sample_rate) for element in self.time_end_values]
        zipped_timevalues = list(zip(sample_rate_start, sample_rate_end))
        
        #lambda function to separate timebins by 5 seconds
        function_timebins = lambda epoch_start, epoch_end: list(range(epoch_start, epoch_end, ExtractBrainStateIndices.epoch_length))
        
        timevalues_epochs = list(map(lambda x: function_timebins(x[0], x[1]), (zipped_timevalues)))
        timevalues_array = np.hstack(timevalues_epochs)

        return timevalues_array

