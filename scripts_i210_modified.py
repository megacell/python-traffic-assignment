__author__ = "Jerome Thai, Nicolas Laurent-Brouty"
__email__ = "jerome.thai@berkeley.edu, nicolas.lb@berkeley.edu"


'''
Scripts for the I-210 sketch with modified 
'''

import numpy as np
from process_data import extract_features
from frank_wolfe_2 import solver_3
from multi_types_solver import gauss_seidel
from utils import multiply_cognitive_cost, heterogeneous_demand
from metrics import save_metrics


def load_I210_modified():
    net = np.loadtxt('data/I210_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/I210_od.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/I210_node.csv', delimiter=',', skiprows=1)
    geometry = extract_features('data/I210Sketch_net.csv')
    demand = np.reshape(demand, (1,3))
    # modify link 21
    net[21,-1] = net[21,-1] * (4**4)
    geometry[21,0] = geometry[21,0] / 4.
    return net, demand, node, geometry


def I210_parametric_study(alphas):
    # load the network and its properties
    g_r, d, node, feat = load_I210_modified()
    # modify the costs on non routed network
    g_nr, small_capacity = multiply_cognitive_cost(g_r, feat, 3000., 100.)
    #divide the demand by 4000 to computationally optimize
    d[:,2] = d[:,2] / 4000.

    for alpha in alphas:
        if alpha == 0.0:
            print 'non-routed = 1.0, routed = 0.0'
            f_nr = solver_3(g_nr, d, max_iter=1000, stop=1e-3)     
            fs=np.zeros((f_nr.shape[0],2))
            fs[:,0]=f_nr 
        elif alpha == 1.0:
            print 'non-routed = 0.0, routed = 1.0'
            f_r = solver_3(g_r, d, max_iter=1000, stop=1e-3)    
            fs=np.zeros((f_r.shape[0],2))
            fs[:,1]=f_r            
        else:
            print 'non-routed = {}, routed = {}'.format(1-alpha, alpha)
            d_nr, d_r = heterogeneous_demand(d, alpha)
            fs = gauss_seidel([g_nr,g_r], [d_nr,d_r], solver_3, max_iter=1000, \
                stop=1e-3, stop_cycle=1e-3, q=50, past=20)
        np.savetxt('data/I210_modified/test_{}.csv'.format(int(alpha*100)), fs, \
            delimiter=',', header='f_nr,f_r')


def I210_metrics(alphas):
    out = np.zeros((len(alphas),6))
    net, d, node, features = load_I210_modified()
    d[:,2] = d[:,2] / 4000. 
    net2, small_capacity = multiply_cognitive_cost(net, features, 3000., 100.)
    save_metrics(alphas, net, net2, d, features, small_capacity, \
        'data/I210_modified/test_{}.csv', 'data/I210_modified/out.csv', skiprows=1)


def main():
    I210_parametric_study(np.linspace(.51,1.,50))
    I210_metrics(np.linspace(0.,1.,101))


if __name__ == '__main__':
    main()