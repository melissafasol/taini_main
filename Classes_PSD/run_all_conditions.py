##all required imports 
import pandas as pd
import os
import numpy as np
import mne
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy
from scipy import signal
import re

from preparefiles import PrepareFiles
from load_recording import LoadRecording
os.chdir('/home/melissa/taini_main')
from constants import baseline_recording_dictionary, saline_recording_dictionary, ETX_recording_dictionary, start_times_baseline, start_times_saline, start_times_ETX
import save_functions


recording_condition = ['baseline', 'saline', 'ETX']
brainstates = [2]
channel_numbers = [4,7,10,11]

for animal in baseline_recording_dictionary['animal_two_brainstates']:
    for channel in channel_numbers:
        for brain_state in brainstates:
            baseline_1brst_files = PrepareFiles(baseline_recording_dictionary['path'], animal, channel, start_times_baseline) 
            raw_recording, brain_state_1, brain_state_2 = baseline_1brst_files.get_data_files()
            start_time_1, start_time_2 = baseline_1brst_files.get_start_time()
            prepared_recording = LoadRecording(raw_recording, brain_state_1, brain_state_2, start_time_1, start_time_2, channel)
            baseline_recording = prepared_recording.get_prepared_recording()

