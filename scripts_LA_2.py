__author__ = "Jerome Thai, Nicolas Laurent-Brouty"
__email__ = "jerome.thai@berkeley.edu, nicolas.lb@berkeley.edu"

import numpy as np
from process_data import map_nodes_to_cities, map_links_to_cities, process_links, \
    geojson_link, cities_to_js, process_net_attack
from scripts_LA import load_LA_3
from utils import modify_capacity,multiply_cognitive_cost
from frank_wolfe_heterogeneous import parametric_study_2, parametric_study_3
from metrics import average_cost_all_or_nothing, all_or_nothing_assignment, \
    cost_ratio, cost, save_metrics, path_cost
from metrics import *




cities = ['Burbank',
    'Glendale',
    'La Canada Flintridge',
    'Pasadena',
    'South Pasadena',
    'Alhambra',
    'San Marino',
    'San Gabriel',
    'Temple City',
    'Arcadia',
    'Sierra Madre',
    'Monrovia',
    'Monterey Park',
    'Rosemead',
    'El Monte',
    'South El Monte',
    'Montebello',
    'Pico Rivera',
    'Irwindale',
    'Baldwin Park',
    'West Covina',
    'Azusa',
    'Covina',
    'Duarte',
    'Glendora']


def visualize_cities():
    cities_to_js('data/cities.js', 'Los Angeles', 0, 1)


def visualize_links_by_city(city):
    # visualize the links from a specific city
    graph, demand, node, features = load_LA_3()
    linkToCity = np.genfromtxt('data/LA/link_to_cities.csv', delimiter=',', \
        skiprows=1, dtype='str')
    links = process_links(graph, node, features, in_order=True)
    names = ['capacity', 'length', 'fftt']
    color = 3*(linkToCity[:,1] == city)
    color = color + 10*(features[:,0] > 900.)
    weight = (features[:,0] <= 900.) + 3.*(features[:,0] > 900.)
    geojson_link(links, names, color, weight)


def process_LA_net_attack(thres,beta):
    process_net_attack('data/LA_net.txt', 'data/LA_net_attack.csv',thres,beta)


def load_LA_4():
    graph = np.loadtxt('data/LA_net_attack.csv', delimiter=',', skiprows=1)
    demand = np.loadtxt('data/LA_od_3.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/LA_node.csv', delimiter=',')
    # features = table in the format [[capacity, length, FreeFlowTime]]
    features = extract_features('data/LA_net.txt')
    # increase capacities of these two links because they have a travel time
    # in equilibrium that that is too big
    features[10787,0] = features[10787,0] * 1.5
    graph[10787,-1] = graph[10787,-1] / (1.5**4)
    features[3348,:] = features[3348,:] * 1.2
    graph[3348,-1] = graph[3348,-1] / (1.2**4)
    # divide demand going to node 106 by 10 because too large
    for i in range(demand.shape[0]):
        if demand[i,1] == 106.:
            demand[i,2] = demand[i,2] / 10.
    return graph, demand, node, features


def LA_parametric_study_attack(alphas,thres,betas):
    for beta in betas:
        net2, d, node, features = LA_metrics_attacks_all(beta, thres)
        parametric_study_3(alphas, beta, net2, d, node, features, 1000., 3000., 'data/LA/test_attack_{}_{}.csv',\
        stop=1e-2)

#beta is the coefficient of reduction of capacity: capacity = beta*capacity
#load_LA_4() loads the modified network
def LA_metrics_attack(alphas, input, output, beta):
    net, d, node, features = load_LA_4()
    # import pdb; pdb.set_trace()
    d[:,2] = d[:,2] / 4000.
    net2, small_capacity = multiply_cognitive_cost(net, features,beta, 1000., 3000.)
    save_metrics(alphas, net, net2, d, features, small_capacity, input, \
        output, skiprows=1, \
        length_unit='Meter', time_unit='Second')

def LA_metrics_attack_2(alphas, input, output, thres, beta):
    net, d, node, features = LA_metrics_attacks_all(beta, thres)
    net2, small_capacity = multiply_cognitive_cost(net, features, 1000., 3000.)
    save_metrics(alphas, net, net2, d, features, small_capacity, input, \
        output, skiprows=1, \
        length_unit='Meter', time_unit='Second')

def LA_metrics_attacks_city(beta, thres, city):
    net, d, node, features = load_LA_3()
    # import pdb; pdb.set_trace()
    d[:,2] = d[:,2] / 4000.

    # extract the mapping from links to cities
    linkToCity = np.genfromtxt('data/LA/link_to_cities.csv', delimiter=',', \
        skiprows=1, dtype='str')
    print linkToCity
    links_affected = np.logical_and(linkToCity[:,1] == city, features[:,0] < thres)
    print np.sum(links_affected)
    # modify all small capacity links in GLendale
    net2 = modify_capacity(net, links_affected, beta)

def LA_metrics_attacks_all(beta, thres):
    net, d, node, features = load_LA_3()
    # import pdb; pdb.set_trace()
    d[:,2] = d[:,2] / 4000.

    # modify all small capacity links
    links_affected = (features[:,0] < thres)
    net2 = modify_capacity(net, links_affected, beta)
    return net2, d, node, features


def compute_metrics_beta(alpha, beta, f, net, d, feat, subset, out, row, fs=None, net2=None, \
    length_unit='Mile', time_unit='Minute'):
    '''
    Save in the numpy array 'out' at the specific 'row' the following metrics
    - average cost for non-routed
    - average cost for routed
    - average cost
    - average cost on a subset (e.g. local routes)
    - average cost outside of a subset (e.g. non-local routes)
    - total gas emissions
    - total gas emissions on a subset (e.g. local routes)
    - total gas emissions outside of a subset (e.g. non-local routes)
    - total flow in the network
    - total flow in the network on a subset (e.g. local routes)
    - total flow in the network outside of a subset (e.g. non-local routes)
    '''
    if length_unit == 'Meter':
        lengths = feat[:,1] / 1609.34 # convert into miles
    elif length_unit == 'Mile':
        lengths = feat[:,1]
    if time_unit == 'Minute':
        a = 60.0
    elif time_unit == 'Second':
        a = 3600.
    b = 60./a
    speed = a * np.divide(lengths, np.maximum(cost(f, net), 10e-8))
    co2 = np.multiply(gas_emission(speed), lengths)
    out[row,0] = alpha
    out[row,1] = beta
    out[row,4] = b * average_cost(f, net, d)
    out[row,5] = b * average_cost_subset(f, net, d, subset)
    out[row,6] = out[row,3] - out[row,4]
    out[row,7] = co2.dot(f) / f.dot(lengths)
    out[row,8] = np.multiply(co2, subset).dot(f) / f.dot(lengths)
    out[row,9] = out[row,6] - out[row,7]
    out[row,10] = np.sum(np.multiply(f, lengths)) * 4000.
    out[row,11] = np.sum(np.multiply(np.multiply(f, lengths), subset)) * 4000.
    out[row,12] = out[row,9] - out[row,10]
    if alpha == 0.0:
        out[row,2] = b * average_cost(f, net, d)
        out[row,3] = b * average_cost_all_or_nothing(f, net, d)
        return
    if alpha == 1.0:
        L = all_or_nothing_assignment(cost(f, net2), net, d)
        out[row,2] = b * cost(f, net).dot(L) / np.sum(d[:,2])
        out[row,3] = b * average_cost(f, net, d)
        return
    out[row,2] = b * cost(f, net).dot(fs[:,0]) / np.sum((1-alpha)*d[:,2])
    out[row,3] = b * cost(f, net).dot(fs[:,1]) / np.sum(alpha*d[:,2])

def save_metrics_beta_LA(alphas, betas, thres, input, output, skiprows=0, \
    length_unit='Mile', time_unit='Minute'):
    out = np.zeros((len(alphas)*len(betas),13))
    for beta in betas:

        net, d, node, features = LA_metrics_attacks_all(beta, thres)
        net2, small_capacity = multiply_cognitive_cost(net, features, 1000., 3000.)

        subset = small_capacity


        a = 0
        if alphas[0] == 0.0:
            alpha = 0.0
            print 'compute for nr = {}, r = {}'.format(1-alphas[0], alphas[0])
            fs = np.loadtxt(input.format(int(alpha*100),int(beta*100)), delimiter=',', \
                skiprows=skiprows)
            f = np.sum(fs, axis=1)
            compute_metrics_beta(0.0, beta, f, net, d, features, subset, out, 0, \
                length_unit=length_unit, time_unit=time_unit)
            a = 1

        b = 1 if alphas[-1] == 1.0 else 0
        for i,alpha in enumerate(alphas[a:len(alphas)-b]):
            print 'compute for nr = {}, r = {}'.format(1-alpha, alpha)
            fs = np.loadtxt(input.format(int(alpha*100),int(beta*100)), delimiter=',', \
                skiprows=skiprows)
            f = np.sum(fs, axis=1)
            compute_metrics_beta(alpha, beta, f, net, d, features, subset, out, i+a, fs=fs, \
                length_unit=length_unit, time_unit=time_unit)

        if alphas[-1] == 1.0:
            alpha = 1.0
            print 'compute for nr = {}, r = {}'.format(1-alphas[-1], alphas[-1])
            fs = np.loadtxt(input.format(int(alpha*100),int(beta*100)), delimiter=',', \
                skiprows=skiprows)
            f = np.sum(fs, axis=1)
            compute_metrics_beta(1.0, beta, f, net, d, features, subset, out, -1, net2=net2, \
                length_unit=length_unit, time_unit=time_unit)

    colnames = 'ratio_routed,beta,tt_non_routed,tt_routed,tt,tt_local,tt_non_local,gas,gas_local,gas_non_local,'
    colnames = colnames + 'vmt,vmt_local,vmt_non_local'
    np.savetxt(output, out, delimiter=',', \
        header=colnames, \
        comments='')

def LA_metrics_attack_3(alphas, betas, input, output, thres):
    save_metrics_beta_LA(alphas, betas, thres, input, output, skiprows=1, \
        length_unit='Meter', time_unit='Second')

def main():
    # map_nodes_to_cities(cities, 'visualization/cities.js', 'data/LA_node.csv', \
    #     'data/LA/node_to_cities.csv')
    # map_links_to_cities('data/LA/node_to_cities.csv', 'data/LA_net.csv', \
    #     'data/LA/link_to_cities.csv')
    # visualize_links_by_city('Glendale')
    #visualize_cities()


    #=================================Attack================================
    #LA_metrics_attacks_city(0.5, 1000.,'Glendale')
    LA_parametric_study_attack(.2,1000.,np.linspace(0.5,1.,6))
    #LA_metrics_attack_3(np.array([0.50]), np.array([0.90]), 'data/LA/test_attack_{}_{}.csv', 'data/LA/out_attack.csv', 1000.)

    #LA_metrics_attack(np.linspace(0,1,11), 'data/LA/test_{}.csv', 'data/LA/out_attack.csv',1.0)


if __name__ == '__main__':
    main()


