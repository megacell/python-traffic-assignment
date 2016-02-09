#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Pedro
#
# Created:     14/10/2013
# Copyright:   (c) Pedro 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np
import os, sys
import AoN
from scipy.sparse import csr_matrix

def main(graph='graph.csv', matrix='matrix.csv'):

    dire_data=os.getcwd()
    dire=os.getcwd()

#We load the data
    graph=np.loadtxt(graph, delimiter=',', skiprows=1)
    j=np.loadtxt(matrix, delimiter=',', skiprows=1)

#Characteristics of the graph
    zones=int(np.max(j[:,0:2])+1)
    links=int(np.max(graph[:,0])+1)

#Builds the matrix on a sparse format because the matrix is too big and too sparse
    matrix=csr_matrix((j[:,2],(j[:,0].astype(int),j[:,1].astype(int))), shape=(zones,zones), dtype="float64")



#Prepares arrays for assignment
    L=np.zeros(links,dtype="float64")
    demand=np.zeros(zones,dtype="float64")


    for i in range(int(zones)): #We assign all zones
        if matrix.indptr[i+1]>matrix.indptr[i]: #Only if there are flows for that particular zone
            demand.fill(0) #We erase the previous matrix array for assignment
            demand[matrix.indices[matrix.indptr[i]:matrix.indptr[i+1]]]=matrix.data[matrix.indptr[i]:matrix.indptr[i+1]] #Fill it in with the new information
            zones, loads=AoN.AllOrNothing(graph,demand,i)  #And assign
            L=L+loads
            print 'Origin ' + str(zones)+' assigned'

    w=open('RESULT.CSV','w')
    print >> w, 'Link,NodeA,NodeB,LOAD'
    for i in range(links-1):
        if L[i]>0:
            print >> w, i,',', graph[i,1],',', graph[i,2],',',L[i]
    w.flush()
    w.close()

    print "DONE"



if __name__ == '__main__':
    main()


