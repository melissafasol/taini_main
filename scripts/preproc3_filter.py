import scipy
from scipy.fft import fft, fftfreq
from scipy import signal

'''apply scipy butterworth bandpass filter and remove epochs with amplitudes larger than 3000mV'''

class Filter:
    
    order = 3
    sampling_rate = 250.4
    nyquist = 125.2
    low = 0.2/nyquist
    high = 100/nyquist
    noise_limit = 3000
    epoch_bins = 1252 #5 seconds * sampling rate
    
    def __init__(self, unfiltered_data, timevalues_array):
        self.unfiltered_data = unfiltered_data
        self.timevalues_array = timevalues_array
        self.extracted_datavalues = []
        self.channel_threshold = []
        
    '''filter out low-frequency drifts and frequencies above 50Hz'''
    
    def butter_bandpass(self):
        butter_b, butter_a = signal.butter(self.order, [self.low, self.high], btype='band', analog = False)
        
        filtered_data = signal.filtfilt(butter_b, butter_a, self.unfiltered_data)

        for timevalue in range(len(self.timevalues_array)):
            start_time_bin = self.timevalues_array[timevalue] 
            end_time_bin = self.timevalues_array[timevalue] + self.epoch_bins
            self.extracted_datavalues.append(filtered_data[start_time_bin: end_time_bin])
            
        for i in range(len(self.extracted_datavalues)):
            for j in range(len(self.extracted_datavalues[i])):
                if self.extracted_datavalues[i][j] >= self.noise_limit:
                    self.channel_threshold.append(i)
                else:
                    pass

        remove_duplicates = sorted(list(set(self.channel_threshold)))
        channels_without_noise = [i for j, i in enumerate(self.extracted_datavalues) if j not in remove_duplicates]
        return channels_without_noise 