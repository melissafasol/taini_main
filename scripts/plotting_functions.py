'''Created March 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file contains all functions needed in power_spectrum_plots.py'''

import numpy as np
import pandas as pd
import os 


'''function to check whether an element exists in a list'''
def check_availability(element, variables: iter):
    return element in variables

'''This function takes raw results csv file and removes unwanted columns and rows'''
def reformat_csv(csv_file_name):
    raw_csv = pd.read_csv(csv_file_name)
    reformat_rows = raw_csv[0:250]
    column_names = reformat_rows.columns
    for column in column_names:
        if column == 'Unnamed: 0':
            reformatted_file = reformat_rows.drop('Unnamed: 0', axis=1)
    
    return reformatted_file 


'''This function takes reformatted csv file and builds a dataframe which can be plotted with seaborn'''
def build_df_to_plot(reformatted_file):

    frequency_percolumn = []
    power_percolumn = []
    column_name = []
    animal_id = []

    column_names = reformatted_file.columns
    for column in column_names[1:]:
        for frequency, power in zip(reformatted_file['Frequency'], reformatted_file[column]):
            frequency_percolumn.append(frequency)
            power_percolumn.append(power)
            column_name.append(column[-7:])
            animal_id.append(column[2:7])

    results = pd.DataFrame({'Animal_ID': animal_id, 'Frequency': frequency_percolumn, 'Power': power_percolumn, 
                        'Channel': column_name}) 

    return results

'''This function takes dataframe and adds a column with genotypes to the dataframe'''
def build_genotype_df(results_dataframe):
    animal_numbers = results_dataframe['Animal_ID']
    animal_numbers = list(animal_numbers)
    
    genotype = []

    gaps = ['S7063', 'S7064', 'S7069', 'S7072', 'S7075', 'S7076', 'S7088', 'S7092', 'S7094', 'S7096']
    
    for animal in animal_numbers:
        if check_availability(animal, gaps) == True:
            genotype.append('GAP')
        else:
            genotype.append('WT')

    genotype_df = pd.DataFrame({'Genotype': genotype})
    
    final_dataframe = results_dataframe.join(genotype_df)
    
    return final_dataframe