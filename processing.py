#! /usr/bin/env python

"""
Functions for Matching program

"""

__author__= "Cameron Durie"

# import
import numpy as np
import time
import glob,os

from cluster import regroup
from catalogs import write_catalog, write_table, table_to_source_list
from plotting import light_curve
from splitting import island_splitting, complete_island_splitting
from astropy.table import vstack, table


# join the Aegean logger
import logging
log = logging.getLogger('Aegean')



def retrieve_data_csv(folder, number):
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

def retrieve_data_fits(folder, number):
    """


    """
    #astrogpy.io fits

    files = []  # To store list of target csv files
    epoch = 0

    os.chdir("%s" % folder)
    for file in glob.glob("*.fits"):
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

        tab['island'] = epoch
        tab['source'][:] = range(0, len(tab))

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



def process_regrouping(cat, number, eps, stage, dist_func, success):
    """


    """

    regroup_start_time = time.time()  # record start time

    regroup_return = regroup(cat, eps, number, far=None, dist=dist_func)
    islands = regroup_return['islands']
    bug_count = regroup_return['bug_counter']

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == number:
            goodies.append(islands[i])
            light_curve(islands[i], stage, number)
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

    percentage_solved = 100*(success/100 + (1-success/100)*(len(goodies)/(len(goodies)+len(badies))))
    print("\nSuccess rate = %f%%" % percentage_solved)

    run_time = (time.time() - regroup_start_time)
    print("%s  --- %f seconds ---" % (stage, run_time))

    return {'eps': eps, 'goodies': goodies, 'badies': badies, 'percentage_solved':  percentage_solved, 'time': run_time, 'bug_count': bug_count}



def process_regrouping_doubleislands(cat, number, eps, stage, dist_func, success):
    """


    """

    regroup_start_time = time.time()  # record start time

    regroup_return = regroup(cat, eps, number, far=None, dist=dist_func, multi = True)
    islands = regroup_return['islands']
    bug_count = regroup_return['bug_counter']

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == number:
            goodies.append(islands[i])
            light_curve(islands[i], stage, number)
        elif len(islands[i])% number == 0:
            seperated_group = island_splitting(islands[i], number, stage)
            goodies.append(seperated_group)
            light_curve(seperated_group, stage, number)
            rest_multi = [item for item in islands[i] if item not in seperated_group]
            if len(islands[i]) == (2*number):
                goodies.append(rest_multi)
                light_curve(rest_multi, stage, number)
            else:
                badies.extend(rest_multi)

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

    percentage_solved = 100*(success/100 + (1-success/100)*(len(goodies)/(len(goodies)+len(badies))))
    print("\nSuccess rate = %f%%" % percentage_solved)

    run_time = (time.time() - regroup_start_time)
    print("%s  --- %f seconds ---" % (stage, run_time))

    return {'eps': eps, 'goodies': goodies, 'badies': badies, 'percentage_solved':  percentage_solved, 'time': run_time, 'bug_count': bug_count}




def process_regrouping_allislands(cat, number, eps, stage, dist_func, success):
    """


    """

    regroup_start_time = time.time()  # record start time

    regroup_return = regroup(cat, eps, number, far=None, dist=dist_func, multi = True)
    islands = regroup_return['islands']
    bug_count = regroup_return['bug_counter']

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == number:
            goodies.append(islands[i])
            light_curve(islands[i], stage, number)
        elif len(islands[i])% number == 0:
            seperated_group = complete_island_splitting(islands[i], number, stage)
            goodies.extend(seperated_group)
            for i in range(int(len(seperated_group))):
                light_curve(seperated_group[i], stage, number)
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

    percentage_solved = 100*(success/100 + (1-success/100)*(len(goodies)/(len(goodies)+len(badies))))
    print("\nSuccess rate = %f%%" % percentage_solved)

    run_time = (time.time() - regroup_start_time)
    print("%s  --- %f seconds ---" % (stage, run_time))

    return {'eps': eps, 'goodies': goodies, 'badies': badies, 'percentage_solved':  percentage_solved, 'time': run_time, 'bug_count': bug_count}



def process_remainder(cat, number, stage, success):
    """


    """

    regroup_start_time = time.time()  # record start time
    islands = [cat]
    bug_count = 0
    eps = 0

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    islands[0] = sorted(islands[0])
    seperated_group = complete_island_splitting(islands[0], number, stage)
    goodies.extend(seperated_group)
    for i in range(int(len(seperated_group))):
       light_curve(seperated_group[i], stage, number)

    badies.extend([item for item in islands[0] if item not in np.ravel(seperated_group)])

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

    percentage_solved = 100*(success/100 + (1-success/100)*(len(goodies)/(len(goodies)+len(badies))))
    print("\nSuccess rate = %f%%" % percentage_solved)

    run_time = (time.time() - regroup_start_time)
    print("%s  --- %f seconds ---" % (stage, run_time))

    return {'eps': eps, 'goodies': goodies, 'badies': badies, 'percentage_solved':  percentage_solved, 'time': run_time, 'bug_count': bug_count}