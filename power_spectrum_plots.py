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

from plotting_functions import check_availability, reformat_csv, build_df_to_plot, build_genotype_df

#variables to change for each plot
savefig_name = "Channel_REM_ETX_2_brainstates.jpg"
plot_title = 'ETX_REM'


os.chdir('/home/melissa/Results/discarding_epoch_test')

f, ax = plt.subplots(figsize=(10,6))
sns.set_style("white") #hue='Channel_Number', ci=95
sns.lineplot(x='Frequency', y='Power', hue='Channel', ci=95, data = test)
sns.despine()
plt.yscale('log')
plt.xlim(1, 49)
plt.ylim(10**-1, 10**2)
plt.legend(title = "ETX REM", labels = ['chan4', 'chan7', 'chan10', 'chan11'])
plt.title("ETX REM")
plt.xlabel("Frequency (Hz)")
plt.ylabel('PSD [V**2/Hz]')
#gap should be blue and wildtype black
os.chdir('/home/melissa/Results/discarding_epoch_test/S7063_plots')
plt.savefig("Channel_REM_ETX_2_brainstates.jpg")