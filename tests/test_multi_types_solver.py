__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from multi_types_solver import shift_polynomial, shift_graph, gauss_seidel
from frank_wolfe_2 import solver, solver_2, solver_3
from utils import braess_heterogeneous


class TestMultiTypesSolver(unittest.TestCase):


    def check(self, f, true, eps):
        error = np.linalg.norm(f - true) / np.linalg.norm(true)
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


    def test_gauss_seidel(self):
        print 'test gauss_seidel'
        g1,g2,d1,d2 = braess_heterogeneous(.25, .25)
        fs = gauss_seidel([g1,g2], [d1,d2], solver, max_iter=200)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-2)
        g1,g2,d1,d2 = braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = gauss_seidel([g1,g2], [d1,d2], solver, max_iter=200) 
        self.check(fs, a, 1e-2)      
        g1,g2,d1,d2 = braess_heterogeneous(.75, .75)
        fs = gauss_seidel([g1,g2], [d1,d2], solver, max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-1)


    def test_gauss_seidel_2(self):
        print 'test gauss_seidel 2'
        g1,g2,d1,d2 = braess_heterogeneous(.25, .25)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_2)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-3)
        g1,g2,d1,d2 = braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = gauss_seidel([g1,g2], [d1,d2], solver_2) 
        self.check(fs, a, 1e-3)      
        g1,g2,d1,d2 = braess_heterogeneous(.75, .75)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_2, max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-3)


    def test_gauss_seidel_3(self):
        print 'test gauss_seidel 3'
        g1,g2,d1,d2 = braess_heterogeneous(.25, .25)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_3)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        #print fs
        #print a
        self.check(fs, a, 1e-3)
        g1,g2,d1,d2 = braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = gauss_seidel([g1,g2], [d1,d2], solver_3) 
        self.check(fs, a, 1e-3)      
        g1,g2,d1,d2 = braess_heterogeneous(.75, .75)
        fs = gauss_seidel([g1,g2], [d1,d2], solver_3, q=50)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(fs, a, 1e-3)


if __name__ == '__main__':
    unittest.main()