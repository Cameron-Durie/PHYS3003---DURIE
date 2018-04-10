#! /usr/bin/env python

"""
Functions for Matching program

"""

__author__= "Cameron Durie"

# import
import numpy as np
import csv
import math
import time
import glob,os

from cluster import sky_dist, regroup, dist_3d, best_dist
from catalogs import write_catalog, write_table, table_to_source_list
from astropy.table import vstack, table

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')



def retrieve_data(folder, number):

    """
    
    
    """

    files = []  # To store list of target csv files
    epoch = 0

    os.chdir("%s" % folder)
    for file in glob.glob("*.csv"):
        if epoch < number:
            files.append(file)
            epoch += 1
        else:
            break
    print(files)
    epoch = 0

    # load tables
    for filename in files:
        tab = table.Table.read("%s" % filename)

        # rename columns
        tab.rename_column("# src", "source")
        tab.rename_column("RA(deg)", "ra")
        tab.rename_column("err_RA(deg)", "err_ra")
        tab.rename_column("Dec(deg)", "dec")
        tab.rename_column("err_Dec(deg)", "err_dec")
        tab.rename_column("Flux(Jy)", "peak_flux")
        tab.rename_column("err_Flux(Jy)", "err_peak_flux")

        # add epoch column
        tab['island'] = epoch

        if epoch == 0:
            frames = tab
        else:
            frames = vstack([frames, tab])
        epoch += 1

    print(frames)
    write_table(frames, "./results/frames%d.csv" % number)

    cat = table_to_source_list(frames)
    print(cat)

    return cat



def process_regrouping(cat, number, length, eps, stage, dist_func, successes):
    """


    """

    regroup_start_time = time.time()  # record start time

    islands = regroup(cat, eps, far=None, dist=dist_func)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == number:
            successes += 1
            goodies.append(islands[i])
        else:
            badies.extend(islands[i])

    goodies = sorted(goodies)

    for i in range(len(goodies)):
        print(goodies[i])

    goodies = np.ravel(goodies)
    badies = np.ravel(badies)

    badies = sorted(badies)

    write_catalog("./results/goodies/%d_epochs/goodies_%s_%depochs" % (number, stage, number), goodies, fmt='csv')
    write_catalog("./results/badies/%d_epochs/badies_%s_%depochs" %(number, stage, number), badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)

    percentage_solved = 100 * (successes*number) / (length)
    print("\nSuccess rate = %f%%" % percentage_solved)

    run_time = (time.time() - regroup_start_time)
    print("%s  --- %f seconds ---" % (stage, run_time))

    return {'goodies': goodies, 'badies': badies, 'success': successes, 'percentage_solved':  percentage_solved, 'time': run_time}