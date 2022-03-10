import os 
import numpy as np 
import pandas as pd 

class ExtractBrainstateTimes(object):
    '''This class contains all functions to slice out data indices corresponding to a particular brain state
    in 5 second time intervals'''
    
    def __init__(self, brainstate_file, brainstate_number):
        self.epoch_duration = int(250.4*5)
        self.brainstate_file = brainstate_file
        self.brainstate_number = brainstate_number
        

    def get_brainstate_excel_values(self):
        '''slice out excel values that correspond to brain state value'''
        column_indices = self.brainstate_file.iloc[:,0] == self.brainstate_number
        brain_state_indices = self.brainstate_file[column_indices]
        all_indices = brain_state_indices.index
        
        return all_indices
    
    def find_where_epoch_jumps(self, brainstate_file, brainstate_number):
        all_indices = self.get_brainstate_excel_values(brainstate_file, brainstate_number)
        epoch_indices = []
        starting_index = all_indices[0]
        
        #find where these indices jump into separate epochs 
        for i in range(len(all_indices)-1):
            if all_indices[i] + 1 != all_indices[i+1]:
                epoch_indices.append([starting_index, all_indices[i]])
                #need to add 1 to the starting index so that it moves to the next index after each loop
                starting_index = all_indices[i+1]
                
        #need to append the last value outside of the loop as loop is for len-1
        epoch_indices.append([starting_index, all_indices[-1]])
        
        #now go back to brain state file and sslice out start and end time values using indices as a guide
        time_start_values = []
        time_end_values = []
        
        for i in range(len(epoch_indices)):
            time_start_values.append(self.brainstate_file.iloc[epoch_indices[i][0], 1])
            
        for i in range(len(epoch_indices)):
            time_end_values.append(self.brainstate_file.iloc[epoch_indices[i][1], 2])
            
        #zip start and end values into pairs 
        zipped_timevalues = zip(time_start_values, time_end_values)
        time_values = list(zipped_timevalues)
        
        #multiply each value by sampling rate and convert to integer to access corresponding integer
        samplerate_start = [element*250.4 for element in time_start_values]
        samplerate_end = [element*250.4 for element in time_end_values]
        
        int_samplestart = [int(x) for x in samplerate_start]
        int_sampleend = [int(x) for x in samplerate_end]
        
        zipped_timevalues = zip(int_samplestart, int_sampleend)
        time_values = list(zipped_timevalues)
        
        #use lambda function to apply function to each time value variable to split into 5 second bins
        bin_separator = lambda a,b: list(range(a, b, self.epoch_duration))
        timevalues_epochs = list(map(lambda x: bin_separator(x[0], x[1]), (time_values)))
        
        #strip list of lists to long array of time values
        timevalues_array = np.hstack(timevalues_epochs)
        
        return timevalues_array