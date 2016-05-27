__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import numpy as np
from process_data import map_nodes_to_cities, map_links_to_cities, process_links, \
    geojson_link, cities_to_js, process_net_attack
from scripts_LA import load_LA_3
from utils import modify_capacity


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


def LA_parametric_study_attack(alphas,thres,beta):
    process_LA_net_attack(thres,beta)
    g, d, node, feat = load_LA_4()
    d[:,2] = d[:,2] / 4000.
    parametric_study_2(alphas, g, d, node, feat, 1000., 3000., 'data/LA/test_attack_{}.csv',\
        stop=1e-3)



#beta is the coefficient of reduction of capacity: capacity = beta*capacity
#load_LA_4() loads the modified network
def LA_metrics_attack(alphas, input, output, beta):
    net, d, node, features = load_LA_4()
    # import pdb; pdb.set_trace()
    d[:,2] = d[:,2] / 4000.
    net2, small_capacity = multiply_cognitive_cost_attack(net, features,beta, 1000., 3000.)
    save_metrics(alphas, net, net2, d, features, small_capacity, input, \
        output, skiprows=1, \
        length_unit='Meter', time_unit='Second')


def LA_metrics_attacks_2(beta, thres):
    net, d, node, features = load_LA_3()
    # import pdb; pdb.set_trace()
    d[:,2] = d[:,2] / 4000.

    # modify all small capacity links
    links_affected = (features[:,0] < thres)
    net2 = modify_capacity(net, links_affected, beta)

    # extract the mapping from links to cities
    linkToCity = np.genfromtxt('data/LA/link_to_cities.csv', delimiter=',', \
        skiprows=1, dtype='str')
    print linkToCity
    links_affected = np.logical_and(linkToCity[:,1] == 'Glendale', features[:,0] < thres)
    print np.sum(links_affected)
    # modify all small capacity links in GLendale
    net2 = modify_capacity(net, links_affected, beta)



def main():
    # map_nodes_to_cities(cities, 'visualization/cities.js', 'data/LA_node.csv', \
    #     'data/LA/node_to_cities.csv')
    # map_links_to_cities('data/LA/node_to_cities.csv', 'data/LA_net.csv', \
    #     'data/LA/link_to_cities.csv')
    # visualize_links_by_city('Glendale')
    #visualize_cities()


    #=================================Attack================================
    LA_metrics_attacks_2(0.5, 1000.)
    #LA_parametric_study_attack(.9,1000.,1.)
    #LA_metrics_attack(np.linspace(0,1,11), 'data/LA/test_{}.csv', 'data/LA/out_attack.csv',1.0)


if __name__ == '__main__':
    main()


