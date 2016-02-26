__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import numpy as np
from All_Or_Nothing import all_or_nothing


def potential(graph ,f):
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


def search_direction(f, graph, g, demand):
    # computes the Frank-Wolfe step
    # g is just a canvas containing the link information and to be updated with 
    # the most recent edge costs
    x = np.power(f.reshape((f.shape[0],1)), np.array([0,1,2,3,4]))
    grad = np.einsum('ij,ij->i', x, graph[:,3:])
    g[:,3] = grad
    return all_or_nothing(g, demand), grad


def total_free_flow_cost(g, demand):
    # computes the average cost under free flow travel times
    L = all_or_nothing(g, demand)
    return g[:,3].dot(L)


def solver(graph, demand, max_iter=100, eps=1e-8, q=None, display=0, past=None,\
    stop=1e-8):
    # Prepares arrays for assignment
    links = int(np.max(graph[:,0])+1)
    f = np.zeros(links,dtype="float64") # initial flow assignment is null
    g = np.copy(graph[:,:4])
    K = total_free_flow_cost(g, demand)
    if K < eps:
        K = np.sum(demand[:,2])
    elif display >= 1:
        print 'average free-flow travel time', K / np.sum(demand[:,2])

    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i+1)
            else:
                print 'iteration: {}, error: {}'.format(i+1, error)
        # construct weighted graph with latest flow assignment
        L, grad = search_direction(f, graph, g, demand)
        if i >= 1:
            # w = f - L
            # norm_w = np.linalg.norm(w,1)
            # if norm_w < eps: return f
            error = grad.dot(f - L) / K
            if error < stop: return f
        s = 2. / (i + 2.)
        f = (1.-s) * f + s * L
    return f


def solver_2(graph, demand, max_iter=100, eps=1e-8, q=10, display=0, past=None,\
    stop=1e-8):
    # version with line search
    # Prepares arrays for assignment
    links = int(np.max(graph[:,0])+1)
    f = np.zeros(links,dtype="float64") # initial flow assignment is null
    g = np.copy(graph[:,:4])
    ls = max_iter/q # frequency of line search
    K = total_free_flow_cost(g, demand)
    if K < eps:
        K = np.sum(demand[:,2])
    elif display >= 1:
        print 'average free-flow travel time', K / np.sum(demand[:,2])

    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i+1)
            else:
                print 'iteration: {}, error: {}'.format(i+1, error)
        # construct weighted graph with latest flow assignment
        L, grad = search_direction(f, graph, g, demand)
        if i >= 1:
            # w = f - L
            # norm_w = np.linalg.norm(w,1)
            # if norm_w < eps: return f
            error = grad.dot(f - L) / K
            if error < stop: return f
        # s = line_search(lambda a: potential(graph, (1.-a)*f+a*L)) if i>max_iter-q \
        #     else 2./(i+2.)
        s = line_search(lambda a: potential(graph, (1.-a)*f+a*L)) if i%ls==(ls-1) \
            else 2./(i+2.)
        if s < eps: return f
        f = (1.-s) * f + s * L
    return f


def solver_3(graph, demand, past=10, max_iter=100, eps=1e-8, q=50, display=0,\
    stop=1e-8):
    # modified Frank-Wolfe from Masao Fukushima
    links = int(np.max(graph[:,0])+1)
    f = np.zeros(links,dtype="float64") # initial flow assignment is null
    L = np.zeros(links,dtype="float64")
    fs = np.zeros((links,past),dtype="float64")
    g = np.copy(graph[:,:4])
    K =  total_free_flow_cost(g, demand)
    if K < eps:
        K = np.sum(demand[:,2])
    elif display >= 1:
        print 'average free-flow travel time', K / np.sum(demand[:,2])

    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i+1)
            else:            
                print 'iteration: {}, error: {}'.format(i+1, error)
        # construct weighted graph with latest flow assignment
        L, grad = search_direction(f, graph, g, demand)
        fs[:,i%past] = L
        w = L - f
        if i >= 1:
            error = -grad.dot(w) / K
            if error < stop: return f
        if i > q:
            # step 3 of Fukushima
            v = np.sum(fs,1) / min(past,i+1) - f
            norm_v = np.linalg.norm(v,1)
            if norm_v < eps: return f
            norm_w = np.linalg.norm(w,1)
            if norm_w < eps: return f
            # step 4 of Fukushima
            gamma_1 = grad.dot(v) / norm_v
            gamma_2 = grad.dot(w) / norm_w
            if gamma_2 > -eps: return f
            d = v if gamma_1 < gamma_2 else w
            # step 5 of Fukushima
            s = line_search(lambda a: potential(graph, f+a*d))
            if s < eps: return f
            f = f + s*d
        else:
            f = f + 2*w/(i+2.)
    return f


def main():
    graph = np.loadtxt('data/braess_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/braess_od.csv', delimiter=',', skiprows=1)
    f = solver(graph, demand)
    print f


if __name__ == '__main__':
    main()
