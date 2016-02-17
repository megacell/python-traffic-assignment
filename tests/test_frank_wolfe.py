__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from frank_wolfe import solver, shift_polynomial, \
    shift_graph, gauss_seidel, jacobi, potential, line_search, \
    solver_2


class TestFrankWolfe(unittest.TestCase):

    def test_solver(self):
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        f = solver(graph, demand, max_iter=300)
        # current implementation of Frank-Wolfe need a lof of iterations
        print 'error w/o line_search', np.linalg.norm(f - np.array([1.,1.,0.,1.,1.]))
        self.assertTrue(np.linalg.norm(f - np.array([1.,1.,0.,1.,1.])) < 1e-2)

        # modify demand
        demand[0,2] = 0.5
        f = solver(graph, demand)
        print 'error w/o line_search', np.linalg.norm(f - np.array([.5,.0,.5,.0,.5]))
        self.assertTrue(np.linalg.norm(f - np.array([.5,.0,.5,.0,.5])) < 1e-8)


    def test_solver_2(self):
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        f = solver_2(graph, demand, max_iter=100)
        # Frank-Wolfe with line-search for the last iterations is good
        print 'error with line_search', np.linalg.norm(f - np.array([1.,1.,0.,1.,1.]))
        self.assertTrue(np.linalg.norm(f - np.array([1.,1.,0.,1.,1.])) < 1e-3)

        # modify demand
        demand[0,2] = 0.5
        f = solver_2(graph, demand)
        print 'error with line_search', np.linalg.norm(f - np.array([.5,.0,.5,.0,.5]))
        self.assertTrue(np.linalg.norm(f - np.array([.5,.0,.5,.0,.5])) < 1e-8)


    def test_shift_polynomial(self):
        b = shift_polynomial(np.array([1.,2.,3.,2.,1.]),2.)
        a = np.array([49.,70.,39.,10.,1.])
        self.assertTrue(np.linalg.norm(a-b)<1e-12)


    def test_shift_graph(self):
        graph1 = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        graph1[:,5] = np.array([2.]*5)
        graph2 = np.copy(graph1)
        d = np.array([0.,1.,2.,3.,4.])
        shift_graph(graph1, graph2, d)
        #print graph1
        #print graph2


    def test_gauss_seidel(self):
        g2 = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        g1 = np.copy(g2)
        g1[2,3] = 1e8
        d1 = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        # routed = .25, non-routed = .25
        d1[0,2] = 0.25
        d2 = np.copy(d1)
        d2[0,2] = 0.25
        fs = gauss_seidel([g1,g2], [d1,d2], max_iter=200)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.assertTrue(np.linalg.norm(fs - a) < 1e-1)
        # routed = 1., non-routed = 1.
        d1[0,2] = 1.
        d2[0,2] = 1.
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = gauss_seidel([g1,g2], [d1,d2], max_iter=200) 
        self.assertTrue(np.linalg.norm(fs - a) < 1e-1)
        # routed = .75, non-routed = .75
        d1[0,2] = .75
        d2[0,2] = .75
        fs = gauss_seidel([g1,g2], [d1,d2], max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.assertTrue(np.linalg.norm(fs - a) < 1e-1)


    def test_jacobi(self):
        g2 = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        g1 = np.copy(g2)
        g1[2,3] = 1e8
        d1 = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        # routed = .25, non-routed = .25
        d1[0,2] = 0.25
        d2 = np.copy(d1)
        d2[0,2] = 0.25
        fs = jacobi([g1,g2], [d1,d2], max_iter=200)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.assertTrue(np.linalg.norm(fs - a) < 1e-1)
        # routed = 1., non-routed = 1.
        d1[0,2] = 1.
        d2[0,2] = 1.
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = jacobi([g1,g2], [d1,d2], max_iter=200) 
        self.assertTrue(np.linalg.norm(fs - a) < 1e-1)
        # routed = .75, non-routed = .75
        d1[0,2] = .75
        d2[0,2] = .75
        fs = jacobi([g1,g2], [d1,d2], max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.assertTrue(np.linalg.norm(fs - a) < 1e-1)


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