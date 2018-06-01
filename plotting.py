#! /usr/bin/env python

"""
Plotting light curves for Matching program.

"""

__author__= "Cameron Durie"

# import
from matplotlib import pyplot as plt
from catalogs import write_catalog


# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def light_curve(island, stage, num):
    """
    Plot the light for a inputted group.

    :param island: The group of sources that have been associated and deemed good.
    :param stage: The name of the current stage.
    :param num: The number of epochs included.

    :return: Nothing. Only plots light curve and generates group csv.
    """

    x = []
    y = []
    flux_error = []

    for i in range(len(island)):
        x.append(island[i].island)
        y.append(island[i].peak_flux)
        flux_error.append(island[i].err_peak_flux)

    which_src = island[0].source
    which_first_island = island[0].island
    plt.errorbar(x,y, yerr=flux_error,  marker= 'o', color='red', ecolor='blue', capsize=2, elinewidth=1)
    plt.xlabel('Epoch number')
    plt.ylabel('peak_flux (Jy)')
    plt.xlim(-1, num)
    plt.ylim(0, y[0]+1)

    plt.suptitle('Light Curve %d' %which_src)
    plt.savefig('./results/plots/%d_epochs/%s/plot_%d - %d.png' %(num, stage, which_src, which_first_island))
    plt.gcf().clear()

    write_catalog('./results/plots/%d_epochs/%s/plot_%d - %d.csv' %(num, stage, which_src, which_first_island), island, fmt='csv');


def multigroup_plot(island, stage, num, group_size):
    """
    Plot the combined light curve of multiple objects.

    :param island: The combined catalogue of sources for multiple sources.
    :param stage: The name of the current stage.
    :param num: The number of epochs included.
    :param group_size: Number of objects included in the multi plot.

    :return: Nothing. Only plots combined light curve and generates multi-group csv.
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

    if (len(island)/num)<30:
        plot_name = str(which_srcs).strip('[]')
    else:
        plot_name = str(len(island))

    plt.plot(x, y, linestyle='none', marker='o', color='red')
    plt.xlabel('Epoch number')
    plt.ylabel('peak_flux (Jy)')
    plt.xlim(-1, num)
    plt.ylim(0, max(y[0],y[1],y[2],y[3]) + 2)

    plt.suptitle('Light Curve %s' % plot_name)
    plt.savefig('./results/plots/%d_epochs/%s/multiplot_%s.png' % (num, stage, plot_name))
    plt.gcf().clear()

    write_catalog('./results/plots/%d_epochs/%s/plot_%s.csv' % (num, stage, plot_name), island, fmt='csv');
