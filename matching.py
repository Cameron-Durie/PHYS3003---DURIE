#! /usr/bin/env python

"""
Matching program using Argean Tools

"""

__author__= "Cameron Durie"

# import
import numpy as np
import csv
import time

from cluster import sky_dist, regroup, dist_3d, best_dist
from catalogs import write_catalog, write_table, table_to_source_list
from processing import retrieve_data_csv, retrieve_data_fits, process_regrouping, process_remainder, process_regrouping_allislands
from iterations import process_iterations, process_iterations_splitting2

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def main():
    """

    """

    start_time = time.time()  # record start time
    hmany = 50  # How many csv files to load
    folder = './Data_set_1/'  # Target folder for extracting csv files

    cat = retrieve_data_csv(folder, hmany)
    success = 0

    stage1 = process_regrouping(cat, hmany, 1.20, 'stage1', best_dist, success)
    success = stage1['percentage_solved']

    stage2 = process_regrouping(stage1['badies'], hmany, 2.5, 'stage2', best_dist, success)
    success = stage2['percentage_solved']

    stage3 = process_regrouping(stage2['badies'], hmany, 0.8, 'stage3', best_dist, success)
    success = stage3['percentage_solved']

    stage4 = process_regrouping(stage3['badies'], hmany, 3.5, 'stage4', best_dist, success)
    success = stage4['percentage_solved']

    stage5 = process_regrouping(stage4['badies'], hmany, 0.6, 'stage5', best_dist, success)
    success = stage5['percentage_solved']

    stage6 = process_regrouping(stage5['badies'], hmany, 1.5, 'stage6', best_dist, success)
    success = stage6['percentage_solved']

    stage7 = process_regrouping(stage6['badies'], hmany, 0.2, 'stage7', sky_dist, success)
    success = stage7['percentage_solved']

    stage8 = process_regrouping_allislands(stage7['badies'], hmany, 0.1, 'stage8', sky_dist, success)
    success = stage8['percentage_solved']

    if len(stage8['badies']) != 0:
        stage9 = process_regrouping_allislands(stage8['badies'], hmany, 0.2, 'stage9', sky_dist, success)
        success = stage9['percentage_solved']
    else:
        stage9 = {'eps': 0.2, 'goodies': [],'badies': [], 'percentage_solved': stage8['percentage_solved'], 'time': 0.0, 'bug_count': 0}

    if len(stage9['badies']) != 0:
        stage10 = process_regrouping_allislands(stage9['badies'], hmany, 0.4, 'stage10', sky_dist, success)
        success = stage10['percentage_solved']
    else:
        stage10 = {'eps': 0.4, 'goodies': [],'badies': [], 'percentage_solved': stage9['percentage_solved'], 'time': 0.0, 'bug_count': 0}

    if len(stage10['badies']) != 0:
        stage11 = process_regrouping_allislands(stage10['badies'], hmany, 0.8, 'stage11', sky_dist, success)
        success = stage11['percentage_solved']
    else:
        stage11 = {'eps': 0.8, 'goodies': [],'badies': [], 'percentage_solved': stage10['percentage_solved'], 'time': 0.0, 'bug_count': 0}

    if len(stage11['badies']) != 0:
        stage12 = process_remainder(stage11['badies'], hmany, 'stage12', success)
        success = stage12['percentage_solved']
    else:
        stage12 = {'eps': 0, 'goodies': [],'badies': [], 'percentage_solved': stage11['percentage_solved'], 'time': 0.0, 'bug_count': 0}



    all_goodies = []
    all_goodies.extend(stage1['goodies'])
    all_goodies.extend(stage2['goodies'])
    all_goodies.extend(stage3['goodies'])
    all_goodies.extend(stage4['goodies'])
    all_goodies.extend(stage5['goodies'])
    all_goodies.extend(stage6['goodies'])
    all_goodies.extend(stage7['goodies'])
    all_goodies.extend(stage8['goodies'])
    all_goodies.extend(stage9['goodies'])
    all_goodies.extend(stage10['goodies'])
    all_goodies.extend(stage11['goodies'])
    all_goodies.extend(stage12['goodies'])

    write_catalog("./results/goodies/%d_epochs/all_goodies_%depochs" % (hmany, hmany), all_goodies, fmt='csv')


    # OUTPUT PERFORMANCE INFORMATION
    stages = [stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8, stage9, stage10, stage11, stage12]
    with open("./results/timing/performance_%d_epochs.csv" %hmany,'w') as run_data:
        csv_writer = csv.writer(run_data, delimiter=',')
        csv_writer.writerow(['stage', 'eps', 'time', 'percentage_solved', 'number_in', 'number_out', 'number_solved', 'bug_count'])
        i = 1
        for stage in stages:
            csv_writer.writerow([i, stage['eps'], stage['time'], stage['percentage_solved'], len(stage['badies'])+len(stage['goodies']), len(stage['badies']), len(stage['goodies']), stage['bug_count']])
            i += 1
        csv_writer.writerow(["total_time = %f secs" %(time.time() - start_time)])

    percentage_solved = 100*((len(all_goodies))/(len(cat)))
    print("\nSuccess rate = %f%%" %percentage_solved)

    print("total  --- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()