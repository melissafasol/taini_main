from tracemalloc import start
from builtins import classmethod
import os 
import numpy as np
import pandas as pd
from constants import start_times_baseline

class PrepareFiles:
    
    def __init__(self, directory_path, animal_id):
        self.directory_path = directory_path
        self.animal_id = animal_id
        self.start_1 = '1_' + animal_id + '.pkl'
        self.start_2 = '2_' + animal_id + '.pkl'
        self.start_dict_1 = animal_id + '_1'
        self.start_dict_2 = animal_id + '_2'
        
        
    def load_two_analysis_files(self):
        animal_recording = [filename for filename in os.listdir(self.directory_path) if filename.startswith(self.animal_id)]
        os.chdir(self.directory_path)
        recording = np.load(animal_recording[0])
        brain_file_1 = [filename for filename in os.listdir(self.directory_path) if filename.endswith(self.start_1)]
        brain_state_1 = pd.read_pickle(brain_file_1[0])
        brain_file_2 = [filename for filename in os.listdir(self.directory_path) if filename.endswith(self.start_2)]
        brain_state_2 = pd.read_pickle(brain_file_2[0])
        return recording, brain_state_1, brain_state_2

    def load_one_analysis_file(self):
        animal_recording = [filename for filename in os.listdir(self.directory_path) if filename.startswith(self.animal_id)]
        os.chdir(self.directory_path)
        recording = np.load(animal_recording[0])
        brain_file_1 = [filename for filename in os.listdir(self.directory_path) if filename.endswith(self.start_1)]
        brain_state_1 = pd.read_pickle(brain_file_1[0])
        return recording, brain_state_1

    def get_one_start_time(self, start_times_dict):
        start_time_1 = start_times_dict[self.start_dict_1]
        start_time_2 = None
        return start_time_1

    def get_two_start_times(self, start_times_dict):
        start_time_1 = start_times_dict[self.start_dict_1]
        start_time_2 = start_times_dict[self.start_dict_2]
        return (start_time_1, start_time_2)


directory_path = '/home/melissa/preprocessing/numpyformat_baseline'
animal_1 = 'S7063'
test_prepare = PrepareFiles(directory_path=directory_path, animal_id=animal_1)
recording, brain_state_1, brain_state_2 = test_prepare.load_two_analysis_files()
start_time_1, start_time_2 = test_prepare.get_two_start_times(start_times_baseline)