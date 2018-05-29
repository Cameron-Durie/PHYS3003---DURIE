#! /usr/bin/env python

"""
Matching program using Argean Tools

"""

__author__= "Cameron Durie"

# import
import csv
import time

from cluster import sky_dist, regroup, dist_3d, best_dist
from catalogs import write_catalog
from processing import retrieve_data_csv, retrieve_data_fits, process_regrouping, process_remainder, process_regrouping_allislands, process_regrouping_fractionislands
from iterations import process_iterations, process_iterations_splitting

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def main():
    """

    """

    start_time = time.time()  # record start time
    hmany = 25  # How many csv files to load
    folder = './expert'  # Target folder for extracting csv files

    data = retrieve_data_fits(folder, hmany)
    success = 0

    print(data['run_partial'])

    stage1 = process_regrouping(data['cat'], hmany, 1.20, 'stage1', best_dist, success)
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

    if len(stage6['badies']) != 0:
        stage7 = process_regrouping(stage6['badies'], hmany, 0.2, 'stage7', sky_dist, success)
        success = stage7['percentage_solved']
    else:
        stage7 = {'eps': 0.2, 'goodies': [],'badies': [], 'percentage_solved': stage6['percentage_solved'], 'time': 0.0, 'bug_count': 0}

    if len(stage7['badies']) != 0:
        stage8 = process_regrouping_allislands(stage7['badies'], hmany, 0.1, 'stage8', sky_dist, success)
        success = stage8['percentage_solved']
    else:
        stage8 = {'eps': 0.1, 'goodies': [],'badies': [], 'percentage_solved': stage7['percentage_solved'], 'time': 0.0, 'bug_count': 0}

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
        if data['run_partial'] is False:
            stage12 = process_remainder(stage11['badies'], hmany, 'stage12', success)
            success = stage12['percentage_solved']
        else:
            stage12 = process_regrouping_fractionislands(stage11['badies'], hmany, 8.0, 'stage12', best_dist, success)
            success = stage12['percentage_solved']

            stage13 = process_regrouping_fractionislands(stage12['badies'], hmany, 4.0, 'stage13', best_dist, success)
            success = stage13['percentage_solved']

            stage14 = process_regrouping_fractionislands(stage13['badies'], hmany, 2.0, 'stage14', best_dist, success)
            success = stage14['percentage_solved']

            stage15 = process_regrouping_fractionislands(stage14['badies'], hmany, 1.0, 'stage15', best_dist, success)
            success = stage15['percentage_solved']

            stage16 = process_regrouping_fractionislands(stage15['badies'], hmany, 0.5, 'stage16', best_dist, success)
            success = stage16['percentage_solved']

            stage17 = process_regrouping_fractionislands(stage16['badies'], hmany, 8.0, 'stage17', best_dist, success, looseness=2)
            success = stage17['percentage_solved']

            stage18 = process_regrouping_fractionislands(stage17['badies'], hmany, 4.0, 'stage18', best_dist, success, looseness=2)
            success = stage18['percentage_solved']

            stage19 = process_regrouping_fractionislands(stage18['badies'], hmany, 2.0, 'stage19', best_dist, success, looseness=2)
            success = stage19['percentage_solved']

            stage20 = process_regrouping_fractionislands(stage19['badies'], hmany, 1.0, 'stage20', best_dist, success, looseness=2)
            success = stage20['percentage_solved']

            stage21 = process_regrouping_fractionislands(stage20['badies'], hmany, 8.0, 'stage21', best_dist, success, looseness=3)
            success = stage21['percentage_solved']

            stage22 = process_regrouping_fractionislands(stage21['badies'], hmany, 4.0, 'stage22', best_dist, success, looseness=3)
            success = stage22['percentage_solved']

            stage23 = process_regrouping_fractionislands(stage22['badies'], hmany, 2.0, 'stage23', best_dist, success, looseness=3)
            success = stage23['percentage_solved']

            stage24 = process_regrouping_fractionislands(stage23['badies'], hmany, 1.0, 'stage24', best_dist, success, looseness=3)
            success = stage24['percentage_solved']

            stage25 = process_remainder(stage24['badies'], hmany, 'stage25', success)
            success = stage25['percentage_solved']
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

    if data['run_partial'] is True:
        all_goodies.extend(stage13['goodies'])
        all_goodies.extend(stage14['goodies'])
        all_goodies.extend(stage15['goodies'])
        all_goodies.extend(stage16['goodies'])
        all_goodies.extend(stage17['goodies'])
        all_goodies.extend(stage18['goodies'])
        all_goodies.extend(stage19['goodies'])
        all_goodies.extend(stage20['goodies'])
        all_goodies.extend(stage21['goodies'])
        all_goodies.extend(stage22['goodies'])
        all_goodies.extend(stage23['goodies'])
        all_goodies.extend(stage24['goodies'])

    write_catalog("./results/goodies/%d_epochs/all_goodies_%depochs" % (hmany, hmany), all_goodies, fmt='csv')


    # OUTPUT PERFORMANCE INFORMATION
    if data['run_partial'] is False:
        stages = [stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8, stage9, stage10, stage11, stage12]
    else:
        stages = [stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8, stage9, stage10, stage11, stage12, stage13, stage14, stage15, stage16, stage17, stage18, stage19, stage20, stage21, stage22, stage23, stage24]

    with open("./results/timing/performance_%d_epochs.csv" %hmany,'w') as run_data:
        csv_writer = csv.writer(run_data, delimiter=',')
        csv_writer.writerow(['stage', 'eps', 'time', 'percentage_solved', 'number_in', 'number_out', 'number_solved', 'correction_count'])
        i = 1
        for stage in stages:
            csv_writer.writerow([i, stage['eps'], stage['time'], stage['percentage_solved'], len(stage['badies'])+len(stage['goodies']), len(stage['badies']), len(stage['goodies']), stage['bug_count']])
            i += 1
        csv_writer.writerow(["total_time = %f secs" %(time.time() - start_time)])

    percentage_solved = 100*((len(all_goodies))/(len(data['cat'])))
    print("\nSuccess rate = %f%%" %percentage_solved)

    print("total  --- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()