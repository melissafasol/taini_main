'''This file is to plot histograms of the gradient and y-intercept of spectral slopes to see
whether they are unimodally or bimodally distributed and use this as a guide to set outlier thresholds''' 

#all required imports 
import pandas as pd
import os
import numpy as np
import mne
import matplotlib
import seaborn as sns

import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from math import pi 

def prepare_file(csv_file_path):
    slope_intercept_df = pd.read_csv(csv_file_path)
    if 'Unnamed: 0' in  slope_intercept_df.columns:
         slope_intercept_df =  slope_intercept_df.drop('Unnamed: 0', axis = 1)
    else:
        pass
    #mean_values = [np.mean( slope_intercept_df[column]) for column in slope_intercept_df]
    #column_names = [str(column) for column in  slope_intercept_df]
    #mean_df = pd.DataFrame([dict(zip(column_names, mean_values))])
    return slope_intercept_df


def build_df_distribution_histogram(reformatted_file):
    
    gradient_df = []
    intercept_df = []

    column_names = reformatted_file.columns
    for column in column_names:
            if column[-5:] == 'slope':
                length_slope = len(reformatted_file[column])
                df = pd.DataFrame(data = {'Slope': reformatted_file[column], 'Animal_Number': column[2:7]})
                gradient_df.append(df)
            else:
                length_intercept = len(reformatted_file[column])
                df = pd.DataFrame(data = {'Intercept': reformatted_file[column], 'Animal_Number': column[2:7]})
                intercept_df.append(df)
    
    
    concatenated_gradient_df = pd.concat(gradient_df)
    concatenated_intercept_df = pd.concat(intercept_df)
    
    return concatenated_gradient_df, concatenated_intercept_df

#loop through both dataframes and separate to mutant and wildtypes

def separate_by_genotype(large_df):
    
    wildtypes = ['S7068', 'S7070', 'S7071', 'S7074', 'S7086', 'S7087', 'S7091', 'S7098', 'S7101']
    gaps = ['S7063', 'S7064', 'S7069', 'S7072', 'S7075', 'S7076', 'S7088', 'S7092', 'S7094', 'S7096']
    
    wildtype_intersection = set(large_df['Animal_Number']).intersection(wildtypes)
    wildtype_list = list(wildtype_intersection)
    gap_intersection = set(large_df['Animal_Number']).intersection(gaps)
    gap_list = list(gap_intersection)
    
    wildtype_df = []
    gap_df = []
    
    for animal in large_df['Animal_Number']:
        if animal == animal in wildtype_list:
            wildtype_df.append(large_df.loc[large_df['Animal_Number'] == str(animal)])
        if animal == animal in gap_list:
            gap_df.append(large_df.loc[large_df['Animal_Number'] == str(animal)])
    
    return wildtype_df, gap_df

def concatenate_genotype_output(wt_to_concat, gap_to_concat):
    wildtype_df = pd.concat(wt_to_concat)
    gap_df = pd.concat(gap_to_concat)
    
    return wildtype_df, gap_df


def hof_spectral_slope_histogram(working_directory, csv_file_path):
    os.chdir(working_directory)
    mean_df = prepare_file(csv_file_path)
    concatenated_gradient_df, concatenated_intercept_df = build_df_distribution_histogram(mean_df)
    wildtype_gradient_large_df, gap_gradient_large_df = separate_by_genotype(concatenated_gradient_df)
    wildtype_intercept__large_df, gap_intercept_large_df = separate_by_genotype(concatenated_intercept_df)
    wildtype_gradient_df, gap_gradient_df = concatenate_genotype_output(wildtype_gradient_large_df, gap_gradient_large_df)
    wildtype_intercept_df, gap_intercept_df = concatenate_genotype_output(wildtype_intercept__large_df, gap_intercept_large_df)
    return wildtype_gradient_df, gap_gradient_df, wildtype_intercept_df, gap_intercept_df