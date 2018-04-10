


def retrieve_data(folder, number)

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



def process_regrouping(cat, eps, stage, dist_func):
    """


    """

    regroup_start_time = time.time()  # record start time

    islands = regroup(cat, eps, far=None, dist=dist_func)

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

    write_catalog("./results/goodies_%s_%depochs" % (stage, hmany), goodies, fmt='csv')
    write_catalog("./results/badies_%s_%depochs" %(stage, hmany), badies, fmt='csv')

    goodies_cat = sorted(goodies)
    print(goodies_cat)
    print(badies)


    percentage_solved = 100 * (successes) / (len(tab))
    print("\nSuccess rate = %f%%" % percentage_solved)

    print("%s--- %f seconds ---" % (stage,(time.time() - start_time))