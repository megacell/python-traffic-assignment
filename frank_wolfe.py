__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import numpy as np
from scipy.sparse import csr_matrix
from All_Or_Nothing import all_or_nothing


def equilibrium_solver(graph, demand, max_iter=100):
    
    # load the data from graph and demand
    graph = np.loadtxt(graph, delimiter=',', skiprows=1)
    od = np.loadtxt(demand, delimiter=',', skiprows=1)

    # Characteristics of the graph
    zones = int(np.max(od[:,0:2])+1)
    links = int(np.max(graph[:,0])+1)

    # Prepares arrays for assignment
    f = np.zeros(links,dtype="float64") # initial flow assignment is null
    L = np.zeros(links,dtype="float64")
    g = np.copy(graph[:,:4])

    for i in range(max_iter):
        # construct weighted graph with latest flow assignment
        x = np.power(f.reshape((links,1)), np.array([0,1,2,3,4]))
        g[:,3] = np.einsum('ij,ij->i', x, graph[:,3:])

        # flow update
        L = all_or_nothing(g, od)
        s = 2. / (i + 2.) if i>0 else 1.
        f = (1.-s) * f + s * L
    return f


def main():
    f = equilibrium_solver(graph='braess_net.csv', demand='braess_od.csv')
    print f

if __name__ == '__main__':
    main()