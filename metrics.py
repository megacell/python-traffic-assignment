__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
compute diverse metrics
'''


import numpy as np
# from All_Or_Nothing import all_or_nothing
from AoN_igraph import all_or_nothing
from process_data import construct_igraph, construct_od


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


# def all_or_nothing_assignment(cost, net, demand):
#     # given vector of edge costs, graph, and demand, computes the AoN assignment
#     g = np.copy(net[:,:4])
#     g[:,3] = cost
#     return all_or_nothing(g, demand)


def all_or_nothing_assignment(cost, net, demand):
    # given vector of edge costs, graph, and demand, computes the AoN assignment
    g = construct_igraph(net)
    od = construct_od(demand)
    g.es["weight"] = cost.tolist()    
    return all_or_nothing(g, od)


def total_cost_all_or_nothing(flow, net, demand):
    # computes the total cost in an all-or-nothing assignment 
    c = cost(flow, net)
    return c.dot(all_or_nothing_assignment(c, net, demand))


def average_cost_all_or_nothing(flow, net, demand):
    # computes the average cost in an all-or-nothing assignment
    return total_cost_all_or_nothing(flow, net, demand) / np.sum(demand[:,2])


def average_cost_subset(flow, net, od, subset, eps=1e-8):
    # computes the average cost ratios on a subset of links
    return np.multiply(cost(flow, net), subset).dot(flow) / np.sum(od[:,2])


def gas_emission(speed):
    return 350.*(speed>30.) + np.multiply((speed<=30.), 350.+650.*(30.-speed)/30.)


def compute_metrics(alpha, f, net, d, feat, subset, out, row, fs=None, net2=None):
    '''
    Save in the numpy array 'out' at the specific 'row' the following metrics
    - average cost for non-routed
    - average cost for routed
    - average cost on a subset
    - total gas emissions
    - total gas emissions on a subset 
    '''
    speed = 60.0 * np.divide(feat[:,1], np.maximum(cost(f, net), 10e-8))
    co2 = np.multiply(gas_emission(speed), feat[:,1])
    out[row,0] = alpha
    out[row,3] = average_cost_subset(f, net, d, subset)
    out[row,4] = co2.dot(f)
    out[row,5] = np.multiply(co2, subset).dot(f)
    if alpha == 0.0:
        out[row,1] = average_cost(f, net, d)
        out[row,2] = average_cost_all_or_nothing(f, net, d)
        return
    if alpha == 1.0:
        L = all_or_nothing_assignment(cost(f, net2), net, d)
        out[row,1] = cost(f, net).dot(L) / np.sum(d[:,2])
        out[row,2] = average_cost(f, net, d)
        return
    out[row,1] = cost(f, net).dot(fs[:,0]) / np.sum((1-alpha)*d[:,2])
    out[row,2] = cost(f, net).dot(fs[:,1]) / np.sum(alpha*d[:,2])


def save_metrics(alphas, net, net2, d, features, subset, input, output):
    out = np.zeros((len(alphas),6))
    a = 0
    if alphas[0] == 0.0:
        alpha = 0.0
        print 'compute for nr = {}, r = {}'.format(1-alphas[0], alphas[0])
        f = np.loadtxt(input.format(int(alpha*100)), delimiter=',')
        compute_metrics(0.0, f, net, d, features, subset, out, 0)
        a = 1

    b = 1 if alphas[-1] == 1.0 else 0
    for i,alpha in enumerate(alphas[a:len(alphas)-b]):
        print 'compute for nr = {}, r = {}'.format(1-alpha, alpha)
        fs = np.loadtxt(input.format(int(alpha*100)), delimiter=',')
        f = np.sum(fs, axis=1)
        compute_metrics(alpha, f, net, d, features, subset, out, i+a, fs=fs)

    if alphas[-1] == 1.0:
        alpha = 1.0
        print 'compute for nr = {}, r = {}'.format(1-alphas[-1], alphas[-1])
        f = np.loadtxt(input.format(int(alpha*100)), delimiter=',')
        compute_metrics(1.0, f, net, d, features, subset, out, -1, net2=net2)

    np.savetxt(output, out, delimiter=',')
