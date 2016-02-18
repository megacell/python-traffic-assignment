__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from frank_wolfe import solver, solver_2, solver_3


class TestFrankWolfeOnLargeNetworks(unittest.TestCase):

    # def test_anaheim(self):
    #     print 'test Frank-Wolfe on Anaheim'
    #     graph = np.loadtxt('data/Anaheim_net.csv', delimiter=',', skiprows=1)
    #     demand = np.loadtxt('data/Anaheim_od.csv', delimiter=',', skiprows=1)        
    #     demand[:,2] = demand[:,2] / 4000
    #     f = solver(graph, demand, max_iter=1000)
    #     # print f.shape
    #     results = np.loadtxt('data/Anaheim_results.csv')
    #     print np.linalg.norm(f*4000 - results) / np.linalg.norm(results)
    #     # print f*4000


    def test_chicago(self):
        print 'test Chicago'
        graph = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/Chicago_od.csv', delimiter=',', skiprows=1)
        results = np.loadtxt('data/Chicago_results.csv', delimiter=',', skiprows=1)     
        demand[:,2] = demand[:,2] / 4000
        # f = solver(graph, demand, max_iter=1000, display=1)
        # error: 0.00647753330249, time: 664.151s
        # f = solver_2(graph, demand, max_iter=1000, q=100, display=1)
        # error: 0.00646125552755, time: 664.678s
        f = solver_3(graph, demand, max_iter=1000, r=200, display=1)
        # error:, time:
        print np.linalg.norm(f*4000 - results[:,2]) / np.linalg.norm(results[:,2])


if __name__ == '__main__':
    unittest.main()