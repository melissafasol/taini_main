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

import Classes_PSD.load_rec_brainstate_files

file_path = '/home/melissa/preprocessing/numpyformat_baseline'
animal_number = 'S7068'
channel = 4 

Classes_PSD.load_rec_brainstate_files.LoadRecAndBrainFiles.get_data_files(file_path, animal_number, channel)