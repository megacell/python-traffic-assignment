__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"


import numpy as np
from AoN_igraph import all_or_nothing
from frank_wolfe_2 import total_free_flow_cost, search_direction, line_search, solver_3
from process_data import construct_igraph, construct_od
from utils import multiply_cognitive_cost, heterogeneous_demand


def search_direction_multi(f, graphs, gs, ods, L, grad):
    # extension of search_direction routine in frank_wolfe_2.py
    # for the heterogeneous game
    links = graphs[0].shape[0]
    types = len(graphs)
    for j, (graph, g, od) in enumerate(zip(graphs, gs, ods)):
        l, gr = search_direction(np.sum(np.reshape(f,(types,links)).T,1), \
            graph, g, od)
        L[(j*links) : ((j+1)*links)] = l
        grad[(j*links) : ((j+1)*links)] = gr
    return L, grad


def merit(f, graphs, gs, ods, L, grad):
    # this computes the merit function associated to the VI problem
    # max_y <F(x), x-y>
    L, grad = search_direction_multi(f, graphs, gs, ods, L, grad)
    return grad.dot(f - L)


def fw_heterogeneous_1(graphs, demands, max_iter=100, eps=1e-8, q=None, \
    display=0, past=None, stop=1e-8):
    '''
    Frank-Wolfe algorithm on the heterogeneous game
    given a list of graphs in the format 
    g = [[link_id from to a0 a1 a2 a3 a4]]
    and demand in the format
    d = [[o d flow]]
    '''
    # construct graph and demand objects suiteable for AoN_igraph 
    gs = [construct_igraph(graph) for graph in graphs]
    ods = [construct_od(demand) for demand in demands]
    # construct empty vector to be filled in with values
    links = graphs[0].shape[0]
    types = len(graphs)
    f = np.zeros(links*types,dtype="float64") # initial flow assignment is null
    L = np.zeros(links*types,dtype="float64")
    grad = np.zeros(links*types,dtype="float64")
    # compute re-normalization constant
    K = sum([total_free_flow_cost(g, od) for g,od in zip(gs, ods)])
    if K < eps:
        K = sum([np.sum(demand[:,2]) for demand in demands])
    elif display >= 1:
        print 'average free-flow travel time', \
            K / sum([np.sum(demand[:,2]) for demand in demands])
    # compute iterations
    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i+1)
            else:
                print 'iteration: {}, error: {}'.format(i+1, error)
        # construct weighted graph with latest flow assignment
        L, grad = search_direction_multi(f, graphs, gs, ods, L, grad)
        if i >= 1:
            error = grad.dot(f - L) / K
            if error < stop: return np.reshape(f,(types,links)).T
        f = f + 2.*(L-f)/(i+2.)
    return np.reshape(f,(types,links)).T


def fw_heterogeneous_2(graphs, demands, past=10, max_iter=100, eps=1e-8, q=50, \
    display=0, stop=1e-8):
    '''
    Frank-Wolfe algorithm on the heterogeneous game
    given a list of graphs in the format 
    g = [[link_id from to a0 a1 a2 a3 a4]]
    and demand in the format
    d = [[o d flow]]
    '''
    assert past <= q, "'q' must be bigger or equal to 'past'"
    # construct graph and demand objects suiteable for AoN_igraph 
    gs = [construct_igraph(graph) for graph in graphs]
    ods = [construct_od(demand) for demand in demands]
    # construct empty vector to be filled in with values
    links = graphs[0].shape[0]
    types = len(graphs)
    f = np.zeros(links*types,dtype="float64") # initial flow assignment is null
    fs = np.zeros((links*types,past),dtype="float64")
    L = np.zeros(links*types,dtype="float64")
    grad = np.zeros(links*types,dtype="float64")
    L2 = np.zeros(links*types,dtype="float64")
    grad2 = np.zeros(links*types,dtype="float64")
    # compute re-normalization constant
    K = sum([total_free_flow_cost(g, od) for g,od in zip(gs, ods)])
    if K < eps:
        K = sum([np.sum(demand[:,2]) for demand in demands])
    elif display >= 1:
        print 'average free-flow travel time', \
            K / sum([np.sum(demand[:,2]) for demand in demands])
    # compute iterations
    for i in range(max_iter):
        if display >= 1:
            if i <= 1:
                print 'iteration: {}'.format(i+1)
            else:            
                print 'iteration: {}, error: {}'.format(i+1, error)
        # construct weighted graph with latest flow assignment
        #print 'f', f
        #print 'reshape', np.reshape(f,(links,types))
        total_f = np.sum(np.reshape(f,(types,links)).T,1)
        #print 'total flow', total_f
        for j, (graph, g, od) in enumerate(zip(graphs, gs, ods)):
            l, gr = search_direction(total_f, graph, g, od)
            L[(j*links) : ((j+1)*links)] = l
            grad[(j*links) : ((j+1)*links)] = gr
        #print 'L', L
        #print 'grad', grad
        fs[:,i%past] = L
        w = L - f
        if i >= 1:
            error = -grad.dot(w) / K
            # if error < stop and error > 0.0:
            if error < stop:
                if display >= 1: print 'stop with error: {}'.format(error)
                return np.reshape(f,(types,links)).T
        if i > q:
            # step 3 of Fukushima
            v = np.sum(fs,axis=1) / min(past,i+1) - f
            norm_v = np.linalg.norm(v,1)
            if norm_v < eps: 
                if display >= 1: print 'stop with norm_v: {}'.format(norm_v)
                return np.reshape(f,(types,links)).T
            norm_w = np.linalg.norm(w,1)
            if norm_w < eps: 
                if display >= 1: print 'stop with norm_w: {}'.format(norm_w)
                return np.reshape(f,(types,links)).T
            # step 4 of Fukushima
            gamma_1 = grad.dot(v) / norm_v
            gamma_2 = grad.dot(w) / norm_w
            if gamma_2 > -eps: 
                if display >= 1: print 'stop with gamma_2: {}'.format(gamma_2)
                return np.reshape(f,(types,links)).T
            d = v if gamma_1 < gamma_2 else w
            # step 5 of Fukushima
            s = line_search(lambda a: merit(f+a*d, graphs, gs, ods, L2, grad2))
            # print 'step', s
            if s < eps: 
                if display >= 1: print 'stop with step_size: {}'.format(s)
                return np.reshape(f,(types,links)).T
            f = f + s*d
        else:
            f = f + 2. * w/(i+2.)
    return np.reshape(f,(types,links)).T


def parametric_study_2(alphas, g, d, node, geometry, thres, cog_cost, output, \
    stop=1e-2):
    g_nr, small_capacity = multiply_cognitive_cost(g, geometry, thres, cog_cost)
    if (type(alphas) is float) or (type(alphas) is int):
        alphas = [alphas]
    for alpha in alphas:
        #special case where in fact homogeneous game
        if alpha == 0.0:
            print 'non-routed = 1.0, routed = 0.0'
            f_nr = solver_3(g_nr, d, max_iter=1000, display=1, stop=stop)     
            fs=np.zeros((f_nr.shape[0],2))
            fs[:,0]=f_nr 
        elif alpha == 1.0:
            print 'non-routed = 0.0, routed = 1.0'
            f_r = solver_3(g, d, max_iter=1000, display=1, stop=stop)    
            fs=np.zeros((f_r.shape[0],2))
            fs[:,1]=f_r            
        #run solver
        else:
            print 'non-routed = {}, routed = {}'.format(1-alpha, alpha)
            d_nr, d_r = heterogeneous_demand(d, alpha)
            fs = fw_heterogeneous_1([g_nr,g], [d_nr,d_r], max_iter=1000, \
                display=1, stop=stop)
        np.savetxt(output.format(int(alpha*100)), fs, \
            delimiter=',', header='f_nr,f_r')

