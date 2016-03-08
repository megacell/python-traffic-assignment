__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"


import numpy as np


def all_or_nothing(g, od):
    '''
    We are given an igraph object 'g' with od in the format {from: ([to], [rate])}
    do all_or_nothing assignment 
    '''
    L = np.zeros(len(g.es), dtype="float64")
    for o in od.keys():
        out = g.get_shortest_paths(o, to=od[o][0], weights="weight", output="epath")
        for i, inds in enumerate(out):
            L[inds] = L[inds] + od[o][1][i]
    return L

