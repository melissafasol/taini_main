'''this file applies functions in psd_taini_mainfunctions.py to all datasets'''
from psd_taini_mainfunctions import load_analysis_files, get_start_times, load_recording_from_start
import Individual_Recording_Conditions.saline_functions
import Individual_Recording_Conditions.ETX_functions
from constants import baseline_recording_dictionary, start_times_baseline
import save_functions

#other required imports 
import pandas as pd 
import os
import numpy 
import mne 
import matplotlib.pyplot as plt
import scipy
from scipy.fft import fft, fftfreq
from scipy import signal
import re
import statistics
from pandas import ExcelWriter
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average

directory_path = '/home/melissa/preprocessing/numpyformat_baseline'

for animal in baseline_recording_dictionary['animal_two_brainstates']:
    recording, brain_state_1, brain_state_2 = load_analysis_files(directory_path, animal)
    start_time_1, start_time_2 = get_start_times(start_times_baseline, animal)
    data_1, data_2 = load_recording_from_start(recording, 4, start_time_1, start_time_2)
    print(data_1)