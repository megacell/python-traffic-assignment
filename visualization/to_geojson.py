__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
This module generates geojson files
'''

import numpy as np
from process_data import extract_features, process_links

begin = 'var geojson_features = [{\n'


def begin_feature(type):
    string = '    "type": "Feature",\n    "geometry": {\n'
    begin_coord = '        "coordinates": [\n'
    return string + '        "type": "{}",\n'.format(type) + begin_coord

def coord(lat,lon,type):
    if type == "LineString": return '            [{}, {}],\n'.format(lon,lat)
    if type == "Point": return '            [{}, {}]'.format(lon,lat)

begin_prop = '            ]},\n    "properties": {\n'

def prop(name, value):
    return '        "{}": "{}",\n'.format(name, value)

def prop_numeric(name, value):
    return '        "{}": {},\n'.format(name, value)


def geojson_link(links, features):
    """
    from array of link coordinates and features, generate geojson file
    links is numpy array where each row has [lat1, lon1, lat2, lon2, features]
    """
    type = 'LineString'
    out = [begin]
    for i in range(links.shape[0]):
        out.append(begin_feature(type))
        out.append(coord(links[i,0], links[i,1], type))
        out.append(coord(links[i,2], links[i,3], type))
        out.append(begin_prop)
        for j,f in enumerate(features):
            out.append(prop(f, links[i,j+4]))
        out.append('    }},{\n')
    out[-1] = '    }}];\n\n'
    out.append('var lat_center_map = {}\n'.format(np.mean(links[:,0])))
    out.append('var lon_center_map = {}\n'.format(np.mean(links[:,1])))
    with open('visualization/links.js', 'w') as f:
        f.write(''.join(out))


def main():
    net = np.loadtxt('data/Chicago_net.csv', delimiter=',', skiprows=1)
    node = np.loadtxt('data/Chicago_node.csv', delimiter=',', skiprows=1)
    features = extract_features('data/ChicagoSketch_net.txt')
    links = process_links(net, node, features)
    geojson_link(links, ['capacity', 'length', 'fftt'])


if __name__ == "__main__":
    main()
