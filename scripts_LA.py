__author__ = "Jerome Thai, Nicolas Laurent"
__email__ = "jerome.thai@berkeley.edu"

'''
Scripts for LA network
'''

import numpy as np
from process_data import process_net, process_trips, extract_features, process_links, \
    geojson_link
from frank_wolfe import solver, solver_2, solver_3


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


def frank_wolfe_on_LA():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od.csv', delimiter=',', skiprows=1)
    demand[:,2] = demand[:,2] / 4000
    f = solver_3(graph, demand, max_iter=1000, q=50, display=1, stop=1e-2)
    print f*4000.
    np.savetxt('data/LA_output.csv', f*4000., delimiter=',')


def visualize_LA():
    graph = np.loadtxt('data/LA_net.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    features = extract_features('data/LA_net.txt')
    links = process_links(graph, node, features, in_order=True)
    color = features[:,0] # we choose the capacities
    names = ['capacity', 'length', 'fftt']
    color = features[:,0] / 2000.
    geojson_link(links, names, color)




def main():
    # process_LA_node()
    # process_LA_net()
    visualize_LA()
    # process_LA_od()
    # frank_wolfe_on_LA()
    pass


if __name__ == '__main__':
    main()