__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from frank_wolfe import solver, potential, line_search, solver_2, solver_3


class TestFrankWolfe(unittest.TestCase):


    def check(self, f, true, eps):
        error = np.linalg.norm(f - true) / np.linalg.norm(true)
        print 'error', error
        self.assertTrue(error < eps)


    def test_solver(self):
        # Frank-Wolfe from Algorithm 1 of Jaggi's paper
        print 'test solver'
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        demand=np.reshape(demand, (1,3))
        f = solver(graph, demand, max_iter=300)
        self.check(f, np.array([1.,1.,0.,1.,1.]), 1e-2)

        # modify demand
        demand[0,2] = 0.5
        f = solver(graph, demand)
        self.check(f, np.array([.5,.0,.5,.0,.5]), 1e-8)


    def test_solver_2(self):
        # Frank-Wolfe from Algorithm 3 of Jaggi's paper (without aprox.)
        # already good improvement
        print 'test solver_2'
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        demand=np.reshape(demand, (1,3))
        f = solver_2(graph, demand, max_iter=100)
        self.check(f, np.array([1.,1.,0.,1.,1.]), 1e-3)

        # modify demand
        demand[0,2] = 0.5
        f = solver_2(graph, demand)
        self.check(f, np.array([.5,.0,.5,.0,.5]), 1e-8)


    def test_solver_3(self):
        print 'test_solver_3'
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        demand=np.reshape(demand, (1,3))
        f = solver_3(graph, demand, max_iter=100)
        #print f
        self.check(f, np.array([1.,1.,0.,1.,1.]), 1e-1)
        # modify demand
        demand[0,2] = 0.5
        f = solver_2(graph, demand)
        self.check(f, np.array([.5,.0,.5,.0,.5]), 1e-8)


    def test_solver_sioux_falls(self):
        print 'test Frank-Wolfe on Sioux Falls'
        graph = np.loadtxt('data/SiouxFalls_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/SiouxFalls_od.csv', delimiter=',', skiprows=1)
        demand[:,2] = demand[:,2] / 4000
        f = solver(graph, demand, max_iter=1000)
        results = np.loadtxt('data/SiouxFalls_results.csv')
        self.check(f*4000, results, 1e-3)


    def test_solver_sioux_falls_2(self):
        print 'test Frank-Wolfe on Sioux Falls 2'
        graph = np.loadtxt('data/SiouxFalls_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/SiouxFalls_od.csv', delimiter=',', skiprows=1)
        demand[:,2] = demand[:,2] / 4000
        f = solver_2(graph, demand, max_iter=1000, q=100)
        results = np.loadtxt('data/SiouxFalls_results.csv')
        self.check(f*4000, results, 1e-3)


    def test_solver_sioux_falls_3(self):
        print 'test Frank-Wolfe on Sioux Falls 3'
        graph = np.loadtxt('data/SiouxFalls_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/SiouxFalls_od.csv', delimiter=',', skiprows=1)
        demand[:,2] = demand[:,2] / 4000
        f = solver_3(graph, demand, max_iter=1000)
        results = np.loadtxt('data/SiouxFalls_results.csv')
        self.check(f*4000, results, 1e-3)


    def test_potential(self):
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        graph[:,5] = np.array([2.]*5)
        #print graph
        out = potential(graph, np.array([2.,2.,2.,2.,2.]))
        self.assertTrue(np.linalg.norm(out - 34.666666666) < 1e-5)


    def test_line_search(self):
        def f(x):
            return (x-0.3)**2
        out = line_search(f)
        self.assertTrue(np.linalg.norm(out - .3) < 1e-5)


if __name__ == '__main__':
    unittest.main()