#! /usr/bin/env python

"""
Matching program using Argean Tools

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
from processing import retrieve_data, process_regrouping
from iterations import process_iterations, process_iterations_splitting
from astropy.table import vstack, table

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def main():


    start_time = time.time()  # record start time
    hmany = 2  # How many csv files to load
    folder = './Data_set_1/'  # Target folder for extracting csv files

    cat = retrieve_data(folder, hmany)
    success = 0

    stage1 = process_regrouping(cat, hmany, len(cat), 1.20, 'stage1', best_dist, success)
    success = stage1['success']

    stage2 = process_regrouping(stage1['badies'], hmany, len(cat), 2.5, 'stage2', best_dist, success)
    success = stage2['success']

    stage3 = process_regrouping(stage2['badies'], hmany, len(cat), 0.8, 'stage3', best_dist, success)
    success = stage3['success']

    stage4 = process_regrouping(stage3['badies'], hmany, len(cat), 3.5, 'stage4', best_dist, success)
    success = stage4['success']

    stage5 = process_regrouping(stage4['badies'], hmany, len(cat), 0.6, 'stage5', best_dist, success)
    success = stage5['success']

    stage6 = process_regrouping(stage5['badies'], hmany, len(cat), 1.5, 'stage6', best_dist, success)
    success = stage6['success']

    """
    process_iterations_splitting(stage6['badies'], hmany, len(cat), 'stage7', best_dist, success, 0.2, 4.0, 0.1)
    """

    all_goodies = []
    all_goodies.extend(stage1['goodies'])
    all_goodies.extend(stage2['goodies'])
    all_goodies.extend(stage3['goodies'])
    all_goodies.extend(stage4['goodies'])
    all_goodies.extend(stage5['goodies'])
    all_goodies.extend(stage6['goodies'])
    

    write_catalog("./results/goodies/%d_epochs/all_goodies_%depochs" % (hmany, hmany), all_goodies, fmt='csv')

    stages = [stage1, stage2, stage3, stage4, stage5, stage6]
    with open("./results/timing/performance_%d_epochs.csv" %hmany,'w') as run_data:
        csv_writer = csv.writer(run_data, delimiter=',')
        csv_writer.writerow(['stage','time', 'percentage_solved'])
        i = 1
        for stage in stages:
            csv_writer.writerow([i, stage['time'], stage['percentage_solved']])
            i += 1

    percentage_solved = 100*(success*hmany)/(len(cat))
    print("\nSuccess rate = %f%%" %percentage_solved)

    print("total  --- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()