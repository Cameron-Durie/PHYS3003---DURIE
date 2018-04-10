

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