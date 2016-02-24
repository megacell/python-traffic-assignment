__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
Various scripts for processing data
'''

import numpy as np
from process_data import extract_features, process_links, geojson_link, \
    process_trips, process_net, process_node, array_to_trips, process_results
from metrics import average_cost, cost_ratio, cost
from frank_wolfe import solver, solver_2, solver_3
from heterogeneous_solver import gauss_seidel, jacobi


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
    # f = solver_3(graph, demand, max_iter=1000, q=200, display=1)
    # error: 0.00648532089623, time: 665.074s
    print np.linalg.norm(f*4000 - results[:,2]) / np.linalg.norm(results[:,2])


def frank_wolfe_on_chicago_2():
    '''
    Frank-Wolfe on Chicago with the inputs processed from:
    http://www.bgu.ac.il/~bargera/tntp/
    but we multiply the demand by 2 to have more congestion
    '''    
    graph = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/Chicago_od.csv', delimiter=',', skiprows=1)
    results = np.loadtxt('data/Chicago_results_2.csv', delimiter=',') 
    demand[:,2] = demand[:,2] / 2000 # technically, it's 2*demand/4000
    # f = solver(graph, demand, max_iter=1000, display=1, stop=1e-2)
    # f = solver_2(graph, demand, max_iter=1000, q=100, display=1, stop=1e-2)
    f = solver_3(graph, demand, max_iter=1000, q=50, display=1, stop=1e-2)
    print np.linalg.norm(f*4000 - results) / np.linalg.norm(results)
    print average_cost(f, graph, demand)


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


def braess_heterogeneous(demand_r, demand_nr):
    # generate heteregenous game on Braess network
    g_r = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
    g_nr = np.copy(g_r)
    g_nr[2,3] = 1e8
    d_nr = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
    d_nr[0,2] = demand_nr
    d_r = np.copy(d_nr)
    d_r[0,2] = demand_r
    return g_nr, g_r, d_nr, d_r


def braess_parametric_study():
    '''
    parametric study of heterogeneous game on the Braess network 
    '''
    g1,g2,d1,d2 = braess_heterogeneous(.0, 1.5)
    fs = solver_2(g1, d1)
    print '.0, 1.5'
    np.savetxt('data/test_1.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(.5, 1.)
    fs = gauss_seidel([g1,g2], [d1,d2], solver_2)
    print '.5, 1.'
    np.savetxt('data/test_2.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(.75, .75)
    fs = gauss_seidel([g1,g2], [d1,d2], solver_2)
    print '.75, .75'
    np.savetxt('data/test_3.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(1., .5)
    fs = gauss_seidel([g1,g2], [d1,d2], solver_2)
    print '1., .5'
    np.savetxt('data/test_4.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(1.5, .0)
    fs = solver_2(g2, d2)
    print '1.5, .0'
    np.savetxt('data/test_5.csv', fs, delimiter=',')


def heterogeneous_demand(d, alpha):
    d_nr = np.copy(d)
    d_r = np.copy(d)
    d_nr[:,2] = (1-alpha) * d_nr[:,2]
    d_r[:,2] = alpha * d_r[:,2]
    return d_nr, d_r


def chicago_parametric_study():
    '''
    parametric study of heterogeneous game on Chicago sketch network
    save into test_*.csv files
    '''
    # graphs
    g_r = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    g_nr = np.copy(g_r)
    features = extract_features('data/ChicagoSketch_net.txt')
    for row in range(g_nr.shape[0]):
        if features[row,0] < 2000.:
            g_nr[row,3] = g_nr[row,3] + 100.
    # demand
    d = np.loadtxt('data/Chicago_od.csv', delimiter=',', skiprows=1)
    d[:,2] = d[:,2] / 2000 # technically, it's 2*demand/4000

    # print 'non-routed = 1.0, routed = 0.0'
    # fs = solver_2(g_nr, d, max_iter=1000, q=100, display=1)    
    # np.savetxt('data/test_1.csv', fs, delimiter=',')
    
    # print 'non-routed = .75, routed = .25'
    # d_nr, d_r = heterogeneous_demand(d, .25)
    # fs = gauss_seidel([g_nr,g_r], [d_nr,d_r], solver_3, max_iter=1000, display=1,\
    #     stop=1e-2, q=50)
    # np.savetxt('data/test_2.csv', fs, delimiter=',')

    print 'non-routed = .5, routed = .5'
    d_nr, d_r = heterogeneous_demand(d, .5)
    fs = gauss_seidel([g_nr,g_r], [d_nr,d_r], solver_3, max_iter=1000, display=1,\
        stop=1e-2, q=50)
    np.savetxt('data/test_3.csv', fs, delimiter=',')

    # print 'non-routed = .25, routed = .75'
    # d_nr, d_r = heterogeneous_demand(d, .75)
    # fs = gauss_seidel([g_nr,g_r], [d_nr,d_r], solver_3, max_iter=1000, display=1,\
    #     stop=1e-2, q=50)
    # np.savetxt('data/test_4.csv', fs, delimiter=',')

    # print 'non-routed = 0.0, routed = 1.0'
    # fs = solver_3(g_r, d, max_iter=1000, q=100, display=1, stop=1e-2)    
    # np.savetxt('data/test_5.csv', fs, delimiter=',')


def chicago_metrics():
    '''
    study the test_*.csv files
    '''
    net = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    d = np.loadtxt('data/Chicago_od.csv', delimiter=',', skiprows=1)
    d[:,2] = d[:,2] / 2000 # technically, it's 2*demand/4000

    print 'only non-routed users'
    f = np.loadtxt('data/test_1.csv', delimiter=',', skiprows=0)
    print average_cost(f, net, d)

    alpha = .25
    print 'avg tt for {} non-routed and {} routed'.format(1-alpha, alpha)
    fs = np.loadtxt('data/test_2.csv', delimiter=',', skiprows=0)
    f = np.sum(fs, axis=1)
    print cost(f, net).dot(fs[:,0]) / np.sum((1-alpha)*d[:,2])
    print cost(f, net).dot(fs[:,1]) / np.sum(alpha*d[:,2])

    alpha = .5
    print 'avg tt for {} non-routed and {} routed'.format(1-alpha, alpha)
    fs = np.loadtxt('data/test_3.csv', delimiter=',', skiprows=0)
    f = np.sum(fs, axis=1)
    print cost(f, net).dot(fs[:,0]) / np.sum((1-alpha)*d[:,2])
    print cost(f, net).dot(fs[:,1]) / np.sum(alpha*d[:,2])

    alpha = .75
    print 'avg tt for {} non-routed and {} routed'.format(1-alpha, alpha)
    fs = np.loadtxt('data/test_4.csv', delimiter=',', skiprows=0)
    f = np.sum(fs, axis=1)
    print cost(f, net).dot(fs[:,0]) / np.sum((1-alpha)*d[:,2])
    print cost(f, net).dot(fs[:,1]) / np.sum(alpha*d[:,2])

    print 'only routed users'
    f = np.loadtxt('data/test_5.csv', delimiter=',', skiprows=0)
    print average_cost(f, net, d)



def main():
    # process_chicago_network()
    # capacities_of_chicago()
    # equilibrium_in_chicago()
    # multiply_demand_by_2()
    # results_for_chicago()
    # frank_wolfe_on_chicago()
    # frank_wolfe_on_chicago_2()
    # braess_parametric_study()
    # chicago_parametric_study()
    chicago_metrics()

if __name__ == '__main__':
    main()