__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import numpy as np
from scipy.sparse import csr_matrix
from All_Or_Nothing import all_or_nothing
from scipy import special as sp


def compute_potential(graph ,f):
    # this routine is useful for doing a line search
    # computes the potential at flow assignment f
    links = int(np.max(graph[:,0])+1)
    g = np.copy(graph.dot(np.diag([1.,1.,1.,1.,1/2.,1/3.,1/4.,1/5.])))
    x = np.power(f.reshape((links,1)), np.array([1,2,3,4,5]))
    return np.sum(np.einsum('ij,ij->i', x, g[:,3:]))


def line_search(f, res=20):
    # on a grid of 2^res points bw 0 and 1, find global minimum
    # of continuous convex function
    d = 1./(2**res-1)
    l, r = 0, 2**res-1
    while r-l > 1:
        if f(l*d) <= f(l*d+d): return l*d
        if f(r*d-d) >= f(r*d): return r*d
        # otherwise f(l) > f(l+d) and f(r-d) < f(r)
        m1, m2 = (l+r)/2, 1+(l+r)/2
        if f(m1*d) < f(m2*d): r = m1
        if f(m1*d) > f(m2*d): l = m2
        if f(m1*d) == f(m2*d): return m1*d
    return l*d



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


def equilibrium_solver_2(graph, demand, max_iter=100):
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
        def h(x): return compute_potential(graph, (1.-x)*f + x*L)
        s = 2. / (i + 2.) if i>0 else line_search(h)
        f = (1.-s) * f + s * L
    return f


def gauss_seidel(graphs, demands, max_cycles=10, max_iter=100, by_origin=False):
    # we are given a list of graphs and demands that are specific for different types of players
    # the gauss-seidel scheme updates cyclically for each type at a time

    # prepare arrays for assignment by type
    types = len(graphs)
    links = int(np.max(graphs[0][:,0])+1)
    fs = np.zeros((links,types),dtype="float64")
    g = np.copy(graphs[0])

    for cycle in range(max_cycles):
        for i in range(types):
            # construct graph with updated latencies
            shift = np.sum(fs[:,range(i)+range(i+1,types)], axis=1)
            shift_graph(graphs[i], g, shift)
            # update flow assignment for this type
            fs[:,i] = equilibrium_solver(g, demands[i], max_iter)
    return fs


def jacobi(graphs, demands, max_cycles=10, max_iter=100, by_origin=False):
    # given a list of graphs and demands specific for different types of players
    # the jacobi scheme updates simultenously for each type at the same time

    # prepare arrays for assignment by type
    types = len(graphs)
    links = int(np.max(graphs[0][:,0])+1)
    fs = np.zeros((links,types),dtype="float64")
    updates = np.copy(fs)
    g = np.copy(graphs[0])

    for cycle in range(max_cycles):
        for i in range(types):
            # construct graph with updated latencies
            shift = np.sum(fs[:,range(i)+range(i+1,types)], axis=1)
            shift_graph(graphs[i], g, shift)
            # update flow assignment for this type
            updates[:,i] = equilibrium_solver(g, demands[i], max_iter)
        # batch update
        fs = np.copy(updates)
    return fs


def shift_graph(graph1, graph2, d):
    # given a graph with polynomial latency functions sum_k a_k x^k and shift d
    # return a graph with updated latencies sum_k a_k (x+d)^k
    links = graph1.shape[0]
    for i in range(links):
        graph2[i,3:] = shift_polynomial(graph1[i,3:], d[i])
    return graph2


def shift_polynomial(coef, d):
    # given polynomial sum_k a_k x^k -> sum_k a_k (x+d)^k
    coef2 = np.zeros(5,dtype="float64")
    for i in range(5):
        for j in range(i,5):
            coef2[i] = coef2[i] + coef[j] * (d**(j-i)) * sp.binom(j,i)
    return coef2


# def shift_graph_2(graph1, graph2, d):
#     # numpy matrix implementation of shift_graph
#     A = np.zeros((5,5),dtype="float64")
#     for i in range(5):
#         for j in range(i,5):
#             A[j,i] = (d**(j-i)) * sp.binom(j,i)
#     graph2[:,3:] = graph2[:,3:].dot(A)
#     return graph2


def main():
    graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
    f = equilibrium_solver(graph, demand)
    print f


if __name__ == '__main__':
    main()
