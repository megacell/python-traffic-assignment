__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from frank_wolfe import solver, shift_polynomial, \
    shift_graph, gauss_seidel, jacobi, potential, line_search, \
    solver_2


class TestFrankWolfe(unittest.TestCase):


    def check(self, f, true, eps):
        error = np.linalg.norm(f - true)
        print 'error', error
        self.assertTrue(error < eps)


    def test_solver(self):
        # Frank-Wolfe from Algorithm 1 of Jaggi's paper
        print 'test solver'
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
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
        f = solver_2(graph, demand, max_iter=100)
        self.check(f, np.array([1.,1.,0.,1.,1.]), 1e-3)

        # modify demand
        demand[0,2] = 0.5
        f = solver_2(graph, demand)
        self.check(f, np.array([.5,.0,.5,.0,.5]), 1e-8)


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


    def braess_heterogeneous(self, demand_r, demand_nr):
        # generate heteregenous game on Braess network
        g2 = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        g1 = np.copy(g2)
        g1[2,3] = 1e8
        d1 = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        d1[0,2] = demand_nr
        d2 = np.copy(d1)
        d2[0,2] = demand_r
        return g1, g2, d1, d2


    def test_gauss_seidel(self):
        print 'test gauss_seidel'
        g1,g2,d1,d2 = self.braess_heterogeneous(.25, .25)
        fs = gauss_seidel([g1,g2], [d1,d2], solver, max_iter=200)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-1)
        g1,g2,d1,d2 = self.braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = gauss_seidel([g1,g2], [d1,d2], solver, max_iter=200) 
        self.check(fs, a, 1e-1)      
        g1,g2,d1,d2 = self.braess_heterogeneous(.75, .75)
        fs = gauss_seidel([g1,g2], [d1,d2], solver, max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-1)


    def test_jacobi(self):
        print 'test jacobi'
        g1,g2,d1,d2 = self.braess_heterogeneous(.25, .25)
        fs = jacobi([g1,g2], [d1,d2], solver, max_iter=200)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-1)       
        g1,g2,d1,d2 = self.braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = jacobi([g1,g2], [d1,d2], solver, max_iter=200) 
        self.check(fs, a, 1e-1)       
        g1,g2,d1,d2 = self.braess_heterogeneous(.75, .75)
        fs = jacobi([g1,g2], [d1,d2], solver, max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-1)


    def test_gauss_seidel_2(self):
        print 'test gauss_seidel 2'
        g1,g2,d1,d2 = self.braess_heterogeneous(.25, .25)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_2)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-3)
        g1,g2,d1,d2 = self.braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = gauss_seidel([g1,g2], [d1,d2], solver_2) 
        self.check(fs, a, 1e-3)      
        g1,g2,d1,d2 = self.braess_heterogeneous(.75, .75)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_2)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-3)


    def test_jacobi_2(self):
        print 'test jacobi 2'
        g1,g2,d1,d2 = self.braess_heterogeneous(.25, .25)
        fs = jacobi([g1,g2], [d1,d2], solver_2)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-3)       
        g1,g2,d1,d2 = self.braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = jacobi([g1,g2], [d1,d2], solver_2) 
        self.check(fs, a, 1e-3)       
        g1,g2,d1,d2 = self.braess_heterogeneous(.75, .75)
        fs = jacobi([g1,g2], [d1,d2], solver_2)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-3)


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