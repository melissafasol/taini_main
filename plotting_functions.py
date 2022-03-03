'''Created March 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all functions needed in power_spectrum_plots.py'''

import numpy as np
import pandas as pd
import os 


'''simple function to prepare csv file for plotting'''
def build_df_data(animal_ids, datafile, is_wild=False):
    for animal_id in animal_ids:
        for frequency, power in zip(datafile['Frequency'], datafile[animal_id]):
            df_data = pd.DataFrame({'animal_id': animal_id, 'frequency': frequency, 'power':power, 'is_wild': is_wild})


def check_availability(element, variables: iter):
    return element in variables


def build_df(datafile):
    '''function takes power csv file and reformats it into pd.DataFrame to plot with pandas'''
    animal_ids = ['S7063','S7064', 'S7068', 'S7069', 'S7072', 'S7088', 'S7094', 'S7096','S7070', 'S7071', 'S7075', 'S7076', 'S7083', 'S7086', 'S7087','S7092', 'S7098', 'S7101', 'S7074', 'S7091']
    channels = ['n4', 'n7', '10', '11']
    animal_number = []
    channel_number = []

    #wildtypes = ['S7068', 'S7070', 'S7071', 'S7074', 'S7086', 'S7087', 'S7091', 'S7098', 'S7101']
    gaps = ['S7063', 'S7064', 'S7069', 'S7072', 'S7075', 'S7076', 'S7088', 'S7092', 'S7094', 'S7096']
    genotype = []
    frequency = []
    power = []

    column_names = datafile.columns

    #animal_id
    for column in range(len(column_names)):
        str_column = str(column)
        for animal in animal_ids:
            if column.startswith(animal):
                animal_number.append([animal]*250)
                frequency.append(datafile.loc[:,'Frequency'])
                power.append(datafile.loc[:,column])
                if check_availability(animal, gaps) == True:
                    genotype.append(["GAP"]*250)
                else:
                    genotype.append(["WT"]*250)
            for channel in channels:
                if str_column[-2:] == channel:
                    channel_number.append([channel])

        animal_number = [item for sublist in animal_number for item in sublist]
        channel_number =  [item for sublist in channel_number for item in sublist]
        print(channel_number)

        print(len(animal_number))
        print(len(channel_number))
        print(len(genotype))
        print(len(frequency))
        print(len(power))

        results_dataframe = pd.DataFrame({'Animal_ID':animal_number, 'Channel_Number': channel_number, 'Genotype': genotype, 'Frequency': frequency, 'Power': power})
