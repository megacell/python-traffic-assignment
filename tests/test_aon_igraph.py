__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from AoN_igraph import all_or_nothing
from process_data import construct_igraph

eps = 1e-8

class TestAllOrNothing(unittest.TestCase):

    def test_all_or_nothing(self):
        # load the data
        graph=np.loadtxt('data/braess_graph.csv', delimiter=',', skiprows=1)
        g = construct_igraph(graph)
        od=np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
        od={int(od[0]): ([int(od[1])],[od[2]])}
        # all or nothing assignment
        L = all_or_nothing(g, od)
        self.assertTrue(np.linalg.norm(L - np.array([2., 0., 2., 0., 2.])) < eps)

        g.es["weight"] = [1., 1., 1000., 1.0, 0.0]
        # modify graph
        L = all_or_nothing(g, od)
        self.assertTrue(np.linalg.norm(L - np.array([0., 2., 0., 0., 2.])) < eps)


    def test_all_or_nothing_2(self):
        # load the data
        graph=np.loadtxt('data/graph_test.csv', delimiter=',')
        g = construct_igraph(graph)
        # print graph
        od=np.loadtxt('data/od_test.csv', delimiter=',')
        od={int(od[0]): ([int(od[1])],[od[2]])}
        L = all_or_nothing(g, od)
        # this should be the right L !!!

if __name__ == '__main__':
    unittest.main()