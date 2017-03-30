__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"


'''
This module is frank-wolfe algorithm using an all-or-nothing assignment
based on igraph package
'''

import numpy as np
from process_data import construct_igraph, construct_od
from AoN_igraph import all_or_nothing


def potential(graph, f):
    # this routine is useful for doing a line search
    # computes the potential at flow assignment f
    links = int(np.max(graph[:, 0]) + 1)
    g = graph.dot(np.diag([1., 1., 1., 1., 1 / 2., 1 / 3., 1 / 4., 1 / 5.]))
    x = np.power(f.reshape((links, 1)), np.array([1, 2, 3, 4, 5]))
    return np.sum(np.einsum('ij,ij->i', x, g[:, 3:]))


def line_search(f, res=20):
    # on a grid of 2^res points bw 0 and 1, find global minimum
    # of continuous convex function
    d = 1. / (2**res - 1)
    l, r = 0, 2**res - 1
    while r - l > 1:
        if f(l * d) <= f(l * d + d):
            return l * d
        if f(r * d - d) >= f(r * d):
            return r * d
        # otherwise f(l) > f(l+d) and f(r-d) < f(r)
        m1, m2 = (l + r) / 2, 1 + (l + r) / 2
        if f(m1 * d) < f(m2 * d):
            r = m1
        if f(m1 * d) > f(m2 * d):
            l = m2
        if f(m1 * d) == f(m2 * d):
            return m1 * d
    return l * d


def total_free_flow_cost(g, od):
    return np.array(g.es["weight"]).dot(all_or_nothing(g, od))


def search_direction(f, graph, g, od):
    # computes the Frank-Wolfe step
    # g is just a canvas containing the link information and to be updated with
    # the most recent edge costs
    x = np.power(f.reshape((f.shape[0], 1)), np.array([0, 1, 2, 3, 4]))
    grad = np.einsum('ij,ij->i', x, graph[:, 3:])
    g.es["weight"] = grad.tolist()
    return all_or_nothing(g, od), grad


def solver(graph, demand, g=None, od=None, max_iter=100, eps=1e-8, q=None,
           display=0, past=None, stop=1e-8):

    if g is None:
        g = construct_igraph(graph)
    if od is None:
        od = construct_od(demand)
    # initial flow assignment is null
    f = np.zeros(graph.shape[0], dtype="float64")
    K = total_free_flow_cost(g, od)
    if K < eps:
        K = np.sum(demand[:, 2])
    elif display >= 1:
        print 'average free-flow travel time', K / np.sum(demand[:, 2])

    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i + 1)
            else:
                print 'iteration: {}, error: {}'.format(i + 1, error)
        # construct weighted graph with latest flow assignment
        L, grad = search_direction(f, graph, g, od)
        if i >= 1:
            error = grad.dot(f - L) / K
            if error < stop:
                return f
        f = f + 2. * (L - f) / (i + 2.)
    return f


def solver_2(graph, demand, g=None, od=None, max_iter=100, eps=1e-8, q=10,
             display=0, past=None, stop=1e-8):

    if g is None:
        g = construct_igraph(graph)
    if od is None:
        od = construct_od(demand)
    # initial flow assignment is null
    f = np.zeros(graph.shape[0], dtype="float64")
    ls = max_iter / q  # frequency of line search
    K = total_free_flow_cost(g, od)
    if K < eps:
        K = np.sum(demand[:, 2])
    elif display >= 1:
        print 'average free-flow travel time', K / np.sum(demand[:, 2])

    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i + 1)
            else:
                print 'iteration: {}, error: {}'.format(i + 1, error)
        # construct weighted graph with latest flow assignment
        L, grad = search_direction(f, graph, g, od)
        if i >= 1:
            # w = f - L
            # norm_w = np.linalg.norm(w,1)
            # if norm_w < eps: return f
            error = grad.dot(f - L) / K
            if error < stop:
                return f
        # s = line_search(lambda a: potential(graph, (1.-a)*f+a*L)) if i>max_iter-q \
        #     else 2./(i+2.)
        s = line_search(lambda a: potential(graph, (1. - a) * \
                        f + a * L)) if i % ls == (ls - 1) else 2. / (i + 2.)
        if s < eps:
            return f
        f = (1. - s) * f + s * L
    return f


def solver_3(graph, demand, g=None, od=None, past=10, max_iter=100, eps=1e-8,
             q=50, display=0, stop=1e-8):
    '''
    this is an adaptation of Fukushima's algorithm
    graph:    numpy array of the format [[link_id from to a0 a1 a2 a3 a4]]
    demand:   mumpy arrau of the format [[o d flow]]
    g:        igraph object constructed from graph
    od:       od in the format {from: ([to], [rate])}
    past:     search direction is the mean over the last 'past' directions
    max_iter: maximum number of iterations
    esp:      used as a stopping criterium if some quantities are too close to 0
    q:        first 'q' iterations uses open loop step sizes 2/(i+2)
    display:  controls the display of information in the terminal
    stop:     stops the algorithm if the error is less than 'stop'
    '''
    assert past <= q, "'q' must be bigger or equal to 'past'"
    if g is None:
        g = construct_igraph(graph)
    if od is None:
        od = construct_od(demand)
    # initial flow assignment is null
    f = np.zeros(graph.shape[0], dtype="float64")
    fs = np.zeros((graph.shape[0], past), dtype="float64")
    K = total_free_flow_cost(g, od)
    if K < eps:
        K = np.sum(demand[:, 2])
    elif display >= 1:
        print 'average free-flow travel time', K / np.sum(demand[:, 2])

    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i + 1)
            else:
                print 'iteration: {}, error: {}'.format(i + 1, error)
        # construct weighted graph with latest flow assignment
        L, grad = search_direction(f, graph, g, od)
        fs[:, i % past] = L
        w = L - f
        if i >= 1:
            error = -grad.dot(w) / K
            # if error < stop and error > 0.0:
            if error < stop:
                if display >= 1:
                    print 'stop with error: {}'.format(error)
                return f
        if i > q:
            # step 3 of Fukushima
            v = np.sum(fs, axis=1) / min(past, i + 1) - f
            norm_v = np.linalg.norm(v, 1)
            if norm_v < eps:
                if display >= 1:
                    print 'stop with norm_v: {}'.format(norm_v)
                return f
            norm_w = np.linalg.norm(w, 1)
            if norm_w < eps:
                if display >= 1:
                    print 'stop with norm_w: {}'.format(norm_w)
                return f
            # step 4 of Fukushima
            gamma_1 = grad.dot(v) / norm_v
            gamma_2 = grad.dot(w) / norm_w
            if gamma_2 > -eps:
                if display >= 1:
                    print 'stop with gamma_2: {}'.format(gamma_2)
                return f
            d = v if gamma_1 < gamma_2 else w
            # step 5 of Fukushima
            s = line_search(lambda a: potential(graph, f + a * d))
            if s < eps:
                if display >= 1:
                    print 'stop with step_size: {}'.format(s)
                return f
            f = f + s * d
        else:
            f = f + 2. * w / (i + 2.)
    return f


def single_class_parametric_study(factors, output, net, demand,
                                  max_iter=100, display=1):
    '''
    parametric study where the equilibrium flow is computed under different
    demand levels alpha*demand for alpha in factors
    '''
    g = construct_igraph(net)
    d = np.copy(demand)
    fs = np.zeros((net.shape[0], len(factors)))
    header = ','.join(['X{}'.format(i) for i in range(len(factors))])
    for i, alpha in enumerate(factors):
        if display >= 1:
            print 'computing equilibrium {}/{}'.format(i + 1, len(factors))
        d[:, 2] = alpha * demand[:, 2]
        f = solver_3(net, d, g=g, past=20, q=50, stop=1e-3, display=display,
                     max_iter=max_iter)
        fs[:, i] = f
    np.savetxt(output, fs, delimiter=',', header=header, comments='')
