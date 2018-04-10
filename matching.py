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
from astropy.table import vstack, table

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')

def main():

    # record start time
    start_time = time.time()

    hmany = 50  # How many csv files to load

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
        else:
            frames = vstack([frames, tab])
        epoch += 1

    print(frames)
    write_table(frames,"./results/frames%d.csv" %hmany)

    cat = table_to_source_list(frames)
    print(cat)


    islands = regroup(cat, 1.26, far=None, dist=best_dist)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []
    successes = 0

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == hmany:
            successes += 1
            goodies.append(islands[i])
    #    else:
    #       badies.append(islands[i])

    goodies = sorted(goodies)
    #    badies = sorted(badies)

    for i in range(len(goodies)):
        print(goodies[i])

    goodies = np.ravel(goodies)
    #    badies = np.ravel(badies)

    badies = [x for x in cat if x not in goodies]  # slow alternative
    badies = sorted(badies)

    write_catalog("./results/goodies1_%depochs" %hmany, goodies, fmt='csv')
    write_catalog("./results/badies1_%depochs" %hmany, badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)

    percentage_solved = 100 * (successes) / (len(tab))
    print("\nSuccess rate = %f%%" % percentage_solved)


    ################### STAGE 2 ###################

    new_cat1 = badies
    islands = regroup(new_cat1, 2.25, far=None, dist=best_dist)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == hmany:
            successes += 1
            goodies.append(islands[i])
    #        else:
    #            badies.append(islands[i])

    goodies = sorted(goodies)
    #    badies = sorted(badies)

    for i in range(len(goodies)):
        print(goodies[i])

    goodies = np.ravel(goodies)
    #    badies = np.ravel(badies)

    badies = [x for x in new_cat1 if x not in goodies]  # slow alternative
    badies = sorted(badies)

    write_catalog("./results/goodies2_%depochs" %hmany, goodies, fmt='csv')
    write_catalog("./results/badies2_%depochs" %hmany, badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)

    percentage_solved = 100 * (successes) / (len(tab))
    print("\nSuccess rate = %f%%" % percentage_solved)



    ################## STAGE 3 ####################

    new_cat2 = badies
    islands = regroup(new_cat2, 0.75, far=None, dist=best_dist)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == hmany:
            successes += 1
            goodies.append(islands[i])
    #        else:
    #            badies.append(islands[i])

    goodies = sorted(goodies)
    #    badies = sorted(badies)

    for i in range(len(goodies)):
        print(goodies[i])

    goodies = np.ravel(goodies)
    #    badies = np.ravel(badies)

    badies = [x for x in new_cat2 if x not in goodies]  # slow alternative
    badies = sorted(badies)

    write_catalog("./results/goodies3_%depochs" %hmany, goodies, fmt='csv')
    write_catalog("./results/badies3_%depochs" %hmany, badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)

    percentage_solved = 100 * (successes) / (len(tab))
    print("\nSuccess rate = %f%%" % percentage_solved)


    ################## STAGE 4 ####################

    new_cat3 = badies
    islands = regroup(new_cat3, 3.5, far=None, dist=best_dist)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == hmany:
            successes += 1
            goodies.append(islands[i])
    #        else:
    #            badies.append(islands[i])

    goodies = sorted(goodies)
    #    badies = sorted(badies)

    for i in range(len(goodies)):
        print(goodies[i])

    goodies = np.ravel(goodies)
    #    badies = np.ravel(badies)

    badies = [x for x in new_cat3 if x not in goodies]  # slow alternative
    badies = sorted(badies)

    write_catalog("./results/goodies5_%depochs" %hmany, goodies, fmt='csv')
    write_catalog("./results/badies5_%depochs" %hmany, badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)

    percentage_solved = 100 * (successes) / (len(tab))
    print("\nSuccess rate = %f%%" % percentage_solved)

    ################## STAGE 5 ####################

    new_cat4 = badies
    islands = regroup(new_cat4, 0.47, far=None, dist=best_dist)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == hmany:
            successes += 1
            goodies.append(islands[i])
    #        else:
    #            badies.append(islands[i])

    previous_success2 = successes

    goodies = sorted(goodies)
    #    badies = sorted(badies)

    for i in range(len(goodies)):
        print(goodies[i])

    goodies = np.ravel(goodies)
    #    badies = np.ravel(badies)

    badies = [x for x in new_cat3 if x not in goodies]  # slow alternative
    badies = sorted(badies)

    write_catalog("./results/goodies5_%depochs" % hmany, goodies, fmt='csv')
    write_catalog("./results/badies5_%depochs" % hmany, badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)

    percentage_solved = 100 * (successes) / (len(tab))
    print("\nSuccess rate = %f%%" % percentage_solved)



    ################## STAGE 6 ####################

    new_cat5 = badies
    islands = regroup(new_cat5, 0.15, far=None, dist=sky_dist)

    for t in range(len(islands)):
        print(len(islands[t]))

    total_count = len(islands)
    print("%d islands created\n" % total_count)

    goodies = []
    badies = []

    for i in range(len(islands)):
        islands[i] = sorted(islands[i])
        if len(islands[i]) == hmany:
            successes += 1
            goodies.append(islands[i])
    #        else:
    #            badies.append(islands[i])

    previous_success2 = successes

    goodies = sorted(goodies)
    #    badies = sorted(badies)

    for i in range(len(goodies)):
        print(goodies[i])

    goodies = np.ravel(goodies)
    #    badies = np.ravel(badies)

    badies = [x for x in new_cat4 if x not in goodies]  # slow alternative
    badies = sorted(badies)

    write_catalog("./results/goodies6_%depochs" % hmany, goodies, fmt='csv')
    write_catalog("./results/badies6_%depochs" % hmany, badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)

    percentage_solved = 100 * (successes) / (len(tab))
    print("\nSuccess rate = %f%%" % percentage_solved)


    """
    ###################### STAGE Iteration ######################

    new_cat5 = badies

    stage2 = []
    a1 = 0.01  #from
    b1 = 0.2  #to
    c1 = 0.001  #increments
    test_area = np.arange(a1,b1,c1)
    print(test_area)

    for eps in test_area:
        islands = regroup(new_cat5, eps, far=None, dist=sky_dist)

        for t in range(len(islands)):
            print(len(islands[t]))

        total_count = len(islands)
        print("%d islands created\n" % total_count)

        goodies = []
        successes = previous_success2

        for i in range(len(islands)):
            islands[i] = sorted(islands[i])
            if len(islands[i]) == hmany:
                successes += 1
                goodies.append(islands[i])
        #        else:
        #            badies.append(islands[i])

        goodies = sorted(goodies)
        #    badies = sorted(badies)

        for i in range(len(goodies)):
            print(goodies[i])

        goodies = np.ravel(goodies)
        #    badies = np.ravel(badies)

        #badies = [x for x in cat if x not in goodies]  # slow alternative
        badies = sorted(badies)

        goodies_cat = sorted(goodies)
        #print(goodies_cat)
        #print(badies)

        percentage_solved = 100 * (successes) / (len(tab))
        print("\nSuccess rate = %f%%" % percentage_solved)

        print("--- %s seconds ---" % (time.time() - start_time))
        print(eps)
        print("-->")
        print(b1)

        alt_point = [eps, percentage_solved, total_count]
        stage2.append(alt_point)

    for i in range(len(stage2)):
        print(stage2[i])

    with open("./results/stages/stage1_eps=%.1f-%.1f_by_%.3f_with_%d_epochs.csv" %(a1, b1, c1, hmany), 'w') as graph_data:
        csv_writer = csv.writer(graph_data, delimiter=',')
        csv_writer.writerow(['eps','success','islands_created'])
        for line in range(len(stage2)):
            csv_writer.writerow(stage2[line])



    percentage_solved = 100*(successes)/(len(tab))
    print("\nSuccess rate = %f%%" %percentage_solved)

    print("--- %s seconds ---" % (time.time() - start_time))
    """


if __name__ == '__main__':
    main()