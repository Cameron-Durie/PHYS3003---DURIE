#! /usr/bin/env python

"""
Functions for Matching program for splitting apart multi-groups

"""

__author__= "Cameron Durie"

# import
import numpy as np
import operator
from plotting import multigroup_plot

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def island_splitting(total_group, num, stage):
    """
    For peeling off one object from a multi-group based on flux splitting.

    :param total_group: The catalogue for the multi-group to be partially split.
    :param num: The number of epochs included.
    :param stage: The name of the current stage.

    :return: The separated group.
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
    For peeling apart all objects in a multi-group based on flux splitting.

    :param total_group: The catalogue for the multi-group to be split.
    :param num: The number of epochs included.
    :param stage: The name of the current stage.

    :return: All separated groups in a list.
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
                which_now = index*(group_size-split_num)+which_group-index
                flux_val = total_group[which_now].peak_flux
                flux_values.append(flux_val)
            index_max, value = max(enumerate(flux_values), key=operator.itemgetter(1))
            good_to_add = [total_group[(index*(group_size-split_num))+index_max-index]]
            new_single_good_island.extend(good_to_add)
            total_group.remove(good_to_add[0])
        new_good_islands.append(new_single_good_island)

    return new_good_islands