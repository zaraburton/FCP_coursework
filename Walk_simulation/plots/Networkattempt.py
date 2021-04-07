import networkx as nx
import matplotlib as plt
import matplotlib.pyplot as plt
#creating an empty graph, S variable

S = nx.Graph()
#nodelist = ['a','b','c','d','e','f','g','h', 'i', 'j','k','l','m']
#S.add_nodes_from(nodelist)
#adding a lits of nodes
S.add_node('a',pos =(10,1))
S.add_node('b',pos =(10,2))
S.add_node('l',pos =(10,7))
S.add_node('k',pos =(7,7))
S.add_node('c',pos =(7,5))
S.add_node('d',pos =(7,2))
S.add_node('e',pos =(7,1))
S.add_node('h',pos =(4,5))
S.add_node('f',pos =(4,1))
S.add_node('m',pos =(4,0))
S.add_node('i',pos =(1,5))
S.add_node('g',pos =(1,2))
S.add_node('j',pos =(1,1))
#nx.set_node_attributes(S,pos)
# adding a list of edges and specifying edges to have characteristics which could relate to time spent between them:
S.add_weighted_edges_from([('a','b',1), ('b','c',2), (('b','d',1)), (('b','l',1)), (('l','k',1)), (('c','k',4)), (('c','h',4)),(('i','h',1)),(('i','g',1)),(('f','g',1)),(('f','m',6)),(('f','e',1)),(('d','e',1)),(('g','j',6))])

nx.draw(S)
plt.savefig("simple_path.png") # save as png
plt.show() # display
#x y co-ord of points
points = [(10,1), (10,7), (10,2), (7,7),(7,5),(7,2),(7,1),(4,5),(4,1),(4,0),(1,5),(1,2), (1,1)]
# nodes 1 node 2 and weight
edges = [(0, 1, 10), (1, 2, 5), (2, 3, 25), (0, 3, 3), (3, 4, 8),(8, 2, 10), (7, 4, 5), (3, 4, 25), (5, 6, 3), (7, 8, 8),(9, 10, 10), (11, 10, 5), (12, 13, 25)]

for i in range(len(edges)):
    add_edge_to_graph(G, points[edges[i][0]], points[edges[i][1]], edges[i][2])

pos = {point: point for point in points}
# add axis
fig, ax = plt.subplots()
nx.draw(G, pos=pos, node_color='k', ax=ax)
nx.draw(G, pos=pos, node_size=1500, ax=ax)  # draw nodes and edges
nx.draw_networkx_labels(G, pos=pos)  # draw node labels/names
# draw edge weights
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
plt.axis("on")
ax.set_xlim(0, 11)
ax.set_ylim(0,11)
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
plt.show()