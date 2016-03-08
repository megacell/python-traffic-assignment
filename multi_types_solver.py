__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import numpy as np
from scipy import special as sp
from AoN_igraph import all_or_nothing
from process_data import construct_igraph, construct_od


def total_ff_costs_heterogeneous(graphs, g, ods):
    cost = 0.
    for graph, od in zip(graphs, ods):
        g.es["weight"] = graph[:,3].tolist()
        cost = cost + graph[:,3].dot(all_or_nothing(g, od))
    return cost


def residual(graphs, demands, g, ods, fs):
    f = np.sum(fs, axis=1)
    x = np.power(f.reshape((graphs[0].shape[0],1)), np.array([0,1,2,3,4]))
    r = 0.
    for i, (graph, demand, od) in enumerate(zip(graphs, demands, ods)):
        grad = np.einsum('ij,ij->i', x, graph[:,3:])
        g.es["weight"] = grad.tolist()
        L = all_or_nothing(g, od)
        r = r + grad.dot(fs[:,i] - L)
    return r


def shift_graph(graph1, graph2, d):
    # given a graph with polynomial latency functions sum_k a_k x^k and shift d
    # return a graph with updated latencies sum_k a_k (x+d)^k
    for i in range(graph1.shape[0]):
        graph2[i,3:] = shift_polynomial(graph1[i,3:], d[i])
    return graph2


def shift_polynomial(coef, d):
    # given polynomial sum_k a_k x^k -> sum_k a_k (x+d)^k
    coef2 = np.zeros(5,dtype="float64")
    for i in range(5):
        for j in range(i,5):
            coef2[i] = coef2[i] + coef[j] * (d**(j-i)) * sp.binom(j,i)
    return coef2


def gauss_seidel(graphs, demands, solver, max_cycles=10, max_iter=100, \
    by_origin=False, q=10, display=0, past=10, stop=1e-8, eps=1e-8, \
    stop_cycle=None):
    # we are given a list of graphs and demands that are specific for different types of players
    # the gauss-seidel scheme updates cyclically for each type at a time
    if stop_cycle is None: 
        stop_cycle = stop
    g = construct_igraph(graphs[0])
    ods = [construct_od(d) for d in demands]
    types = len(graphs)
    fs = np.zeros((graphs[0].shape[0],types),dtype="float64")
    g2 = np.copy(graphs[0])
    K =  total_ff_costs_heterogeneous(graphs, g, ods)
    if K < eps:
        K = np.sum([np.sum(d[:,2]) for d in demands])
    elif display >= 1:
        print 'average free-flow travel time', \
            K / np.sum([np.sum(d[:,2]) for d in demands])

    for cycle in range(max_cycles):
        if display >= 1: print 'cycle:', cycle
        for i in range(types):
            # construct graph with updated latencies
            shift = np.sum(fs[:,range(i)+range(i+1,types)], axis=1)
            shift_graph(graphs[i], g2, shift)
            g.es["weight"] = g2[:,3].tolist()
            # update flow assignment for this type
            fs[:,i] = solver(g2, demands[i], g, ods[i], max_iter=max_iter, q=q, \
                display=display, past=past, stop=stop, eps=eps)
        # check if we have convergence
        r = residual(graphs, demands, g, ods, fs) / K
        if display >= 1:
            print 'error:', r
        if r < stop_cycle and r > 0:
            return fs
    return fs
