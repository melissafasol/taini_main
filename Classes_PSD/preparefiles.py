import os 
import numpy as np 
import pandas as pd 

class PrepareFiles():
    '''this class contains all the functions required to find brainstate files(in pkl format)
    and raw_recording files (in numpy format)'''
    
    '''folder_path = folder containing all brain states and numpy files
    animal_number = animal ids of files to be loaded together
    files = empty list to contain list of files corresponding to animal number
    start_1 = starting time for first numpy file 
    start_2 = starting tmie for second numpy file 
    channel_number = channel to slice out of loaded data recording
    start_dictionary = dictionary with start times for recording condition (baseline, saline or ETX)'''
    
    
    def __init__(self, directory_path, animal_id, channel, start_dictionary):
        self.directory_path = directory_path
        self.animal_id = animal_id
        self.start_1 = '1_' + animal_id + '.pkl'
        self.start_2 = '2_' + animal_id + '.pkl'
        self.channel = channel
        self.start_dictionary = start_dictionary
        
        '''to permanently save a value instead of loading each time, cache them under the init function'''
        #t1, t2 = self._get_start_time(start_dictionary)
        #self.t1, self.t2 = t1, t2 #to use throughout
        
    def get_data_files(self):
        '''function returns file names in folder'''
        os.chdir(self.directory_path)
        animal_recording = [filename for filename in os.listdir(self.directory_path) if filename.startswith(self.animal_id)]
        print(type(animal_recording))
        recording = np.load(animal_recording[0])
        brain_file_1 = [filename for filename in os.listdir(self.directory_path) if filename.endswith(self.start_1)]
        brain_state_1 = pd.read_pickle(brain_file_1[0])
        brain_file_2 = [filename for filename in os.listdir(self.directory_path) if filename.endswith(self.start_2)]
        brain_state_2 = pd.read_pickle(brain_file_2[0])
    
        return recording, brain_state_1, brain_state_2
    
    
    def get_start_time(self):
        '''function finds animal number in dictionary and loads data from the start point'''
        start_time_1 = None
        start_time_2 = None
        
        for self.animal_id in self.start_dictionary:
            if self.animal_id == self.start_1:
                time_1 = self.start_dictionary[self.animal_id]
                start_time_1 = time_1[0]            
            if self.animal_id == self.start_2:
                time_2 = self.start_dictionary[self.animal_id]
                start_time_2 = time_2[0]
            else:
                time_2 = None
                start_time_2 = None
        
        return start_time_1, start_time_2
    
    