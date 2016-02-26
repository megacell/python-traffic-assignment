__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
compute diverse metrics
'''


import numpy as np
from All_Or_Nothing import all_or_nothing


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


def all_or_nothing_assignment(cost, net, demand):
    # given vector of edge costs, graph, and demand, computes the AoN assignment
    g = np.copy(net[:,:4])
    g[:,3] = cost
    return all_or_nothing(g, demand)


def total_cost_all_or_nothing(flow, net, demand):
    # computes the total cost in an all-or-nothing assignment 
    c = cost(flow, net)
    return c.dot(all_or_nothing_assignment(c, net, demand))


def average_cost_all_or_nothing(flow, net, demand):
    # computes the average cost in an all-or-nothing assignment
    return total_cost_all_or_nothing(flow, net, demand) / np.sum(demand[:,2])


def ratio_subset(flow, net, subset, eps=1e-8):
    # computes the average cost ratios on a subset of links
    tmp = np.multiply(cost(flow, net), subset)
    return np.sum(np.divide(tmp, np.maximum(net[:,3], eps))) / np.sum(subset)
