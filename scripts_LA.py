__author__ = "Jerome Thai, Nicolas Laurent"
__email__ = "jerome.thai@berkeley.edu"

'''
Scripts for LA network
'''

import numpy as np
from process_data import process_net, process_trips, extract_features, process_links, \
    geojson_link, construct_igraph, construct_od
from frank_wolfe_2 import solver, solver_2, solver_3
from multi_types_solver import gauss_seidel
from metrics import average_cost_all_or_nothing, all_or_nothing_assignment, \
    cost_ratio, cost


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


def remove_loops_in_LA_od():
    out = ['O,D,demand\n']
    demand = np.loadtxt('data/LA_od.csv', delimiter=',', skiprows=1)
    for row in range(demand.shape[0]):
        o = int(demand[row,0])
        d = int(demand[row,1])
        if o != d:
            out.append('{},{},{}\n'.format(o,d,demand[row,2]))
    with open('data/LA_od.csv', 'w') as f:
        f.write(''.join(out))


def load_LA():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    return graph, demand, node


def load_LA_2():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od_2.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    features = extract_features('data/LA_net.txt')
    features[10787,0] = features[10787,0] * 1.5
    graph[10787,-1] = graph[10787,-1] / (1.5**4)
    features[3348,:] = features[3348,:] * 1.2
    graph[3348,-1] = graph[3348,-1] / (1.2**4)
    return graph, demand, node, features


def check__LA_connectivity():
    graph, demand, node = load_LA()
    print np.min(graph[:,1:3])
    print np.max(graph[:,1:3])
    print np.min(demand[:,:2])
    print np.max(demand[:,:2])
    od = construct_od(demand)
    g = construct_igraph(graph)
    f = np.zeros((graph.shape[0],))
    print average_cost_all_or_nothing(f, graph, demand)


def frank_wolfe_on_LA():
    graph, demand, node, features = load_LA_2()
    demand[:,2] = demand[:,2] / 4000.
    f = solver_3(graph, demand, max_iter=1000, q=50, display=1, stop=1e-2)
    np.savetxt('data/LA/LA_output_4.csv', f, delimiter=',')


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
    net, demand, node, features = load_LA_2()
    demand[:,2] = demand[:,2] / 4000.
    f = np.loadtxt('data/LA/LA_output_4.csv', delimiter=',', skiprows=0)
    costs = cost(f, net)
    cr = cost_ratio(f, net)
    print np.sort(cr)[-20:]
    for row in range(net.shape[0]):
        if cr[row] >= 10.: 
            print cr[row]
            print net[row,:3], features[row,:]
    L = all_or_nothing_assignment(costs, net, demand)
    print costs.dot(L) / np.sum(demand[:,2])


def reduce_demand():
    net, demand, node = load_LA()
    features = extract_features('data/LA_net.txt')
    f = np.loadtxt('data/LA/LA_output_3.csv', delimiter=',', skiprows=0)
    cr = cost_ratio(f, net)
    for row in range(net.shape[0]):
        if cr[row] >= 10.: 
            out = []
            for i in range(demand.shape[0]):
                if int(demand[i,0]) == int(net[row,1]):
                    out.append(demand[i,2])
                    demand[i,2] = demand[i,2] / 10.
            if len(out) > 0:
                out = np.array(out)
                print '\nratio:', cr[row]
                print 'origin: {}\nflow: {}'.format(int(demand[i,0]), np.sum(out))
                print np.sort(out).tolist()

    for row in range(net.shape[0]):
        if cr[row] >= 10.: 
            out = []
            for i in range(demand.shape[0]):
                if int(demand[i,1]) == int(net[row,2]):
                    out.append(demand[i,2])
                    demand[i,2] = demand[i,2] / 10.

            if len(out) > 0:
                out = np.array(out)
                print '\nratio:', cr[row]
                print 'destination: {}\nflow: {}'.format(int(demand[i,0]), np.sum(out))
                print np.sort(out).tolist()

    # np.savetxt('data/LA_od_2.csv', demand, delimiter=',', header='O,D,flow')


def increase_capacity():
    net, demand, node = load_LA()
    f = np.loadtxt('data/LA/LA_output_3.csv', delimiter=',', skiprows=0)
    cr = cost_ratio(f, net)

        

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


def main():
    # process_LA_node()
    # process_LA_net()
    visualize_LA_capacity()
    # visualize_LA_result()
    # process_LA_od()
    # frank_wolfe_on_LA()
    # check_LA_result()
    # LA_parametric_study()
    # check__LA_connectivity()
    # remove_loops_in_LA_od()
    # reduce_demand()
    # load_LA_2()

if __name__ == '__main__':
    main()