__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
from metrics import cost, cost_ratio, total_cost, average_cost,\
    total_cost_all_or_nothing, average_cost_all_or_nothing, average_cost_subset, \
    all_or_nothing_assignment
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


    def test_average_cost_all_or_nothing(self):
        net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        flow = np.array([.5,.5,.0,.5,.5])
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        demand=np.reshape(demand, (1,3))
        c = average_cost_all_or_nothing(flow, net, demand)
        self.assertTrue(abs(c - 1.0) < 1e-8)


    def test_total_cost_all_or_nothing(self):
        net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        flow = np.array([.5,.5,.0,.5,.5])
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        demand=np.reshape(demand, (1,3))
        c = total_cost_all_or_nothing(flow, net, demand)
        self.assertTrue(abs(c - 2.0) < 1e-8)


    # def test_ratio_subset(self):
    #     net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
    #     flow = np.array([.5,.5,.0,.5,.5])
    #     subset = np.array([0,1,0,1,0])
    #     r = ratio_subset(flow, net, subset)
    #     self.assertTrue(abs(r - 1.0) < 1e-8)


    def test_all_or_nothing_assignment(self):
        net = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
        cost = np.array([1.,5.,1.,5.,1.])
        demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        demand=np.reshape(demand, (1,3))
        L = all_or_nothing_assignment(cost, net, demand)
        self.assertTrue(np.linalg.norm(L - np.array([2.,0.,2.,0.,2.])) < 1e-8)


if __name__ == '__main__':
    unittest.main()
