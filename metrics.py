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


def compute_metrics(alpha, f, net, d, feat, subset, out, row, fs=None, net2=None, \
    length_unit='Mile', time_unit='Minute'):
    '''
    Save in the numpy array 'out' at the specific 'row' the following metrics
    - average cost for non-routed
    - average cost for routed
    - average cost on a subset
    - total gas emissions
    - total gas emissions on a subset 
    '''
    if length_unit == 'Meter':
        lengths = feat[:,1] / 1609.34 # convert into miles
    elif length_unit == 'Mile':
        lengths = feat[:,1]
    if time_unit == 'Minute':
        a = 60.0
    elif time_unit == 'Second':
        a = 3600.
    b = 60./a
    speed = a * np.divide(lengths, np.maximum(cost(f, net), 10e-8))
    co2 = np.multiply(gas_emission(speed), lengths)
    out[row,0] = alpha
    out[row,3] = b * average_cost(f, net, d)
    out[row,4] = b * average_cost_subset(f, net, d, subset)
    out[row,5] = out[row,3] - out[row,4]
    out[row,6] = co2.dot(f) / f.dot(lengths)
    out[row,7] = np.multiply(co2, subset).dot(f) / f.dot(lengths)
    out[row,8] = out[row,6] - out[row,7]
    if alpha == 0.0:
        out[row,1] = b * average_cost(f, net, d)
        out[row,2] = b * average_cost_all_or_nothing(f, net, d)
        return
    if alpha == 1.0:
        L = all_or_nothing_assignment(cost(f, net2), net, d)
        out[row,1] = b * cost(f, net).dot(L) / np.sum(d[:,2])
        out[row,2] = b * average_cost(f, net, d)
        return
    out[row,1] = b * cost(f, net).dot(fs[:,0]) / np.sum((1-alpha)*d[:,2])
    out[row,2] = b * cost(f, net).dot(fs[:,1]) / np.sum(alpha*d[:,2])


def save_metrics(alphas, net, net2, d, features, subset, input, output, skiprows=0, \
    length_unit='Mile', time_unit='Minute'):
    out = np.zeros((len(alphas),9))
    a = 0
    if alphas[0] == 0.0:
        alpha = 0.0
        print 'compute for nr = {}, r = {}'.format(1-alphas[0], alphas[0])
        fs = np.loadtxt(input.format(int(alpha*100)), delimiter=',', \
            skiprows=skiprows)
        f = np.sum(fs, axis=1)
        compute_metrics(0.0, f, net, d, features, subset, out, 0, \
            length_unit=length_unit, time_unit=time_unit)
        a = 1

    b = 1 if alphas[-1] == 1.0 else 0
    for i,alpha in enumerate(alphas[a:len(alphas)-b]):
        print 'compute for nr = {}, r = {}'.format(1-alpha, alpha)
        fs = np.loadtxt(input.format(int(alpha*100)), delimiter=',', \
            skiprows=skiprows)
        f = np.sum(fs, axis=1)
        compute_metrics(alpha, f, net, d, features, subset, out, i+a, fs=fs, \
            length_unit=length_unit, time_unit=time_unit)

    if alphas[-1] == 1.0:
        alpha = 1.0
        print 'compute for nr = {}, r = {}'.format(1-alphas[-1], alphas[-1])
        fs = np.loadtxt(input.format(int(alpha*100)), delimiter=',', \
            skiprows=skiprows)
        f = np.sum(fs, axis=1)
        compute_metrics(1.0, f, net, d, features, subset, out, -1, net2=net2, \
            length_unit=length_unit, time_unit=time_unit)

    np.savetxt(output, out, delimiter=',', \
        header='ratio_routed,tt_non_routed,tt_routed,tt,tt_local,tt_non_local,gas,gas_local,gas_non_local', \
        comments='')


def path_cost(net, cost, d, g=None, od=None):
    '''
    given vector of edge costs, graph, demand
    returns shortest path cost for all ODs in d (or od) in the format
    {(o, d): path_cost}
    '''
    if g is None: 
        g = construct_igraph(net)
        g.es["weight"] = cost.tolist()
    if od is None:
        od = construct_od(d)
    out = {}
    for o in od.keys():
        c = g.shortest_paths_dijkstra(o, target=od[o][0], weights="weight")
        for i,d in enumerate(od[o][0]):
            out[(o,d)] = c[0][i]
    return out


def path_cost_non_routed(net, nr_cost, tt, d, g=None, od=None):
    '''
    given vector of edge costs, graph, demand
    returns travel time cost for non-routed users for all ODs in d (or od) in the format
    {(o, d): path_cost}
    '''
    if g is None: 
        g = construct_igraph(net)
        g.es["weight"] = nr_cost.tolist()
    if od is None:
        od = construct_od(d)
    out = {}
    for o in od.keys():
        p = g.get_shortest_paths(o, to=od[o][0], weights="weight", output="epath")
        for i,d in enumerate(od[o][0]):
            out[(o,d)] = np.sum(tt[p[i]])
    return out


def all_or_nothing_assignment(cost, net, demand):
    # given vector of edge costs, graph, and demand, computes the AoN assignment
    g = construct_igraph(net)
    od = construct_od(demand)
    g.es["weight"] = cost.tolist()    
    return all_or_nothing(g, od)
