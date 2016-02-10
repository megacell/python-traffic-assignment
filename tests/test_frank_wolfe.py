__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from frank_wolfe import equilibrium_solver


class TestFrankWolfe(unittest.TestCase):

    def test_equilibrium_solver(self):
        graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        f = equilibrium_solver(graph, demand)
        # not much precision with current implementation of Frank-Wolfe
        self.assertTrue(np.linalg.norm(f - np.array([1.,1.,0.,1.,1.])) < 1e-1)

        # modify demand
        demand[0,2] = 0.5
        f = equilibrium_solver(graph, demand)
        self.assertTrue(np.linalg.norm(f - np.array([.5,.0,.5,.0,.5])) < 1e-8)

if __name__ == '__main__':
    unittest.main()