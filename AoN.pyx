"""
Original Algorithm for Shortest path (Dijkstra with a Fibonacci heap) was written by Jake Vanderplas <vanderplas@astro.washington.edu> under license: BSD, (C) 2012

Codes for route ennumeration, DAG construction and Link nesting were written by Pedro Camargo (2013) and have all their rights reserved to the author
"""

import warnings
import numpy as np
cimport numpy as np
cimport cython

include 'parameters.pxi'

#from scipy.sparse import csr_matrix, isspmatrix, isspmatrix_csr, isspmatrix_csc, lil_matrix, lil_matrix, coo_matrix

from libc.stdlib cimport abort, malloc, free


# GRAPH STRUCTURE:  LINK ID, NODE A, NODE B, IMPEDANCE



def AllOrNothing(GRAPH,demand,origin):
    cdef int nodes

    if demand.dtype != "float64":
        print 'EXCEPTION: Demand should be type float (float64). \nData transformed. Possible precision loss'
        demand=demand.astype(float)


    if GRAPH.dtype != "float64":
        print 'EXCEPTION: GRAPH should be type float (float64). \nData transformed. Possible precision loss'
        GRAPH=GRAPH.astype(float)


    links=GRAPH.shape[0] #Number of links in the network
    max_link=int(np.max(GRAPH[:,0])+1) #Max ID link in the  network
    nodes=np.max(GRAPH[:,1:3])+1

    #We start the liloads matrix here to add the flows from start, so we don't
    #have to add the flows from all the iterations/origins
    LILOADS=np.zeros(max_link,dtype=DTYPE)


    a_nodes=np.zeros(links, dtype=ITYPE) #Holds node of origin
    b_nodes=np.zeros(links, dtype=ITYPE) #Holds node of destination
    graph_fs=np.empty(nodes+1, dtype=ITYPE)  #Holds the Forward star for the graph
    graph_n_u=np.zeros(links, dtype=DTYPE) #Holds data for the graph (nested utility)

    a_nodes[:]=GRAPH[:,1].astype(ITYPE)
    b_nodes[:]=GRAPH[:,2].astype(ITYPE)
    graph_n_u[:]=GRAPH[:,3]
    graph_fs.fill(-1)
    ind = np.lexsort((b_nodes,a_nodes)) # Sort by a, then by b
    ind = ind.astype(ITYPE)
    idsgraph=GRAPH[:,0].astype(ITYPE)
    idsgraph[np.arange(links-1)]=idsgraph[ind]

    _Ordering_and_Forward_Star(a_nodes,
                               b_nodes,
                               graph_n_u,
                               ind,
                               graph_fs)

    assigone(demand,graph_n_u, b_nodes, graph_fs,idsgraph,LILOADS, origin)

    return ((origin, LILOADS))




cdef assigone(np.ndarray[DTYPE_t, ndim=1, mode='c'] demand,
            np.ndarray[DTYPE_t, ndim=1, mode='c'] csr_weights,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] csr_indices,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] csr_indptr,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] ids_graph,
            np.ndarray[DTYPE_t, ndim=1, mode='c'] LILOADS,
            int origin):

    cdef int N, number_of_links, init_origin, end_origin, nodes, links, i, j

    #Nodes in our graph
    #The sparse graph has an overhead of one on the shape
    N = csr_indptr.shape[0]-1

    #------------------------------
    # initializes dist_matrix for output
    dist_matrix = np.empty(N, dtype=DTYPE)
    dist_matrix.fill(np.inf)
    dist_matrix[origin] = 0
    umatrix=np.zeros(N, dtype=DTYPE)
    #------------------------------


    #------------------------------
    # initializes predecessors for output
    predecessors = np.empty(N, dtype=ITYPE)
    predecessors.fill(-1)
    #------------------------------

    #------------------------------
    #initializes the matrix that will return the links in the tree
    conn = np.empty(N, dtype=ITYPE)
    conn.fill(-1)
    #------------------------------


    #------------------------------
    #Runs the shortest path algorithm to capture the SPath
    _dijkstra_directed(origin,
                       csr_weights,
                       csr_indices,
                       csr_indptr,
                       dist_matrix,
                       predecessors,
                       ids_graph,
                       conn)
    #------------------------------

    #----------------------------------------------------------------------------------------------
    #performs the assignment itself

    #starts matrices to hold the loads
    nodes=predecessors.size
    links=csr_weights.size


    _assignsAON(predecessors,
         conn,
         demand,
         LILOADS,
         nodes,
         origin)


    index=0
    conn=0

    return 1



@cython.boundscheck(False) # turn of bounds-checking for entire function
cdef _assignsAON(np.ndarray[ITYPE_t, ndim=1, mode='c'] pred,
              np.ndarray[ITYPE_t, ndim=1, mode='c'] conn,
              np.ndarray[DTYPE_t, ndim=1, mode='c'] demand,
              np.ndarray[DTYPE_t, ndim=1, mode='c'] LILOADS,
              int nodes,
              int origin):

    cdef unsigned int t_origin
    cdef ITYPE_t c, o, j, i, p, k
    cdef DTYPE_t d
    cdef unsigned int dests = demand.shape[0]

    for i from 0 <= i < dests:
        if demand[i]>0:
            j=i
            p=pred[j]
            while p>=0:
                c=conn[j]
                LILOADS[c]=LILOADS[c]+demand[i]
                j=p
                p=pred[j]
    return 1



# ############################################################################################################################################################
##############################################################################################################################################################
# ########     CREATES THE FORWARD STAR FOR COMPUTING SHORTEST PATHS   #######################################################################################
##############################################################################################################################################################
# ############################################################################################################################################################
#Procedure to simply get the graph, sort it using the keys in IND
#and prepare the forward star
def Ordering_and_Forward_Star():
    return 'empty'
cdef _Ordering_and_Forward_Star(np.ndarray[ITYPE_t, ndim=1, mode='c'] a_nodes, #A_Node/B_Node
                    np.ndarray[ITYPE_t, ndim=1, mode='c'] b_nodes,
                    np.ndarray[DTYPE_t, ndim=1, mode='c'] graph_n_u,
                    np.ndarray[ITYPE_t, ndim=1, mode='c'] ind,
                    np.ndarray[ITYPE_t, ndim=1, mode='c'] graph_fs):
    cdef int k,l,m
    cdef unsigned int links = a_nodes.shape[0]
    cdef unsigned int nodes = graph_fs.shape[0]
    cdef np.ndarray aux_a=np.zeros(links, dtype=ITYPE)
    cdef np.ndarray aux_b=np.zeros(links, dtype=ITYPE)
    cdef np.ndarray aux_u=np.zeros(links, dtype=DTYPE)
    cdef np.ndarray aux_n_u=np.zeros(links, dtype=DTYPE)

    #Copy data into auxiliary variables
    for k from 0 <= k < links:
        aux_a[k]=a_nodes[k]
        aux_b[k]=b_nodes[k]
        aux_n_u[k]=graph_n_u[k]


#Ordering
    for k from 0 <= k < links:
        l=ind[k]
        a_nodes[k]=aux_a[l]
        b_nodes[k]=aux_b[l]
        graph_n_u[k]=graph_n_u[l]

#Assembling FS
    #First element of the forward star
    l=a_nodes[0]
    graph_fs[l]=0

    for k from 1 <= k < links:
        l=a_nodes[k] #current origin node
        m=a_nodes[k-1] #PREVIUOS origin node
        if l!=m: #If the current link starts after
            graph_fs[l]=k
    #Last elemnt of the FS
    graph_fs[nodes-1]=links


#Filling whatever was not filled in the graph_fs (missing nodes)
    l=0
    for k from 0< k <= nodes:
        m=nodes-k
        if graph_fs[m]>=0:
            l=graph_fs[m]
        if graph_fs[m]==-1:
            graph_fs[m]=l
"""-------------------------------------------------------------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------------------------------------------------------------------------------------------------------------------------"""


#Jake Vanderpla's Dijkstra implementation with path tracking variables added to it
#This code was taken from SciPy V0.11
cdef _dijkstra_directed(int origin,
            np.ndarray[DTYPE_t, ndim=1, mode='c'] csr_weights,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] csr_indices,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] csr_indptr,
            np.ndarray[DTYPE_t, ndim=1, mode='c'] dist_matrix,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] pred,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] ids,
            np.ndarray[ITYPE_t, ndim=1, mode='c'] connectors):

    cdef unsigned int N = dist_matrix.shape[0]
    cdef unsigned int i, k, j_source, j_current
    cdef ITYPE_t j

    cdef DTYPE_t weight

    cdef FibonacciHeap heap
    cdef FibonacciNode *v, *current_node
    cdef FibonacciNode* nodes = <FibonacciNode*> malloc(N *
                                                        sizeof(FibonacciNode))

    j_source=origin

    for k from 0 <= k < N:
        initialize_node(&nodes[k], k)

    dist_matrix[j_source] = 0
    heap.min_node = NULL
    insert_node(&heap, &nodes[j_source])

    while heap.min_node:
        v = remove_min(&heap)
        v.state = SCANNED

        for j from csr_indptr[v.index] <= j < csr_indptr[v.index + 1]:
            j_current = csr_indices[j]
            current_node = &nodes[j_current]
            if current_node.state != SCANNED:
                weight = csr_weights[j]
                if current_node.state == NOT_IN_HEAP:
                    current_node.state = IN_HEAP
                    current_node.val = v.val + weight
                    insert_node(&heap, current_node)
                    pred[j_current] = v.index

                    #The link that took us to such node
                    connectors[j_current] = ids[j]

                elif current_node.val > v.val + weight:
                    decrease_val(&heap, current_node,
                                 v.val + weight)
                    pred[j_current] = v.index

                    #The link that took us to such node
                    connectors[j_current] = ids[j]

        #v has now been scanned: add the distance to the results
        dist_matrix[v.index] = v.val

    free(nodes)


######################################################################
# FibonacciNode structure
#  This structure and the operations on it are the nodes of the
#  Fibonacci heap.
#
cdef enum FibonacciState:
    SCANNED
    NOT_IN_HEAP
    IN_HEAP


cdef struct FibonacciNode:
    unsigned int index
    unsigned int rank
    FibonacciState state
    DTYPE_t val
    FibonacciNode* parent
    FibonacciNode* left_sibling
    FibonacciNode* right_sibling
    FibonacciNode* children


cdef void initialize_node(FibonacciNode* node,
                          unsigned int index,
                          DTYPE_t val=0):
    # Assumptions: - node is a valid pointer
    #              - node is not currently part of a heap
    node.index = index
    node.val = val
    node.rank = 0
    node.state = NOT_IN_HEAP

    node.parent = NULL
    node.left_sibling = NULL
    node.right_sibling = NULL
    node.children = NULL


cdef FibonacciNode* rightmost_sibling(FibonacciNode* node):
    # Assumptions: - node is a valid pointer
    cdef FibonacciNode* temp = node
    while(temp.right_sibling):
        temp = temp.right_sibling
    return temp


cdef FibonacciNode* leftmost_sibling(FibonacciNode* node):
    # Assumptions: - node is a valid pointer
    cdef FibonacciNode* temp = node
    while(temp.left_sibling):
        temp = temp.left_sibling
    return temp


cdef void add_child(FibonacciNode* node, FibonacciNode* new_child):
    # Assumptions: - node is a valid pointer
    #              - new_child is a valid pointer
    #              - new_child is not the sibling or child of another node
    new_child.parent = node

    if node.children:
        add_sibling(node.children, new_child)
    else:
        node.children = new_child
        new_child.right_sibling = NULL
        new_child.left_sibling = NULL
        node.rank = 1


cdef void add_sibling(FibonacciNode* node, FibonacciNode* new_sibling):
    # Assumptions: - node is a valid pointer
    #              - new_sibling is a valid pointer
    #              - new_sibling is not the child or sibling of another node
    cdef FibonacciNode* temp = rightmost_sibling(node)
    temp.right_sibling = new_sibling
    new_sibling.left_sibling = temp
    new_sibling.right_sibling = NULL
    new_sibling.parent = node.parent
    if new_sibling.parent:
        new_sibling.parent.rank += 1


cdef void remove(FibonacciNode* node):
    # Assumptions: - node is a valid pointer
    if node.parent:
        node.parent.rank -= 1
        if node.left_sibling:
            node.parent.children = node.left_sibling
        elif node.right_sibling:
            node.parent.children = node.right_sibling
        else:
            node.parent.children = NULL

    if node.left_sibling:
        node.left_sibling.right_sibling = node.right_sibling
    if node.right_sibling:
        node.right_sibling.left_sibling = node.left_sibling

    node.left_sibling = NULL
    node.right_sibling = NULL
    node.parent = NULL


######################################################################
# FibonacciHeap structure
#  This structure and operations on it use the FibonacciNode
#  routines to implement a Fibonacci heap

ctypedef FibonacciNode* pFibonacciNode


cdef struct FibonacciHeap:
    FibonacciNode* min_node
    pFibonacciNode[100] roots_by_rank  # maximum number of nodes is ~2^100.


cdef void insert_node(FibonacciHeap* heap,
                      FibonacciNode* node):
    # Assumptions: - heap is a valid pointer
    #              - node is a valid pointer
    #              - node is not the child or sibling of another node
    if heap.min_node:
        add_sibling(heap.min_node, node)
        if node.val < heap.min_node.val:
            heap.min_node = node
    else:
        heap.min_node = node


cdef void decrease_val(FibonacciHeap* heap,
                       FibonacciNode* node,
                       DTYPE_t newval):
    # Assumptions: - heap is a valid pointer
    #              - newval <= node.val
    #              - node is a valid pointer
    #              - node is not the child or sibling of another node
    #              - node is in the heap
    node.val = newval
    if node.parent and (node.parent.val >= newval):
        remove(node)
        insert_node(heap, node)
    elif heap.min_node.val > node.val:
        heap.min_node = node


cdef void link(FibonacciHeap* heap, FibonacciNode* node):
    # Assumptions: - heap is a valid pointer
    #              - node is a valid pointer
    #              - node is already within heap

    cdef FibonacciNode *linknode, *parent, *child

    if heap.roots_by_rank[node.rank] == NULL:
        heap.roots_by_rank[node.rank] = node
    else:
        linknode = heap.roots_by_rank[node.rank]
        heap.roots_by_rank[node.rank] = NULL

        if node.val < linknode.val or node == heap.min_node:
            remove(linknode)
            add_child(node, linknode)
            link(heap, node)
        else:
            remove(node)
            add_child(linknode, node)
            link(heap, linknode)


cdef FibonacciNode* remove_min(FibonacciHeap* heap):
    # Assumptions: - heap is a valid pointer
    #              - heap.min_node is a valid pointer
    cdef FibonacciNode *temp, *temp_right, *out
    cdef unsigned int i

    # make all min_node children into root nodes
    if heap.min_node.children:
        temp = leftmost_sibling(heap.min_node.children)
        temp_right = NULL

        while temp:
            temp_right = temp.right_sibling
            remove(temp)
            add_sibling(heap.min_node, temp)
            temp = temp_right

        heap.min_node.children = NULL

    # choose a root node other than min_node
    temp = leftmost_sibling(heap.min_node)
    if temp == heap.min_node:
        if heap.min_node.right_sibling:
            temp = heap.min_node.right_sibling
        else:
            out = heap.min_node
            heap.min_node = NULL
            return out

    # remove min_node, and point heap to the new min
    out = heap.min_node
    remove(heap.min_node)
    heap.min_node = temp

    # re-link the heap
    for i from 0 <= i < 100:
        heap.roots_by_rank[i] = NULL

    while temp:
        if temp.val < heap.min_node.val:
            heap.min_node = temp
        temp_right = temp.right_sibling
        link(heap, temp)
        temp = temp_right

    return out






