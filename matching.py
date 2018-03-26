#! /usr/bin/env python

"""
Matching program using Argean Tools

"""

__author__= "Cameron Durie"

import numpy as np
import math

from cluster import sky_dist, regroup
from catalogs import load_table,write_table, table_to_source_list
from astropy import table
from models import OutputSource

import time

# join the Aegean logger
import logging
log = logging.getLogger('Aegean')


def main():

    tab = table.Table.read('Data_set_1/epoch00.csv');
    print(tab)

    # rename columns
    tab.rename_column("RA(deg)","ra_str")
    tab.rename_column("err_RA(deg)", "err_ra")
    tab.rename_column("Dec(deg)", "dec_str")
    tab.rename_column("err_Dec(deg)", "err_dec")
    tab.rename_column("Flux(Jy)", "int_flux")
    tab.rename_column("err_Flux(Jy)", "err_int_flux")

    print(tab)

    cat = table_to_source_list(tab, src_type=OutputSource)
    print(cat)

    islands = regroup(cat, 10, far=None, dist=sky_dist)

    print(islands)



if __name__ == '__main__':
    main()





