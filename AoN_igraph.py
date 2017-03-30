import numpy as np

'''
all-or-nothing assignment using igraph
'''


def all_or_nothing(g, od):
    '''
    We are given an igraph object 'g'
    with od in the format {from: ([to], [rate])}
    do all_or_nothing assignment
    '''
    L = np.zeros(len(g.es), dtype="float64")
    for o in od.keys():
        out = g.get_shortest_paths(
            o, to=od[o][0], weights="weight", output="epath")
        for i, inds in enumerate(out):
            # if len(inds) == 0:
                # print 'no path between {} and {}'.format(o, od[o][0][i])
            L[inds] = L[inds] + od[o][1][i]
    return L
