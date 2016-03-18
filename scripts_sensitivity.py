__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
various scripts for sensitivity analysis
'''

import numpy as np

delta = np.array([[1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [1,1,0,0,1,1,0,0],
    [0,0,1,1,0,0,1,1],
    [1,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,1]])

lam = np.ones((1,8))

M = np.vstack((delta, lam))

print delta
print lam
print M
print np.linalg.matrix_rank(M)
print np.linalg.matrix_rank(M[:,[0,3,6,7]])
print M[:,[0,3,6,7]]
delta2 = delta[:,[0,3,6,7]]
lam2 = lam[:,[0,3,6,7]]
print np.linalg.matrix_rank(delta2)
print np.linalg.inv(delta2.T.dot(delta2)).dot(lam2.T)
print 1/np.sum(np.linalg.inv(delta2.T.dot(delta2)))