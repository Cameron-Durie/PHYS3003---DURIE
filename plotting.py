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

    for i in range(len(island)):
        x.append(island[i].island)
        y.append(island[i].peak_flux)

    which_src = island[0].source
    df = pd.DataFrame({'epoch': x, 'peak_flux': y})

    plt.plot('epoch','peak_flux', data=df, marker= 'o', color='red')
    plt.savefig('./results/plots/%d_epochs/%s/plot_%d.png' %(num, stage, which_src), bbox_inches='tight')
    plt.gcf().clear()