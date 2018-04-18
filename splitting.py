#! /usr/bin/env python

"""
Functions for Matching program

"""

__author__= "Cameron Durie"

# import
import numpy as np
import operator
from plotting import multigroup_plot

def island_splitting(total_group, num, stage):
    """

    """

    group_size = int(len(total_group)/num)
    print(total_group)

    multigroup_plot(total_group, stage, num, group_size)

    new_good_island = []

    for index in range(num):
        flux_values = []
        for which_group in range(group_size):
            which_now = index*group_size+which_group
            flux_val = [total_group[which_now].peak_flux]
            flux_values.extend(flux_val)
        index_max, value = max(enumerate(flux_values), key=operator.itemgetter(1))
        good_to_add = [total_group[index*group_size+index_max]]
        new_good_island.extend(good_to_add)

    return new_good_island

def complete_island_splitting(total_group, num, stage):
    """

    """
    group_size = int(len(total_group)/num)
    print(total_group)

    multigroup_plot(total_group, stage, num, group_size)
    new_good_islands = []

    for split_num in range(group_size):
        new_single_good_island = []
        for index in range(num):
            flux_values = []
            for which_group in range(group_size-split_num):
                which_now = index*(group_size-split_num)+which_group
                flux_val = [total_group[which_now].peak_flux]
                flux_values.extend(flux_val)
            index_max, value = max(enumerate(flux_values), key=operator.itemgetter(1))
            good_to_add = [total_group[(index*group_size)+index_max]]
            new_single_good_island.extend(good_to_add)
        new_good_islands.append(new_single_good_island)

    return new_good_islands