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
    - average cost
    - average cost on a subset (e.g. local routes)
    - average cost outside of a subset (e.g. non-local routes)
    - total gas emissions
    - total gas emissions on a subset (e.g. local routes)
    - total gas emissions outside of a subset (e.g. non-local routes)
    - total flow in the network
    - total flow in the network on a subset (e.g. local routes)
    - total flow in the network outside of a subset (e.g. non-local routes)
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
    out[row,9] = np.sum(np.multiply(f, lengths)) * 4000.
    out[row,10] = np.sum(np.multiply(np.multiply(f, lengths), subset)) * 4000.
    out[row,11] = out[row,9] - out[row,10]
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
    out = np.zeros((len(alphas),12))
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

    colnames = 'ratio_routed,tt_non_routed,tt_routed,tt,tt_local,tt_non_local,gas,gas_local,gas_non_local,'
    colnames = colnames + 'vmt,vmt_local,vmt_non_local'
    np.savetxt(output, out, delimiter=',', \
        header=colnames, \
        comments='')


def path_cost(net, cost, d, g=None, od=None):
    '''
    given graph, vector of edge costs, demand
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
    given 
    net:     graph
    nr_cost: vector of edge costs
    tt:      vector of free-flow travel times
    d:       demand
    returns travel time cost for non-routed users for all ODs in d (or od) in the format
    {(o, d): path_cost}
    '''
    if g is None: 
        g = construct_igraph(net)
        g.es["weight"] = nr_cost.tolist()
    else:
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


def OD_routed_costs(alphas, net, demand, inputs, output, verbose=0):
    '''
    from input files of equilibrium flows for the heterogeneous game
    outputs the travel times of routes users
    '''
    od = construct_od(demand) # od is a dict {origin: ([destination],[demand])}
    num_ods = demand.shape[0]
    out = np.zeros((num_ods, len(alphas)+2))
    out[:,:2] = demand[:,:2]
    g = construct_igraph(net) # construct igraph object
    for i, alpha in enumerate(alphas):
        fs = np.loadtxt(inputs.format(int(alpha*100)), delimiter=',', skiprows=1)
        c = cost(np.sum(fs, axis=1), net)
        g.es["weight"] = c.tolist()    
        # get shortest path and returns {(o, d): path_cost}
        if verbose >= 1: 
            print 'computing OD costs for alpha = {} ...'.format(alpha)
        costs = path_cost(net, c, demand, g, od) 
        for j in range(num_ods):
            out[j,i+2] = costs[(int(out[j,0]), int(out[j,1]))]
    header = ['o,d']
    for alpha in alphas: 
        header.append(str(int(alpha*100)))
    np.savetxt(output, out, delimiter=',', header=','.join(header), comments='')


def OD_non_routed_costs(alphas, net, net2, demand, inputs, output, verbose=0):
    '''
    from input files of equilibrium flows for the heterogeneous game
    outputs the travel times of non-routed users
    net  : network with travel time cost functions
    net2 : network with perseived cost functions
    '''
    od = construct_od(demand)
    num_ods = demand.shape[0]
    out = np.zeros((num_ods, len(alphas)+2))
    out[:,:2] = demand[:,:2]
    g = construct_igraph(net)
    for i, alpha in enumerate(alphas):
        fs = np.loadtxt(inputs.format(int(alpha*100)), delimiter=',', skiprows=1)
        c = cost(np.sum(fs, axis=1), net2) # vector of non-routed edge costs
        g.es["weight"] = c.tolist() 
        tt = cost(np.sum(fs, axis=1), net) # vector of edge travel times
        # import pdb; pdb.set_trace()
        if verbose >= 1: 
            print 'computing OD costs for alpha = {} ...'.format(alpha)
        costs = path_cost_non_routed(net2, c, tt, demand, g, od)
        for j in range(num_ods):
            out[j,i+2] = costs[(int(out[j,0]), int(out[j,1]))]
    header = ['o,d']
    for alpha in alphas: 
        header.append(str(int(alpha*100)))
    np.savetxt(output, out, delimiter=',', header=','.join(header), comments='')


def free_flow_OD_costs(net, costs, demand, output, verbose=0):
    '''
    do all-or-nothing assignments following list of arc costs 'costs'
    output OD costs under arc costs contained in 'net'
    '''
    od = construct_od(demand)
    num_ods = demand.shape[0]
    out = np.zeros((num_ods, len(costs)+3))
    out[:,:2] = demand[:,:2]
    g = construct_igraph(net)
    out[:,2] = demand[:,2]
    for i,c in enumerate(costs):
        if verbose >= 1: 
            print 'computing OD costs for {}-eme cost vector ...'.format(i+1)
        cost = path_cost_non_routed(net, c, net[:,3], demand, g, od)
        for j in range(num_ods):
            out[j,i+3] = cost[(int(out[j,0]), int(out[j,1]))]
    header = ['o,d,demand'] + [str(i) for i in range(len(costs))]
    np.savetxt(output, out, delimiter=',', header=','.join(header), comments='')

