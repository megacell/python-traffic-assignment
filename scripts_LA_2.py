__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import numpy as np
from process_data import map_nodes_to_cities, map_links_to_cities, process_links, \
    geojson_link, cities_to_js
from scripts_LA import load_LA_3


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


def main():
    # map_nodes_to_cities(cities, 'visualization/cities.js', 'data/LA_node.csv', \
    #     'data/LA/node_to_cities.csv')
    # map_links_to_cities('data/LA/node_to_cities.csv', 'data/LA_net.csv', \
    #     'data/LA/link_to_cities.csv')
    visualize_links_by_city('Glendale')
    #visualize_cities()


if __name__ == '__main__':
    main()