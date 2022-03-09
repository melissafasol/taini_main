import os 
import numpy as np 
import pandas as pd 

class LoadRecAndBrainFiles():
    '''this class contains all the functions required to load EEG datafiles'''
    
    '''folder_path = folder containing all brain states and numpy files
    animal_number = animal ids of files to be loaded together
    files = empty list to contain list of files corresponding to animal number
    start_1 = starting time for first numpy file 
    start_2 = starting tmie for second numpy file 
    channel_number = channel to slice out of loaded data recording'''
    
    
    def __init__(self, file_path, animal_id, channel_number):
        self.file_path = file_path
        self.animal_id = animal_id
        self.start_1 = animal_id + '_1'
        self.start_2 = animal_id + '_2'
        self.channel_number = channel_number
        
        '''to permanently save a value instead of loading each time, cache them under the init function'''
        #t1, t2 = self._get_start_time(start_dictionary)
        #self.t1, self.t2 = t1, t2 #to use throughout
        
    def get_requiredfiles(self):
        '''function returns file names in folder'''
        
        files = []
        data = None
        brain_state_1 = None
        brain_state_2 = None
        
        for r,d, f in os.walk(self.file_path):
            for file in f:
                if self.animal_id in file:
                    files.append(os.path.join(r, file))
        
        for i in files:
            if i.endswith('npy'):
                data = np.load(i)
                
        for i in files:
            if i.endswith('1_' + self.animal_id + '.pkl'):
                brain_state_1 = pd.read_pickle(i)
            else:
                if i.endswith('2_' + self.animal_id + '.pkl'):
                    brain_state_2 = pd.read_pickle(i)
        
        print('data1',data)
        
        return data, brain_state_1, brain_state_2
    
    
    def get_start_time(self, start_dictionary):
        '''function finds animal number in dictionary and loads data from the start point'''
        time_1 = None
        time_2 = None
        
        for self.animal_id in start_dictionary:
            if self.animal_id == self.start_1:
                time_1 = start_dictionary[self.animal_id]
            else:
                if self.animal_id == self.start_2:
                    time_2 = start_dictionary[self.animal_id]
                    
        time_1 = time_1[0]
        time_2 = time_2[0]
        
        return time_1, time_2
    
    
    def load_files(self, start_dictionary):
        
        data, brain_state_1, brain_state_2 = self.get_requiredfiles()
        
        print('data2',data)
        
        time_1, time_2 = self.get_start_time(start_dictionary)
        chan_num = self.channel_number
        '''function looks at filenames and loads numpy and corresponding brain state files'''
        
        data_baseline_1 = data[chan_num, time_1:]
        data_baseline_2 = data[chan_num, time_2:]
        
        return data_baseline_1, data_baseline_2 