__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from heterogeneous_solver import shift_polynomial, shift_graph, gauss_seidel, jacobi
from frank_wolfe import solver, solver_2, solver_3


class TestHeterogeneousSolver(unittest.TestCase):


    def check(self, f, true, eps):
        error = np.linalg.norm(f - true)
        print 'error', error
        self.assertTrue(error < eps)


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

    def test_gauss_seidel_3(self):
        print 'test gauss_seidel 3'
        g1,g2,d1,d2 = self.braess_heterogeneous(.25, .25)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_3)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-3)
        g1,g2,d1,d2 = self.braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = gauss_seidel([g1,g2], [d1,d2], solver_3) 
        self.check(fs, a, 1e-3)      
        g1,g2,d1,d2 = self.braess_heterogeneous(.75, .75)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_3)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-3)


    def test_jacobi_3(self):
        print 'test jacobi 3'
        g1,g2,d1,d2 = self.braess_heterogeneous(.25, .25)
        fs = jacobi([g1,g2], [d1,d2], solver_3)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-3)       
        g1,g2,d1,d2 = self.braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = jacobi([g1,g2], [d1,d2], solver_3) 
        self.check(fs, a, 1e-3)       
        g1,g2,d1,d2 = self.braess_heterogeneous(.75, .75)
        fs = jacobi([g1,g2], [d1,d2], solver_3)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-3)



if __name__ == '__main__':
    unittest.main()
