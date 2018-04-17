#! /usr/bin/env python

"""
Plotting light curves

"""

__author__= "Cameron Durie"

# import
from matplotlib import pyplot as plt

import pandas as pd


# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def light_curve(island, stage, num):

    x = []
    y = []
    flux_error = []

    for i in range(len(island)):
        x.append(island[i].island)
        y.append(island[i].peak_flux)
        flux_error.append(island[i].err_peak_flux)

    which_src = island[0].source
    df = pd.DataFrame({'epoch': x, 'peak_flux': y})

    plt.plot('epoch','peak_flux', data=df, marker= 'o', color='red')
    plt.xlabel('Epoch')
    plt.ylabel('peak_flux')
    plt.ylim(0, y[1]+1)

    plt.suptitle('Light Curve %d' %which_src)
    plt.savefig('./results/plots/%d_epochs/%s/plot_%d.png' %(num, stage, which_src))
    plt.gcf().clear()


def multigroup_plot(island, stage, num, group_size):
    """

    """
    x = []
    y = []
    flux_error = []

    for i in range(len(island)):
        x.append(island[i].island)
        y.append(island[i].peak_flux)
        flux_error.append(island[i].err_peak_flux)

    which_srcs = []
    for k in range(group_size):
        which_srcs.append(island[k].source)
    plot_name = str(which_srcs).strip('[]')

    df = pd.DataFrame({'epoch': x, 'peak_flux': y})

    plt.plot('epoch', 'peak_flux', data=df, linestyle='none', marker='o', color='red')
    plt.xlabel('Epoch')
    plt.ylabel('peak_flux')
    plt.ylim(0, max(y[0],y[1],y[2],y[3]) + 1)

    plt.suptitle('Light Curve %s' % plot_name)
    plt.savefig('./results/plots/%d_epochs/%s/multiplot_%s.png' % (num, stage, plot_name))
    plt.gcf().clear()
