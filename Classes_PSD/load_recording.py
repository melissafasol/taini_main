import os 
import numpy as np 
import pandas as pd 

class LoadRecording():
    '''this class contains all the functions required to find brainstate files(in pkl format)
    and raw_recording files (in numpy format)'''
    
    '''
    start_1 = starting time for first numpy file 
    start_2 = starting time for second numpy file 
    channel_number = channel to slice out of loaded data recording
    start_dictionary = dictionary with start times for recording condition (baseline, saline or ETX)'''
    
    
    def __init__(self, recording_to_load, brain_state_file_1, brain_state_file_2, start_time_1, start_time_2, channel_number):
        self.recording_to_load = recording_to_load
        self.brain_state_file_1 = brain_state_file_1
        self.brain_state_file_2 = brain_state_file_2
        self.start_time_1 = start_time_1
        self.start_time_2 = start_time_2 
        self.channel_number = channel_number
        

    def get_prepared_recording(self):
        'function loads the recording according to specified channel and start time from start time dictionary'

        data_baseline_1 = self.recording_to_load[self.channel_number, self.start_time_1:]
        
        if type(self.start_time_2) == int:
            data_baseline_2 = self.recording_to_load[self.channel_number, self.start_time_2:]
        else:
            data_baseline_2 = None 
        
        return data_baseline_1, data_baseline_2 