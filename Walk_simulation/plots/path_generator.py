import networkx as nx
import pandas as pd
import copy
import matplotlib as plt
import matplotlib.pyplot as plt
'''Function to create lists of the paths between tills and the entrance from G'''
def add_edge_to_graph(G, e1, e2, w):
    G.add_edge(e1, e2, weight=w)
G = nx.Graph()
#specifying the x y co-ordinates of the nodes in the shope
points = [(10,0), (10,10), (10,4), (7,10),(7,7),(7,5),(7,3),(4,7),(4,3),(4,0),(1,7),(1,4), (1,0),(4,10), (1,10)]
# nodes 1 node 2 and weight (where node 0 is the first node in points and node 1 is the 2nd ect)
edges = [(0, 2, 10), (2, 1, 1), (1, 3, 1), (4, 3, 1), (4, 7, 1),(7, 10, 1), (10, 11, 1), (11, 12, 1), (5, 6, 1), (6, 8, 1),(8, 9, 10), (11, 12, 10), (3, 6, 1), (13,14,1),(8,13,1)]
#adding edges to graph for the range of edges specified in edges
for i in range(len(edges)):
    add_edge_to_graph(G, points[edges[i][0]], points[edges[i][1]], edges[i][2])
pos = {point: point for point in points}

print(" The number of nodes: {:d}".format(len(G.nodes())))
print(" The number of edges: {:d}".format(len(G.edges())))

#this is the function to get the paths between the nodes, n1 is entrance node, n2 is exit node
def paths_entrance_to_till(G,n1,n2):
    nx.all_simple_paths(G,n1,n2)

paths1 = nx.all_simple_paths(G, (10,0),(4,0))
paths2 = nx.all_simple_paths(G, (10,0),(1,0))
#printing the list of the paths
print(list(paths1))
print(list(paths2))
#plotting path1 nodes as blue for visulisation
node_colors = ["blue" if n in list(paths1) else "red" for n in G.nodes()]
nx.draw_networkx_nodes(G, pos=pos, node_color=node_colors)
nx.draw_networkx_edges(G, pos=pos)
plt.show()
