__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import numpy as np
from scipy.sparse import csr_matrix
from All_Or_Nothing import all_or_nothing

def compute_potential(graph ,f):
    # this routine is useful for doing a line search using amijo rule
    pass


def equilibrium_solver(graph, demand, max_iter=100):
    # Prepares arrays for assignment
    links = int(np.max(graph[:,0])+1)
    f = np.zeros(links,dtype="float64") # initial flow assignment is null
    L = np.zeros(links,dtype="float64")
    g = np.copy(graph[:,:4])

    for i in range(max_iter):
        # construct weighted graph with latest flow assignment
        x = np.power(f.reshape((links,1)), np.array([0,1,2,3,4]))
        g[:,3] = np.einsum('ij,ij->i', x, graph[:,3:])

        # flow update
        L = all_or_nothing(g, demand)
        s = 2. / (i + 2.) if i>0 else 1.
        f = (1.-s) * f + s * L
    return f


def main():
    graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
    f = equilibrium_solver(graph, demand)
    print f

if __name__ == '__main__':
    main()