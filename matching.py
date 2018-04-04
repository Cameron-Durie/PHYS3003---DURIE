#! /usr/bin/env python

"""
Matching program using Argean Tools

"""

__author__= "Cameron Durie"

# import
import numpy as np
import math
import time
import glob

from cluster import sky_dist, regroup, dist_3d
from catalogs import write_catalog, write_table, table_to_source_list
from astropy.table import vstack, table


# join the Aegean logger
import logging
log = logging.getLogger('Aegean')


def main():

    # record start time
    start_time = time.time()


    # load tables
    filenames = glob.glob('./Data_set_2_small' + "/*.csv")
    files = []
    for filename in filenames:
        files.append(table.Table.read(filename))


    print(files)

    tab0 = table.Table.read('Data_set_2_small/epoch00.csv');
    print(tab0)
    tab1 = table.Table.read('Data_set_2_small/epoch01.csv');
    print(tab1)

    # rename columns
    tab0.rename_column("# src", "source")
    tab0.rename_column("RA(deg)","ra")
    tab0.rename_column("err_RA(deg)", "err_ra")
    tab0.rename_column("Dec(deg)", "dec")
    tab0.rename_column("err_Dec(deg)", "err_dec")
    tab0.rename_column("Flux(Jy)", "peak_flux")
    tab0.rename_column("err_Flux(Jy)", "err_peak_flux")

    tab1.rename_column("# src", "source")
    tab1.rename_column("RA(deg)", "ra")
    tab1.rename_column("err_RA(deg)", "err_ra")
    tab1.rename_column("Dec(deg)", "dec")
    tab1.rename_column("err_Dec(deg)", "err_dec")
    tab1.rename_column("Flux(Jy)", "peak_flux")
    tab1.rename_column("err_Flux(Jy)", "err_peak_flux")

    print(tab0)
    print(tab1)

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



