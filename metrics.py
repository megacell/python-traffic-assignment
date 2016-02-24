__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
compute diverse metrics
'''


import numpy as np


def cost(flow, net):
    # returns vector of cost flows
    links = net.shape[0]
    x = np.power(flow.reshape((links,1)), np.array([0,1,2,3,4]))
    return np.einsum('ij,ij->i', x, net[:,3:])


def cost_ratio(flow, net, eps=1e-8):
    # returns vector of cost flows over zero-flow-cost
    tmp = np.divide(np.maximum(cost(flow, net), eps), np.maximum(net[:,3], eps))
    return np.minimum(tmp, 1./eps)


def total_cost(flow, net):
    return cost(flow, net).dot(flow)


def average_cost(flow, net, od):
    return total_cost(flow, net) / np.sum(od[:,2])



