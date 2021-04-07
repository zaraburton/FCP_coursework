import networkx as nx
import matplotlib as plt
import matplotlib.pyplot as plt
###This code creates a network as a first attempt at simulating the path through a shop, includes the succesful weighting of edges at entrance and exit
def add_edge_to_graph(G, e1, e2, w):
    G.add_edge(e1, e2, weight=w)
G = nx.Graph()
points = [(10,0), (10,10), (10,4), (7,10),(7,7),(7,4),(7,2),(4,7),(4,3),(4,0),(1,7),(1,4), (1,1)]
# nodes 1 node 2 and weight
edges = [(0, 2, 10), (2, 1, 1), (1, 3, 1), (4, 3, 1), (4, 7, 1),(7, 10, 1), (10, 11, 1), (11, 12, 1), (5, 6, 1), (6, 8, 1),(8, 9, 10), (11, 12, 10), (3, 6, 1)]

for i in range(len(edges)):
    add_edge_to_graph(G, points[edges[i][0]], points[edges[i][1]], edges[i][2])
pos = {point: point for point in points}
# add axis
fig, ax = plt.subplots()
nx.draw(G, pos=pos, node_color='k', ax=ax)
nx.draw(G, pos=pos, node_size=100, ax=ax)  # draw nodes and edges
#nx.draw_networkx_labels(G, pos=pos)  # draw node labels/names
# draw edge weights
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
plt.axis("on")
ax.set_xlim(0, 12)
ax.set_ylim(0,12)
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
plt.show()
plt.savefig('Network path.png')