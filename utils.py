__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
Some function that can be useful
'''

import numpy as np


def digits(x):
    # return number of digits in the integer part
    if x < 10.0: return 1
    return int(np.log(x)/np.log(10)) + 1


def spaces(n):
    # return the appropriate number of spaces
    return ''.join([' ']*(n))


def multiply_cognitive_cost(net, feat, thres, cog_cost):
    net2 = np.copy(net)
    small_capacity = np.zeros((net2.shape[0],))
    for row in range(net2.shape[0]):
        if feat[row,0] < thres:
            small_capacity[row] = 1.0
            net2[row,3:] = net2[row,3:] * cog_cost
    return net2, small_capacity


def heterogeneous_demand(d, alpha):
    d_nr = np.copy(d)
    d_r = np.copy(d)
    d_nr[:,2] = (1-alpha) * d_nr[:,2]
    d_r[:,2] = alpha * d_r[:,2]
    return d_nr, d_r