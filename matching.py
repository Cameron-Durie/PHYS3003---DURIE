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

    hmany = 70  # How many csv files to load


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


    # load tables and rename colomns
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

        print(tab)






    frames = vstack([tab0, tab1])
    print("print frames")
    print(frames)

    write_table(frames,"results/t1.csv")

    cat = table_to_source_list(frames)
    print(cat)

    # 30, 0.094

    islands = regroup(cat, 0.094, far=None, dist=dist_3d)
    print(islands)

    for t in range(len(islands)):
        print(len(islands[t]))





    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    main()



