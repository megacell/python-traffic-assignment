__author__ = "Jerome Thai, Nicolas Laurent-Brouty"
__email__ = "jerome.thai@berkeley.edu, nicolas.lb@berkeley.edu"


'''
Scripts for the I-210 sketch
'''

from process_data import extract_features, process_links, geojson_link, \
    process_trips, process_net, process_node, array_to_trips, process_results
from frank_wolfe import solver, solver_2, solver_3
import numpy as np
from metrics import cost, cost_ratio


def process_I210_net():
    process_net('data/I210Sketch_net.csv', 'data/I210_net.csv')


def frank_wolfe_on_I210():
    '''
    Frank-Wolfe on I210
    '''    
    graph = np.loadtxt('data/I210_net.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/I210_od.csv', delimiter=',', skiprows=1)
    demand[:,2] = 1. * demand[:,2] / 4000 
    # run solver
    f = solver_3(graph, demand, max_iter=1000, q=50, display=1, stop=1e-2)
    # display cost
    for a,b in zip(cost(f, graph), f*4000): print a,b
    # visualization
    node = np.loadtxt('data/I210_node.csv', delimiter=',', skiprows=1)
    # extract features: 'capacity', 'length', 'fftt'
    feat = extract_features('data/I210Sketch_net.csv')
    ratio = cost_ratio(f, graph)
    # merge features with the cost ratios
    features = np.zeros((feat.shape[0],4))
    features[:,:3] = feat
    features[:,3] = ratio
    # join features with (lat1,lon1,lat2,lon2)
    links = process_links(graph, node, features)
    color = features[:,3] # we choose the costs
    names = ['capacity', 'length', 'fftt', 'tt_over_fftt']
    geojson_link(links, names, color)


def main():
    #process_I210_net()
    frank_wolfe_on_I210()

if __name__ == '__main__':
    main()