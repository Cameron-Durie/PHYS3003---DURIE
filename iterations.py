#! /usr/bin/env python

"""
Tuning functions for Matching program.

"""

__author__= "Cameron Durie"

# import
import numpy as np
import csv
import time

from cluster import regroup

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')


def process_iterations(cat, number, length, stage_name, dist_func, previous_successes, a1, b1, c1):
    """
    Function for tuning program eps values in layer one.

    :param cat: Inputted catalogue of sources as yet unsolved.
    :param number: The number of epochs included.
    :param length: The length of the inputted catalogue of sources.
    :param stage_name: The name of the stage being tuned.
    :param dist_func: The seperation function to be used.
    :param previous_successes: The percentage of sources solved by the beginning of this tuning stage.
    :param a1: Starting eps.
    :param b1: Ending eps.
    :param c1: Increment for eps.

    :return: Nothing. However it does output csv file with info for each eps tested.
    """

    start_time = time.time()
    stage = []
    test_area = np.arange(a1,b1,c1)
    print(test_area)

    for eps in test_area:
        regroup_return = regroup(cat, eps, number, far=None, dist=dist_func)
        islands = regroup_return['islands']

        for t in range(len(islands)):
            print(len(islands[t]))

        total_count = len(islands)
        print("%d islands created\n" % total_count)

        successes = 0

        for i in range(len(islands)):
            islands[i] = sorted(islands[i])
            if len(islands[i]) == number:
                successes += 1


        percentage_solved = 100*(successes*number)/(length) + previous_successes
        print("\nSuccess rate = %f%%" % percentage_solved)

        print("--- %s seconds ---" % (time.time() - start_time))
        print(eps)
        print("-->")
        print(b1)

        alt_point = [eps, percentage_solved, total_count]
        stage.append(alt_point)

    for i in range(len(stage)):
        print(stage[i])

    with open("./results/stages/%s_eps=%.1f-%.1f_by_%.3f_with_%d_epochs.csv" %(stage_name, a1, b1, c1, number), 'w') as graph_data:
        csv_writer = csv.writer(graph_data, delimiter=',')
        csv_writer.writerow(['eps','success','islands_created'])
        for line in range(len(stage)):
            csv_writer.writerow(stage[line])



def process_iterations_splitting(cat, number, length, stage_name, dist_func, previous_successes, a1, b1, c1):
    """
    Function for tuning program eps value for layer two. The maximum point should not be selected. A lower eps should be selected.

    :param cat: Inputted catalogue of sources as yet unsolved.
    :param number: The number of epochs included.
    :param length: The length of the inputted catalogue of sources.
    :param stage_name: The name of the stage being tuned.
    :param dist_func: The seperation function to be used.
    :param previous_successes: The percentage of sources solved by the beginning of this tuning stage.
    :param a1: Starting eps.
    :param b1: Ending eps.
    :param c1: Increment for eps.

    :return: Nothing. However it does output csv file with info for each eps tested.
    """

    start_time = time.time()
    stage = []
    test_area = np.arange(a1,b1,c1)
    print(test_area)


    for eps in test_area:
        regroup_return = regroup(cat, eps, number, far=None, dist=dist_func)
        islands = regroup_return['islands']

        for t in range(len(islands)):
            print(len(islands[t]))

        total_count = len(islands)
        print("%d islands created\n" % total_count)

        successes = 0

        for i in range(len(islands)):
            islands[i] = sorted(islands[i])
            if len(islands[i]) == number:
                successes += 1
            elif len(islands[i]) == 2*number:
                successes += 2

        percentage_solved = 100 * (successes*number)/(length) + previous_successes
        print("\nSuccess rate = %f%%" % percentage_solved)

        print("--- %s seconds ---" % (time.time() - start_time))
        print(eps)
        print("-->")
        print(b1)

        alt_point = [eps, percentage_solved, total_count]
        stage.append(alt_point)

    for i in range(len(stage)):
        print(stage[i])

    with open("./results/stages/%s_eps=%.1f-%.1f_by_%.3f_with_%d_epochs.csv" %(stage_name, a1, b1, c1, number), 'w') as graph_data:
        csv_writer = csv.writer(graph_data, delimiter=',')
        csv_writer.writerow(['eps','success','islands_created'])
        for line in range(len(stage)):
            csv_writer.writerow(stage[line])