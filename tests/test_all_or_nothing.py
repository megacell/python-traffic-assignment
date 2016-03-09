__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from All_Or_Nothing import all_or_nothing

eps = 1e-8

class TestAllOrNothing(unittest.TestCase):

    def test_all_or_nothing(self):
        # load the data
        graph=np.loadtxt('data/braess_graph.csv', delimiter=',', skiprows=1)
        od=np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        od=np.reshape(od, (1,3))
        # all or nothing assignment
        L = all_or_nothing(graph, od)
        self.assertTrue(np.linalg.norm(L - np.array([2., 0., 2., 0., 2.])) < eps)

        # modify graph
        graph[2,3] = 1000.
        graph[0,3] = 1.
        L = all_or_nothing(graph, od)
        self.assertTrue(np.linalg.norm(L - np.array([0., 2., 0., 0., 2.])) < eps)


    def test_all_or_nothing_2(self):
        # load the data
        graph=np.loadtxt('data/graph_test.csv', delimiter=',')
        # print graph
        od=np.loadtxt('data/od_test.csv', delimiter=',')
        od=np.reshape(od, (1,3))
        L = all_or_nothing(graph, od)
        # print L
        # this L is wrong!! :(

if __name__ == '__main__':
    unittest.main()
