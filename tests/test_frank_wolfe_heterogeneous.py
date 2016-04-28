__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from frank_wolfe_heterogeneous import fw_heterogeneous_1, fw_heterogeneous_2
from utils import braess_heterogeneous


class TestFrankWolfeHeterogeneous(unittest.TestCase):

    def check(self, f, true, eps):
        error = np.linalg.norm(f - true) / np.linalg.norm(true)
        print 'error', error
        self.assertTrue(error < eps)

    def test_fw_heterogeneous_1(self):
        print 'test fw_heterogeneous 1'
        g1,g2,d1,d2 = braess_heterogeneous(.25, .25)
        fs = fw_heterogeneous_1([g1,g2], [d1,d2], max_iter=200)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-2)
        g1,g2,d1,d2 = braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = fw_heterogeneous_1([g1,g2], [d1,d2], max_iter=200) 
        self.check(fs, a, 1e-2)      
        g1,g2,d1,d2 = braess_heterogeneous(.75, .75)
        fs = fw_heterogeneous_1([g1,g2], [d1,d2], max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(np.sum(fs,1), np.sum(a,1), 1e-2) 


    def test_fw_heterogeneous_2(self):
        print 'test fw_heterogeneous 2'
        g1,g2,d1,d2 = braess_heterogeneous(.25, .25)
        fs = fw_heterogeneous_2([g1,g2], [d1,d2], q=10, past=10)
        a = np.array([[.125,.25],[.125,.0],[.0, .25],[.125, .0],[.125, .25]])
        self.check(fs, a, 1e-2)
        g1,g2,d1,d2 = braess_heterogeneous(1., 1.)
        a = np.array([[.5,.5],[.5,.5],[.0, .0],[.5, .5],[.5, .5]])
        fs = fw_heterogeneous_2([g1,g2], [d1,d2], q=10, past=10) 
        self.check(fs, a, 1e-2)      
        g1,g2,d1,d2 = braess_heterogeneous(.75, .75)
        fs = fw_heterogeneous_2([g1,g2], [d1,d2], q=200, past=10, max_iter=200)
        a = np.array([[.375, .625],[.375, .125],[.0, .5],[.375, .125],[.375, .625]])
        self.check(np.sum(fs,1), np.sum(a,1), 1e-2) 


if __name__ == '__main__':
    unittest.main()