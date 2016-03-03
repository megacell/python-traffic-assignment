__author__ = "Jerome Thai, Nicolas Laurent"
__email__ = "jerome.thai@berkeley.edu"

'''
Scripts for LA network
'''

import numpy as np
from process_data import process_net, process_trips, extract_features, process_links, \
    geojson_link
from frank_wolfe import solver, solver_2, solver_3
from metrics import cost, all_or_nothing_assignment, ratio_subset, average_cost, \
    average_cost_all_or_nothing
from heterogeneous_solver import gauss_seidel, jacobi


def process_LA_node():
    lines = open("data/LA_node.txt", "r").readlines()
    code = 'data=' + lines[0]
    exec code
    array = np.zeros((len(data), 3))
    for node in data:
        array[int(node[1]['nid'])-1, 0] = node[1]['nid']
        array[int(node[1]['nid'])-1, 1] = node[1]['coords'][1]
        array[int(node[1]['nid'])-1, 2] = node[1]['coords'][0]
    np.savetxt('data/LA_node.csv', array, delimiter=',')


def process_LA_net():
    process_net('data/LA_net.txt', 'data/LA_net.csv')


def process_LA_od():
    process_trips('data/LA_od.txt', 'data/LA_od.csv')


def load_LA():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    return graph, demand, node

def frank_wolfe_on_LA():
    graph, demand, node = load_LA()
    demand[:,2] = demand[:,2] / 4000
    f = solver_3(graph, demand, max_iter=1000, q=50, display=1, stop=1e-2)
    print f*4000.
    np.savetxt('data/LA_output.csv', f*4000., delimiter=',')


def visualize_LA_capacity():
    graph, demand, node = load_LA()
    features = extract_features('data/LA_net.txt')
    links = process_links(graph, node, features, in_order=True)
    color = features[:,0] # we choose the capacities
    names = ['capacity', 'length', 'fftt']
    color = 2.1 * features[:,0] / 2000.
    geojson_link(links, names, color)


def visualize_LA_result():
    net, demand, node = load_LA()
    f = np.loadtxt('data/LA_output.csv', delimiter=',', skiprows=0)
    features = np.zeros((f.shape[0], 4))
    features[:,:3] = extract_features('data/LA_net.txt')
    f = np.divide(f, features[:,0])
    features[:,3] = f
    links = process_links(net, node, features, in_order=True)
    color = 2.0*f + 1.0
    geojson_link(links, ['capacity', 'length', 'fftt', 'flow_over_capacity'], color)


def check_LA_result():
    net, demand, node = load_LA()
    demand[:,2] = demand[:,2] / 4000
    f = np.loadtxt('data/LA_output.csv', delimiter=',', skiprows=0)
    #f = np.zeros((f.shape[0],))
    costs = cost(f/4000., net)
    L = all_or_nothing_assignment(costs, net, demand)
    print costs.dot(L) / np.sum(demand[:,2])
    # 1312s = 22min for free-flow travel times
    # 2771s = 46min for equilibrium travel times (routed users only)


def heterogeneous_demand(d, alpha):
    d_nr = np.copy(d)
    d_r = np.copy(d)
    d_nr[:,2] = (1-alpha) * d_nr[:,2]
    d_r[:,2] = alpha * d_r[:,2]
    return d_nr, d_r


def LA_parametric_study():
    g_r, d, node = load_LA()
    d[:,2] = d[:,2] / 4000.
    g_nr = np.copy(g_r)
    features = extract_features('data/LA_net.txt')
    for row in range(g_nr.shape[0]):
        if features[row,0] < 1000.:
            g_nr[row,3] = g_nr[row,3] + 3000.

    # print 'non-routed = 1.0, routed = 0.0'
    # fs = solver_3(g_nr, d, max_iter=1000, q=100, display=1, stop=1e-2)    
    # np.savetxt('data/LA_result_0.csv', fs, delimiter=',')

    print 'non-routed = 0.0, routed = 1.0'
    fs = solver_3(g_r, d, max_iter=1000, q=100, display=1, stop=1e-2)    
    np.savetxt('data/LA_result_100.csv', fs, delimiter=',')

    # alpha = 0.9
    # print 'non-routed = {}, routed = {}'.format(1-alpha, alpha)
    # d_nr, d_r = heterogeneous_demand(d, alpha)
    # fs = gauss_seidel([g_nr,g_r], [d_nr,d_r], solver_3, max_iter=1000, display=1,\
    #     stop=1e-2, q=50, stop_cycle=1e-3)
    # np.savetxt('data/LA_result_{}.csv'.format(int(alpha*100)), fs, delimiter=',')


def check_LA_result_heterogeneous():

    net, d, node = load_LA()
    d[:,2] = d[:,2] / 4000.
    net2 = np.copy(net)
    features = extract_features('data/LA_net.txt')
    small_capacity = np.zeros((net2.shape[0],))
    for row in range(net2.shape[0]):
        if features[row,0] < 1000.:
            small_capacity[row] = 1.0
            net2[row,3] = net2[row,3] + 3000.

    alpha = .0 
    print 'non-routed = {}, routed = {}'.format(1-alpha, alpha)
    f = np.loadtxt('data/LA_result_0.csv', delimiter=',', skiprows=0)
    print average_cost(f, net, d)
    print average_cost_all_or_nothing(f, net, d)
    print ratio_subset(f, net, small_capacity)

    for alpha in [.1,.2,.3,.4,.5,.6,.7,.8,.9]:
    # for alpha in [.1,.2,.3,.4,.5]:
        print 'non-routed = {}, routed = {}'.format(1-alpha, alpha)
        fs = np.loadtxt('data/LA_result_{}.csv'.format(int(alpha*100)), delimiter=',', skiprows=0)
        f = np.sum(fs, axis=1)
        print cost(f, net).dot(fs[:,0]) / np.sum((1-alpha)*d[:,2])
        print cost(f, net).dot(fs[:,1]) / np.sum(alpha*d[:,2])
        print ratio_subset(f, net, small_capacity)

    alpha = 1. 
    print 'non-routed = {}, routed = {}'.format(1-alpha, alpha)
    f = np.loadtxt('data/LA_result_100.csv', delimiter=',', skiprows=0)
    # f = np.loadtxt('data/LA_output.csv', delimiter=',', skiprows=0) / 4000.
    L = all_or_nothing_assignment(cost(f, net2), net, d)
    print cost(f, net).dot(L) / np.sum(d[:,2])
    print average_cost(f, net, d)
    print average_cost_all_or_nothing(f, net, d)
    print ratio_subset(f, net, small_capacity)


def main():
    # process_LA_node()
    # process_LA_net()
    # visualize_LA_capacity()
    # visualize_LA_result()
    # process_LA_od()
    # frank_wolfe_on_LA()
    # check_LA_result()
    # LA_parametric_study()
    check_LA_result_heterogeneous()


if __name__ == '__main__':
    main()