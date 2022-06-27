class ETXPrepare2Files:
    
    '''class for two ETX files, if only one file then just use parent prepare file'''
    
    def __init__(self, directory_path, animal_id, start_time_dict, channel_number):
        self.directory_path = directory_path
        self.animal_id = animal_id
        self.start_time_dict = start_time_dict
        self.channel_number = channel_number
        self.end_A = 'ETX_A.npy'
        self.end_B = 'ETX_B.npy'
        self.start_dict_1A = animal_id + '_1A'
        self.end_dict_1A = animal_id + '_2A'
        self.start_dict_1B = animal_id + '_1B'
        self.end_dict_1B = animal_id + '_2B'
        self.brain_state_file = animal_id + '.pkl'
        self.files = []
        
    def load_ETX_two(self):
        os.chdir(self.directory_path)
        animal_recording_A = [filename for filename in os.listdir(self.directory_path) if filename.startswith(self.animal_id) and filename.endswith(self.end_A)]
        animal_recording_B = [filename for filename in os.listdir(self.directory_path) if filename.startswith(self.animal_id) and filename.endswith(self.end_B)]
        recording_A = np.load(animal_recording_A[0])
        recording_B = np.load(animal_recording_B[0])
        
        for dict_id in self.start_time_dict:
            if dict_id == self.start_dict_1A:
                start_1 = int(self.start_time_dict[dict_id])
            elif dict_id == self.end_dict_1A:
                end_1 = int(self.start_time_dict[dict_id])
            elif dict_id == self.start_dict_1B:
                start_2 = int(self.start_time_dict[dict_id])
            elif dict_id == self.end_dict_1B:
                end_2 = int(self.start_time_dict[dict_id])
                
        recording_1 = recording_A[self.channel_number, start_1: end_1]
        recording_1 = np.array(recording_1)
        recording_2 = recording_B[self.channel_number, start_2: end_2]
        recording_2 = np.array(recording_2)
        
        concatenate_recordings = np.concatenate([recording_1, recording_2], axis=0)
        brain_state = pd.read_pickle(self.brain_state_file)
        
        return concatenate_recordings, brain_state

class SalinePrepare2Files(ETXPrepare2Files):
    
    def __init__(self, directory_path, animal_id, start_time_dict, channel_number):
        super().__init__(directory_path, animal_id, start_time_dict, channel_number)
        self.end_A = 'saline_1A.npy'
        self.end_B = 'saline_1B.npy'
        self.start_dict_1A = animal_id + '_1A'
        self.end_dict_1A = animal_id + '_2A'
        self.start_dict_1B = animal_id + '_1B'
        self.end_dict_1B = animal_id + '_2B'
        self.brain_state_file = animal_id + '.pkl'
        self.files = []