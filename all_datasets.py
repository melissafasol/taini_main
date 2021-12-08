'''this file applies functions in psd_taini_mainfunctions.py to all datasets'''

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average
from psd_taini_mainfunctions import loading_analysis_files, brainstate_times, highpass, channel_data_extraction, loading_analysis_files_onebrainstate, looking_for_outliers, remove_noise, psd_per_channel, psd_average
from psd_taini_mainfunctions import starting_times_dict, channels_dict, genotype_per_animal

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

path = '/home/melissa/preprocessing/numpyformat'

animal_number_two_brainstates = ['S7063', 'S7064', 'S7069', 'S7070', 'S7071', 'S7083', 'S7086', 'S7091', 'S7092', 'S7098', 'S7101']
animal_number_one_brainstate = ['S7068', 'S7072', 'S7074', 'S7075', 'S7076', 'S7088', 'S7094']
channel_number = 9

print(len(animal_number_two_brainstates))
print(len(animal_number_one_brainstate))

'all empty lists below'
small_dfs_two_brainstates = []
slopegradient_intercept =[]

for i in range(len(animal_number_two_brainstates)-1):
    animal_number = animal_number_two_brainstates[i]
    print(animal_number)
    data_baseline1, data_baseline2, brain_state_1, brain_state_2, time_1, time_2 = loading_analysis_files(path, animal_number, starting_times_dict, channel_number)
    REM_1_timevalues = brainstate_times(brain_state_1, 2)
    REM_2_timevalues = brainstate_times(brain_state_2, 2)
    REM_1_filtered = highpass(data_baseline1)
    REM_2_filtered = highpass(data_baseline2)
    REM_1_datavalues = channel_data_extraction(REM_1_timevalues, REM_1_filtered)
    REM_2_datavalues = channel_data_extraction(REM_2_timevalues, REM_2_filtered)
    REM_1_withoutartifacts = remove_noise(REM_1_datavalues)
    REM_2_withoutartifacts = remove_noise(REM_2_datavalues)
    psd_REM_1, frequency = psd_per_channel(REM_1_withoutartifacts)
    psd_REM_2, frequency = psd_per_channel(REM_2_withoutartifacts)
    intercept_slope = looking_for_outliers(psd_REM_1, frequency)
    slopegradient_intercept.append([animal_number, intercept_slope])
    intercept_slope_2 = looking_for_outliers(psd_REM_2, frequency)
    slopegradient_intercept.append([animal_number, intercept_slope_2])
    psd_average_1 = psd_average(psd_REM_1, frequency, animal_number)
    list_mean_1 = list(psd_average_1)
    print(list_mean_1)
    psd_average_2 = psd_average(psd_REM_2, frequency, animal_number)
    list_mean_2 = list(psd_average_2)
    
     
    for x in genotype_per_animal:
        if x == animal_number:
            genotype = genotype_per_animal[x]
    print(genotype)

    sleepstate = ['REM']
    recordingtype = ['baseline']
    results = {'Animal_Number':[animal_number]*627, 'Genotype':genotype*627, 
    'Sleep_State' : sleepstate*627, 'Recording_Type': recordingtype*627,
    'Frequency': frequency, 'Power_1': list_mean_1, 'Power_2': list_mean_2}

    df_1 = pd.DataFrame(data = results)
    col = df_1.loc[:, "Power_1":"Power_2"]
    df_1["Power"] = col.mean(axis = 1)
    average_p = df_1.loc[:, "Power"]
    print(average_p)
    df_1.drop(["Power_1", "Power_2"], axis = 1, inplace=True)
    fig = plt.figure()
    plt.semilogy(frequency, average_p)
    plt.xlabel('frequency [Hz]')
    plt.xlim(1,100)
    plt.ylim(10**-3, 10**4)
    plt.ylabel('Power spectrum')
    fig.suptitle(animal_number)
    os.chdir('/home/melissa/psd_plots_december21')
    fig.savefig(animal_number + 'average')
    plt.show()
    small_dfs_two_brainstates.append(df_1)
    animal_number = [i+1]
    

#last animal not included in loop
animal_number = animal_number_two_brainstates[-1]
data_baseline1, data_baseline2, brain_state_1, brain_state_2, time_1, time_2 = loading_analysis_files(path, animal_number, starting_times_dict, channel_number)
REM_1_timevalues = brainstate_times(brain_state_1, 2)
REM_2_timevalues = brainstate_times(brain_state_2, 2)
REM_1_filtered = highpass(data_baseline1)
REM_2_filtered = highpass(data_baseline2)
REM_1_datavalues = channel_data_extraction(REM_1_timevalues, REM_1_filtered)
REM_2_datavalues = channel_data_extraction(REM_2_timevalues, REM_2_filtered)
REM_1_withoutartifacts = remove_noise(REM_1_datavalues)
REM_2_withoutartifacts = remove_noise(REM_2_datavalues)
psd_REM_1, frequency = psd_per_channel(REM_1_withoutartifacts)
psd_REM_2, frequency = psd_per_channel(REM_2_withoutartifacts)
intercept_slope = looking_for_outliers(psd_REM_1, frequency)
slopegradient_intercept.append([animal_number, intercept_slope])
intercept_slope_2 = looking_for_outliers(psd_REM_2, frequency)
slopegradient_intercept.append([animal_number, intercept_slope_2])
psd_average_1 = psd_average(psd_REM_1, frequency, animal_number)
list_mean_1 = list(psd_average_1)
psd_average_2 = psd_average(psd_REM_2, frequency, animal_number)
list_mean_2 = list(psd_average_2)
    
for x in genotype_per_animal:
    if x == animal_number:
        genotype = genotype_per_animal[x]
print(genotype)

sleepstate = ['REM']
recordingtype = ['baseline']
results = {'Animal_Number':[animal_number]*627, 'Genotype':genotype*627, 
           'Sleep_State' : sleepstate*627, 'Recording_Type': recordingtype*627,
           'Frequency': frequency, 'Power_1': list_mean_1, 'Power_2': list_mean_2}

df_lastvalue = pd.DataFrame(data = results)
col = df_lastvalue.loc[:, "Power_1":"Power_2"]
df_lastvalue["Power"] = col.mean(axis = 1)
average_p = df_lastvalue.loc[:, "Power"]
df_lastvalue.drop(["Power_1", "Power_2"], axis = 1, inplace=True)
fig = plt.figure()
plt.semilogy(frequency, average_p)
plt.xlabel('frequency [Hz]')
plt.xlim(0,100)
plt.ylim(10**-3, 10**4)
plt.ylabel('Power spectrum')
fig.suptitle(animal_number)
os.chdir('/home/melissa/psd_plots_december21')
fig.savefig(animal_number + 'average')
plt.show()
small_dfs_two_brainstates.append(df_lastvalue)


small_dfs_one_brainstate = []

for i in range(len(animal_number_one_brainstate)-1):
    animal_number = animal_number_one_brainstate[i]
    data_baseline1, brain_state_1, time_1 = loading_analysis_files_onebrainstate(path, animal_number, starting_times_dict, channel_number)
    REM_1_timevalues = brainstate_times(brain_state_1, 2)
    REM_1_filtered = highpass(data_baseline1)
    REM_1_datavalues = channel_data_extraction(REM_1_timevalues, REM_1_filtered)
    REM_1_withoutartifacts = remove_noise(REM_1_datavalues)
    psd_REM_1, frequency = psd_per_channel(REM_1_withoutartifacts)
    intercept_slope = looking_for_outliers(psd_REM_1, frequency)
    slopegradient_intercept.append([animal_number, intercept_slope])
    psd_average_1 = psd_average(psd_REM_1, frequency, animal_number)
    list_average_1 = list(psd_average_1)
    
    for x in genotype_per_animal:
        if x == animal_number:
            genotype = genotype_per_animal[x]
    print(genotype)

    sleepstate = ['REM']
    recordingtype = ['baseline']
    results = {'Animal_Number':[animal_number]*627, 'Genotype':genotype*627, 
    'Sleep_State' : sleepstate*627, 'Recording_Type': recordingtype*627,
    'Frequency': frequency, 'Power_1': list_mean_1}

    df_2 = pd.DataFrame(data = results)
    small_dfs_one_brainstate.append(df_2)
    animal_number = [i+1]


animal_number = animal_number_one_brainstate[-1]
print(animal_number)
data_baseline1, brain_state_1, time_1 = loading_analysis_files_onebrainstate(path, animal_number, starting_times_dict, channel_number)
REM_1_timevalues = brainstate_times(brain_state_1, 2)
REM_1_filtered = highpass(data_baseline1)
REM_1_datavalues = channel_data_extraction(REM_1_timevalues, REM_1_filtered)
REM_1_withoutartifacts = remove_noise(REM_1_datavalues)
psd_REM_1, frequency = psd_per_channel(REM_1_withoutartifacts)
intercept_slope = looking_for_outliers(psd_REM_1, frequency)
slopegradient_intercept.append([animal_number, intercept_slope])
psd_average_1 = psd_average(psd_REM_1, frequency, animal_number)
list_average_1 = list(psd_average_1)

for x in genotype_per_animal:
    if x == animal_number:
        genotype = genotype_per_animal[x]
print(genotype)

sleepstate = ['REM']
recordingtype = ['baseline'] 
results = {'Animal_Number':[animal_number]*627, 'Genotype':genotype*627, 
'Sleep_State' : sleepstate*627, 'Recording_Type': recordingtype*627,
'Frequency': frequency, 'Power_1': list_mean_1}

df_lastvalue = pd.DataFrame(data = results)
small_dfs_one_brainstate.append(df_lastvalue)


'''checking last df is the last animal in list'''
print(len(small_dfs_one_brainstate))
print(len(small_dfs_two_brainstates))
print(slopegradient_intercept)
os.chdir('/home/melissa/preprocessing')
numpy.save(channel_number + 'channel_number_slope_intercepts_gradient', slopegradient_intercept)

large_dfs_two_brainstates = pd.concat([small_dfs_two_brainstates[0], small_dfs_two_brainstates[1],
                                      small_dfs_two_brainstates[2], small_dfs_two_brainstates[3],
                                      small_dfs_two_brainstates[4], small_dfs_two_brainstates[5],
                                      small_dfs_two_brainstates[6], small_dfs_two_brainstates[7],
                                      small_dfs_two_brainstates[8], small_dfs_two_brainstates[9],
                                      small_dfs_two_brainstates[10]], ignore_index=True)
 

large_dfs_one_brainstate = pd.concat([small_dfs_one_brainstate[0], small_dfs_one_brainstate[1],
                                    small_dfs_one_brainstate[2], small_dfs_one_brainstate[3],
                                    small_dfs_one_brainstate[4], small_dfs_one_brainstate[5],
                                    small_dfs_one_brainstate[6]],ignore_index=True)

os.chdir('/home/melissa/all_taini_melissa/')
large_dfs_one_brainstate.to_pickle('one_mean_REM.pkl')
large_dfs_two_brainstates.to_pickle('two_mean_REM.pkl')






