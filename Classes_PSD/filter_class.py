import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy 
from scipy import signal
from scipy.fft import fft, fftfreq

class FilterArtefactsOut(object):
    '''This class contains all functions required to filter out low-frequency drifts and frequencies above 100Hz
    timevalues_array = output of ExtractBrainstateTimes Class
    '''
    
    def __init__(self, raw_data, timevalues_array):
        self.raw_data = raw_data
        self.timevalues_array = timevalues_array
        self.lowcut = 1
        self.highcut = 100
        self.order_of_filter = 3
        self.sample_rate = 250.4
        self.nyquist_sr = 125.2
        self.low_nyq = (self.lowcut)/(self.nyquist_sr)
        self.high_nyq = (self.highcut)/(self.nyquist_sr)
        
        '''required coefficients for butter bandpass filter'''
        butter_b, butter_a = signal.butter(self.order_of_filter, [self.low_nyq, self.high_nyq], btype='band', analog = False)
        self.butter_b, self.butter_a = butter_b, butter_a
        
    def butter_bandpass_filter(self, raw_data):
        butter_y = signal.filtfilt(self.butter_b, self.butter_a, raw_data)
            
        filtered_data = signal.filtfilt(self.butter_b, self.butter_a, raw_data)

        return filtered_data
        
    def extract_time_filtered_data(self, timevalues_array, raw_data):
        '''this function extracts brainstate time values out of filtered data'''
        extracted_datavalues = []
        
        filtered_data = self.butter_bandpass_filter(raw_data)
        
        for i in range(len(timevalues_array)):
            start_epoch = timevalues_array[i]
            end_epoch = timevalues_array[i] + 1252
            extracted_datavalues.append(filtered_data[start_epoch:end_epoch])
            
        return extracted_datavalues
    
    def remove_noise(self, timevalues_array, raw_data):
        '''this function looks if any signal amplitude values exceed 3000mV and removes these epochs'''
        extracted_datavalues = self.extract_time_filtered_data(timevalues_array, raw_data)
        channel_threshold = []
        
        for i in range(len(extracted_datavalues)):
            for j in range(len(extracted_datavalues[i])):
                if extracted_datavalues[i][j] >= 3000:
                    channel_threshold.append(i)
                else:
                    pass
                    
        removing_duplicates = []
        for i in range(len(channel_threshold)):
            j = i + 1 
            if i == j:
                del[i]
            else:
                removing_duplicates.append(channel_threshold[i])
    
        channels_withoutnoise = [i for j, i in enumerate(extracted_datavalues) if j not in removing_duplicates]
        
        return channels_withoutnoise