__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

'''
This module processes the *.txt files from Bar-Gera 
that can be found here: http://www.bgu.ac.il/~bargera/tntp/
'''

import csv
import numpy as np


def process_net(input, output):
    flag = False
    i = 0
    out = ['LINK,A,B,a0,a1,a2,a3,a4\n']
    with open(input, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)>0:
                if flag == False:
                    if row[0].split()[0] == '~': flag = True
                else:
                    l = row[0].split()[:-1]
                    a4 = float(l[4]) * float(l[5]) / (float(l[2])/4000)**4
                    out.append('{},{},{},{},0,0,0,{}\n'.format(i,l[0],l[1],l[4],a4))
                    i = i+1
    with open(output, "w") as text_file:
        text_file.write(''.join(out))



def process_trips(input, output):
    origin = -1
    out = ['O,D,Ton\n']
    with open(input, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #before, keyword, after = row.partition('Origin')
            if len(row)>0: 
                l = row[0].split()
                if l[0] == 'Origin':
                    origin = l[1]
                elif origin != -1:
                    for i,e in enumerate(l):
                        if i%3 == 0:
                            out.append('{},{},'.format(origin,e))
                        if i%3 == 2:
                            out.append('{}\n'.format(e[:-1]))
    with open(output, "w") as text_file:
        text_file.write(''.join(out))


def process_results(input, output, network):
    graph = np.loadtxt(network, delimiter=',', skiprows=1)
    raw = np.loadtxt(input, delimiter=',')
    out = np.zeros(graph.shape[0])
    for i in range(graph.shape[0]):
        for j in range(raw.shape[0]):
            if (graph[i,1] == raw[j,0]) and (graph[i,2] == raw[j,1]):
                out[i] = raw[j,2]
                continue
    np.savetxt(output, out, delimiter=",")


def main():
    # process_trips('data/SiouxFalls_trips.txt', 'data/SiouxFalls_od.csv')
    # process_trips('data/Anaheim_trips.txt', 'data/Anaheim_od.csv')
    # process_trips('data/ChicagoSketch_trips.txt', 'data/Chicago_od.csv')
    # process_results('data/Anaheim_raw_results.csv', 'data/Anaheim_results.csv',\
    #    'data/Anaheim_net.csv')
    process_net('data/ChicagoSketch_net.txt', 'data/Chicago_net.csv')

if __name__ == '__main__':
    main()