import pandas as pd
import os
import numpy as np

start_times_S7096 = {'S7096_1': [34465057], 'S7096_2':[56099616],
                    'S7096_1A': [56054795], 'S7096_2A':[61102858],
                    'S7096_1B': [1], 'S7096_2B': [16586496]}

def concatenate_S7096(path, channel_number, animal_number, start_times_S7096):
    start_1 = 'S7096_1'
    end_1 = 'S7096_2'
    start_1A = 'S7096_1A'
    end_1A = 'S7096_2A'
    start_1B = 'S7096_1B'
    end_1B = 'S7096_2B'

    files = []

    for r, d, f in os.walk(path):
        for file in f:
            if animal_number in file:
                files.append(os.path.join(r, file))

    print(files)

    for recording in files:
        if recording.endswith('S7096_A.npy'):
            numpy_A = np.load(recording)
        if recording.endswith('S7096_B.npy'):
            numpy_B = np.load(recording)          

    for animal_id in start_times_S7096:
        if animal_id == start_1:
            start_1 = start_times_S7096[animal_id]
        elif animal_id == end_1:
            end_1 = start_times_S7096[animal_id]
        elif animal_id == start_1A:
            start_2 = start_times_S7096[animal_id]
        elif animal_id == end_1A:
            end_2 = start_times_S7096[animal_id]
        elif animal_id == start_1B:
            start_3 = start_times_S7096[animal_id]
        elif animal_id == end_1B:
            end_3 = start_times_S7096[animal_id]

    start_1 = int(start_1)
    end_1 = int(end_1)
    start_2 = int(start_2)
    end_2 = int(end_2)
    start_3 = int(start_3)
    end_3 = int(end_3)

    recording_1 = numpy_A[channel_number, start_1:end_1]
    recording_2 = numpy_A[channel_number, start_2:end_2]
    recording_3 = numpy_B[channel_number, start_3:end_3]

    baseline_1 = recording_1
    baseline_2 = np.concatenate((recording_2, recording_3))

    for brain_state_file in files:
        if brain_state_file.endswith('A.pkl'):
            brain_state_A = pd.read_pickle(brain_state_file)
        elif brain_state_file.endswith('B.pkl'):
            brain_state_B = pd.read_pickle(brain_state_file)

    return baseline_1, baseline_2, brain_state_A, brain_state_B
