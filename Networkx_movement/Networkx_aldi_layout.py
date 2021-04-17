# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 19:53:35 2021

@author: wills
"""

import networkx as nx 

# Example shop layout network for aldi with one entrance at (0,0) and two exits at (6,6) and (7,6)
# Shop has 8 ailes

def aldi_layout():

    G = nx.grid_2d_graph(8,7)
    
    for m in [1,2,3,4,5,6,7]:
        G.remove_node((m,0))
    for o in [0,1,2,3,4,5]:
        G.remove_node((o,6))
    
    for n in [0,1,2,3,4,5,6]:  
        for i in [2,3,4]:
            G.remove_edge((n,i),((n+1),i))
    G.remove_edge((6,6),(7,6))
    
    # Drawing of example shop layout network
    pos = dict(zip(G,G))
    nx.draw(G,pos,with_labels=True)
    return G