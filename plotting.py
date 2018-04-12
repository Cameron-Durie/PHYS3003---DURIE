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

    print(island)

    for i in range(len(island)):
        x.extend(island[i].island)
        y.extend(island[i].peak_flux)

    df = pd.DataFrame({'epoch': x, 'peak_flux': y})

    print(x)
    print(y)

    plt.plot('epoch','peak_flux', data=df, maker= 'o', color='red')
    savefig('./results/plots/%s/plot%d.png' %(stage, num), bbox_inches='tight')
