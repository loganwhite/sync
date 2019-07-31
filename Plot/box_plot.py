#!/usr/local/bin/python3

import matplotlib
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter, MultipleLocator
import os
import matplotlib.pylab as pylab

from matplotlib.ticker import FormatStrFormatter

COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf']

font_size = '12'
params = {
		'axes.labelsize' : font_size,
		'xtick.labelsize' : font_size,
		'ytick.labelsize' : font_size,
		# 'lines.linewidth' : '0.2',
		'legend.fontsize' : font_size,
		'figure.figsize' : '4, 2.8',
	}
pylab.rcParams.update(params)




def plot_util_box():



    plt.close('all')
    fig = plt.figure(figsize=(3.5, 2.5))
    # ax2 = ax.twinx()
    ax = fig.add_subplot(111)

	
    filename = filename
    # matplotlib2tikz.save("{}.tex".format(filename))

    ax.xlabel('')
    ax.ylabel('Link Utilization (\%)')
    
    plt.savefig('{}.pdf'.format(filename), format='pdf', dpi=900)

    plt.show()

plot_util_box()

