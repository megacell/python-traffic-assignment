__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
import numpy as np
from frank_wolfe import equilibrium_solver


class TestFrankWolfe(unittest.TestCase):

    def test_equilibrium_solver(self):
        print 'test equilibrium_solver'

if __name__ == '__main__':
    unittest.main()