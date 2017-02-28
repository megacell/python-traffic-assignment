__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
Various scripts for processing data
'''

import numpy as np
from process_data import extract_features, process_links, geojson_link, \
    process_trips, process_net, process_node, array_to_trips, process_results
from metrics import average_cost, cost_ratio, cost, save_metrics
from frank_wolfe import solver, solver_2, solver_3
from heterogeneous_solver import gauss_seidel, jacobi
from All_Or_Nothing import all_or_nothing


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


def braess_heterogeneous(demand_r, demand_nr):
    # generate heteregenous game on Braess network
    g_r = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
    g_nr = np.copy(g_r)
    g_nr[2,3] = 1e8
    d_nr = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
    d_nr = d_nr.reshape((1, 3))
    d_nr[0,2] = demand_nr
    d_r = np.copy(d_nr)
    d_r[0,2] = demand_r
    return g_nr, g_r, d_nr, d_r


def braess_parametric_study():
    '''
    parametric study of heterogeneous game on the Braess network 
    '''
    g1,g2,d1,d2 = braess_heterogeneous(.0, 1.5)
    fs = solver_2(g1, d1, display=1)
    print '.0, 1.5'
    np.savetxt('data/braess/test_1.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(.5, 1.)
    fs = gauss_seidel([g1,g2], [d1,d2], solver_2, display=1)
    print '.5, 1.'
    np.savetxt('data/braess/test_2.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(.75, .75)
    fs = gauss_seidel([g1,g2], [d1,d2], solver_2, display=1)
    print '.75, .75'
    np.savetxt('data/braess/test_3.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(1., .5)
    fs = gauss_seidel([g1,g2], [d1,d2], solver_2, display=1)
    print '1., .5'
    np.savetxt('data/braess/test_4.csv', fs, delimiter=',')
    g1,g2,d1,d2 = braess_heterogeneous(1.5, .0)
    fs = solver_2(g2, d2, display=1)
    print '1.5, .0'
    np.savetxt('data/braess/test_5.csv', fs, delimiter=',')


def main():
    braess_parametric_study()


if __name__ == '__main__':
    main()
