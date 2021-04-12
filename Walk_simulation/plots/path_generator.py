import networkx as nx
import pandas as pd
import copy
import matplotlib as plt
import matplotlib.pyplot as plt
import string
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

#setting node characteristics, defining till and entrance nodes
till_nodes = [(10,0),(4,0)]
entrance_nodes = [(10,1)]
aisle_nodes = [(10,10), (10,4), (7,10),(7,7),(7,5),(7,3),(4,7),(4,3),(1,7),(1,4), (4,10), (1,10)]

#relabelling the nodes as names of what they represent
mapping= { 0: "entrance",1: "aisle2",2: "aisle1",3:"aisle3",4:"aisle4",5:"aisle5",6:"aisle6",7:"aisle7",8:"aisle8",9:"till1",10:"aisle9",11:"aisle10",12:"till2",13:"aisle11",14:"aisle12"}
G = nx.relabel_nodes(G, mapping)

#mapping = dict(zip(G, string.ascii_lowercase))
#G = nx.relabel_nodes(G, mapping)

def set_node_characteristic(G,n,value):
    ''' Where the G and n are the graph and node that are being assigned a value relating to the time spent at the node'''
    return nx.set_node_attributes(G,n,value)

nx.set_node_attributes(G, {0:5, 8:5}, 'time')
G.nodes(data=True)
till_nodes = set_node_characteristic(G,till_nodes,5)
entrance_nodes = set_node_characteristic(G,entrance_nodes,5)
aisle_nodes = set_node_characteristic(G,aisle_nodes,1)

print(G.nodes.data)

#this is the function to get the paths between the nodes, n1 is entrance node, n2 is exit node
def path_entrance_to_till(G,n1,n2):
    return nx.shortest_path(G,n1,n2)

paths1 = path_entrance_to_till(G, (10,0),(4,0))
paths2 = path_entrance_to_till(G, (10,0),(1,0))

#function to enable plotting of the shortest path in BLUE
def node_colors(G, path):
    colours = []
    for node in G.nodes():
        if node in path:
            colours.append('b')
        else:
            colours.append('r')
    return colours
colours = node_colors(G,paths2)
nx.draw_networkx_nodes(G, pos=pos, node_color=colours)
nx.draw_networkx_edges(G, pos=pos)
plt.show()
