#! /usr/bin/env python

"""
Matching program using Argean Tools

"""

__author__= "Cameron Durie"

# import
import numpy as np
import math
import time
import glob,os

from cluster import sky_dist, regroup, dist_3d
from catalogs import write_catalog, write_table, table_to_source_list
from astropy.table import vstack, table

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def main():

    # record start time
    start_time = time.time()

    hmany = 3  # How many csv files to load


    folder = './Data_set_2_small/'  # Target folder for extracting csv files


    files = []  # To store list of target csv files
    epoch = 0

    os.chdir("%s" %folder)
    for file in glob.glob("*.csv"):
        if epoch < hmany:
            files.append(file)
            epoch += 1
        else:
            break
    print(files)

    epoch = 0

    # load tables
    for filename in files:
        tab = table.Table.read("%s" %filename)

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
            epoch += 1
        else:
            frames = vstack([frames, tab])
            epoch += 1

    print(frames)
    write_table(frames,"./results/frames1.csv")

    cat = table_to_source_list(frames)
    print(cat)

    # Data_set_2_small
    # for 2 epochs eps =  1.7  for dist_3d,  eps =  0.112  for sky_dist --> 64.36% ,  64.36% (dist_3d was quicker:  0.068sec vs. 0.80sec)
    # for 25 epochs eps = 1.9  for dist 3d,  eps =  0.09  for sky dist  --> 47.52% ,  39.60% (dist 3d was quicker:  0.933sec vs. 1.86sec)
    # for 50 epochs eps = 1.72 for dist_3d,  eps =  0.112  for sky_dist --> 50.495% , 34.653% (dist_3d was quicker: 2.185sec vs. 5.792sec


    islands = regroup(cat, 1.72, far=None, dist=dist_3d)
    print(islands)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" %total_count)

    goodies = []
    successes = 0

    for i in range(len(islands)):
        if len(islands[i]) == hmany:
            successes += 1
            islands[i] = sorted(islands[i])
            goodies.append(islands[i])

    goodies = sorted(goodies)


    for i in range(len(goodies)):
        print(goodies[i])
    goodies = np.ravel(goodies)
    print(type(goodies[i]))
    write_catalog("./results/goodies",goodies, fmt='csv')

    percentage_solved = 100*(successes)/(len(tab))
    print("\nSuccess rate = %f%%" %percentage_solved)

    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    main()

