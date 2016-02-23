__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
from metrics import cost, cost_ratio, total_cost, average_cost
import numpy as np


class TestMetrics(unittest.TestCase):


    def test_cost(self):
        net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        net[:,5] = np.array([2.]*5)
        flow = np.array([0., 1., 2., 3., 4.])
        result = np.array([0., 3., 8., 19., 36.])
        self.assertTrue(np.linalg.norm(result - cost(flow, net)) < 1e-8)


    def test_cost_ratio(self):
        net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        net[:,5] = np.array([2.]*5)
        flow = np.array([0., 1., 2., 3., 4.])
        result = np.array([1.0, 3.0, 1e8, 19, 1e8])
        self.assertTrue(np.linalg.norm(result - cost_ratio(flow, net)) < 1e-8)


    def test_total_cost(self):
        net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        net[:,5] = np.array([2.]*5)
        flow = np.array([0., 1., 2., 3., 4.])
        self.assertTrue(np.linalg.norm(total_cost(flow, net) - 220.) < 1e-8)


    def test_average_cost(self):
        net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        net[:,5] = np.array([2.]*5)
        flow = np.array([0., 1., 2., 3., 4.])
        od = np.array([[0,0,0.],[0,0,1.],[0,0,2.],[0,0,3.],[0,0,4.]])
        self.assertTrue(np.linalg.norm(average_cost(flow, net, od) - 22.) < 1e-8)


if __name__ == '__main__':
    unittest.main()
