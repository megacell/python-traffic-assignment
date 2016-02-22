__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
Various scripts for processing data
'''

import numpy as np
from process_data import extract_features, process_links, geojson_link, \
    process_trips, process_net, process_node, array_to_trips, process_results
from metrics import average_cost, cost_ratio


def test_anaheim(self):
    print 'test Frank-Wolfe on Anaheim'
    graph = np.loadtxt('data/Anaheim_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/Anaheim_od.csv', delimiter=',', skiprows=1)        
    demand[:,2] = demand[:,2] / 4000
    f = solver(graph, demand, max_iter=1000)
    # print f.shape
    results = np.loadtxt('data/Anaheim_results.csv')
    print np.linalg.norm(f*4000 - results) / np.linalg.norm(results)
    # print f*4000


def process_chicago_network():
    '''
    prepare .csv files for our algorithm from .txt files available in
    http://www.bgu.ac.il/~bargera/tntp/
    '''
    process_trips('data/ChicagoSketch_trips.txt', 'data/Chicago_od.csv')
    process_net('data/ChicagoSketch_net.txt', 'data/Chicago_net.csv')
    input = 'data/ChicagoSketch_node.csv'
    output = 'data/Chicago_node.csv'
    max_X = -87.110063
    min_X = -88.9242653
    max_Y = 42.711908
    min_Y = 40.946233
    process_node(input, output, min_X, max_X, min_Y, max_Y)


def capacities_of_chicago():
    '''
    visualize capacities in the network of Chicago
    '''
    net = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/Chicago_node.csv', delimiter=',', skiprows=1)
    features = extract_features('data/ChicagoSketch_net.txt')
    links = process_links(net, node, features)
    color = features[:,0] / 2000. # we choose the capacity
    geojson_link(links, ['capacity', 'length', 'fftt'], color)


def multiply_demand_by_2():
    '''
    Multiply demand in Chicago by 2 and generate input file for Bar-Gera
    '''
    demand = np.loadtxt('data/Chicago_od.csv', delimiter=',', skiprows=1)
    demand[:,2] = 2.*demand[:,2]
    array_to_trips(demand, 'data/ChicagoSketch_trips_2.txt')


def results_for_chicago():
    '''
    Take Bar-gera results and check the link flows are aligned with Chicago_net.csv
    '''
    process_results('data/Chicago_raw_results_2.csv', 'data/Chicago_results_2.csv',\
        'data/Chicago_net.csv')


def frank_wolfe_on_chicago():
    '''
    Frank-Wolfe on Chicago with the inputs processed from:
    http://www.bgu.ac.il/~bargera/tntp/
    '''
    graph = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/Chicago_od.csv', delimiter=',', skiprows=1)
    results = np.loadtxt('data/Chicago_results.csv', delimiter=',', skiprows=1)     
    demand[:,2] = demand[:,2] / 4000
    f = solver(graph, demand, max_iter=1000, display=1)
    # error: 0.00647753330249, time: 664.151s
    # f = solver_2(graph, demand, max_iter=1000, q=100, display=1)
    # error: 0.00646125552755, time: 664.678s
    # f = solver_3(graph, demand, max_iter=1000, r=200, display=1)
    # error: 0.00648532089623, time: 665.074s
    print np.linalg.norm(f*4000 - results[:,2]) / np.linalg.norm(results[:,2])


def frank_wolfe_on_chicago_2():
    '''
    Frank-Wolfe on Chicago with the inputs processed from:
    http://www.bgu.ac.il/~bargera/tntp/
    but we multiply the demand by 2 to have more congestion
    '''    
    print 'test Chicago_2'
    graph = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/Chicago_od.csv', delimiter=',', skiprows=1)
    results = np.loadtxt('data/Chicago_results_2.csv', delimiter=',') 
    demand[:,2] = demand[:,2] / 2000 # technically, it's 2*demand/4000
    f = solver(graph, demand, max_iter=1000, display=1)
    print np.linalg.norm(f*4000 - results) / np.linalg.norm(results)


def equilibrium_in_chicago():
    '''
    visualize costs in the network of Chicago
    '''
    net = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/Chicago_node.csv', delimiter=',', skiprows=1)
    flow = np.loadtxt('data/Chicago_results_2.csv', delimiter=',')
    # flow = np.loadtxt('data/Chicago_results.csv', delimiter=',', skiprows=1)[:,2]
    print average_cost(flow/4000., net)
    costs = cost_ratio(flow/4000., net)
    f = extract_features('data/ChicagoSketch_net.txt')
    features = np.zeros((f.shape[0],4))
    features[:,:3] = f
    features[:,3] = costs
    links = process_links(net, node, features)
    color = features[:,3] - 1.0 # we choose the costs
    geojson_link(links, ['capacity', 'length', 'fftt', 'tt_over_fftt'], color)


def main():
    # process_chicago_network()
    # capacities_of_chicago()
    equilibrium_in_chicago()
    # multiply_demand_by_2()
    # results_for_chicago()
    # frank_wolfe_on_chicago()
    # frank_wolfe_on_chicago_2()

if __name__ == '__main__':
    main()