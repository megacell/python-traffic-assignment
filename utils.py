__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
Some function that can be useful
'''

import numpy as np


def digits(x):
    # return number of digits in the integer part
    if x < 10.0: return 1
    return int(np.log(x)/np.log(10)) + 1


def spaces(n):
    # return the appropriate number of spaces
    return ''.join([' ']*(n))