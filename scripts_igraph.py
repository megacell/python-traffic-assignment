__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"


from igraph import Graph
import numpy as np

graph=np.loadtxt('data/I210/graph.csv', delimiter=',')
od=np.loadtxt('data/I210/od.csv', delimiter=',')
#vertices = [i for i in range(7)]
#edges = [(0,2),(0,1),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,0),(3,1),(3,2),(2,4),(4,5),(4,6),(5,4),(5,6),(6,4),(6,5)]
#g = Graph(vertex_attrs={"label":vertices}, edges=edges, directed=True)


vertices = range(int(np.max(graph[:,1:3]))+1)
#print vertices
edges = graph[:,1:3].astype(int).tolist()
weights = graph[:,3].tolist()
#print edges
#print weights
g = Graph(vertex_attrs={"label":vertices}, edges=edges, directed=True)
out = g.get_shortest_paths(18, to=19, weights=weights, output="vpath")
print out
out = g.get_shortest_paths(18, to=[11,19], weights=weights, output="epath")
print out
#print [e for e in g.es]

g.es["weight"] = weights
out = g.get_shortest_paths(18, to=19, weights="weight", output="vpath")
print out
out = g.get_shortest_paths(18, to=[11,19], weights="weight", output="epath")
print out
L = np.zeros(len(edges))
L[out[1]] = 10.
L[out[1]] = 10. + L[out[1]]
L[[39,40,38]] =  10. + L[[39,40,38]]
print L
# graph=np.loadtxt('data/graph.csv', delimiter=',', skiprows=1)
# od=np.loadtxt('data/matrix.csv', delimiter=',', skiprows=1)
# print np.max(graph[:,1:3])
# print np.min(graph[:,1:3])
# print np.max(od[:,:2])
# print np.min(od[:,:2])