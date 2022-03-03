'''Created March 2022
author: Melissa Fasol, University of Edinburgh
email: s1660428@ed.ac.uk

This file takes output of power script and reformats csv files into format suitable for plotting with seaborn and matplotlib'''

from copyreg import remove_extension
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import pickle
import scipy.stats as stats
import seaborn as sns

from plotting_functions import check_availability, build_df


#constants
from constants import wildtypes_animal_ids, gap_animal_ids


os.chdir('/home/melissa/Results/discarding_epoch_test')
REM_ETX = pd.read_csv('2_S7063_test_psd_ETX_2_brainfiles.csv')
nonREM_ETX = pd.read_csv('1_S7063_test_psd_ETX_2_brainfiles.csv')
wake_ETX = pd.read_csv('0_S7063_test_psd_ETX_2.csv')

REM_ETX = REM_ETX.iloc[0:250]
REM_ETX = REM_ETX.drop('Unnamed: 0', axis=1)
#REM_df = build_df(REM_ETX)
print(REM_ETX)

column_names = REM_ETX.columns

for i in column_names[1:]:
    print(i)

#build dataframe to separate animals by columns
#def build_df_columns(dataset):
 #   column_names = dataset.columns
  #  for column_name in column_names[1:]:
   #     print(column_name)
    #    for frequency, power in zip(dataset['Frequency'], dataset[column_name]):
    #        df = pd.DataFrame({'Channel': [column_name], 'Frequency': frequency, 'Power': power})
    

f, ax = plt.subplots(figsize=(10,6))
sns.set_style("white") 
sns.lineplot(x='Frequency', y='S7063_Chan4', dataset=REM_ETX)
sns.despine()
plt.yscale('log')
plt.xlim(0.2,49)
plt.ylim(10**-1, 10**2)
plt.legend(title = 'REM')
