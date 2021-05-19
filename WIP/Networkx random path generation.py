# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 15:33:34 2021

@author: wills
"""

import networkx as nx
import random



#-----------------------------------------------------------------------------

# Function which generates all possible paths for a given network G
# Inputs:
    # G = Network in the form of an nx graph
    # ent = Position of entrance node(s)
    # ext = Position of exit node()
# Outputs:
    # paths = List of all possible paths

def possible_paths(G, ent, ext):
    paths = []
    
    for i in nx.all_simple_paths(G, source =ent, target = ext):
        paths.append(i)
    return(paths)

#  TO DO: Add input sanitisation for function

#-----------------------------------------------------------------------------


# Function which randomly selects a path when given the list of possible paths
# Inputs:
    # paths = list of all possible paths
# Outputs:
    # indv_path = The randomly generated individual path

def rand_path(paths):
    rand_int = random.randint(0,len(paths))
    indv_path = paths[rand_int]
    print('Individual Path:',indv_path,"\n",'Path Number:',rand_int,"\n",'Total Paths:',len(paths))

#  TO DO: Add input sanitisation for function

#-----------------------------------------------------------------------------


# Example shop layout network for aldi with one entrance at (0,0) and two exits at (6,6) and (7,6)
# Shop has 8 ailes

G = nx.grid_2d_graph(8,7)


# Removing nodes and edges from grid to make shop layout
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
        

# Inline callback for functions in this file
# Using these lines in other scripts will call functions from this file
paths = possible_paths(G, (0,0),[(6,6),(7,6)])
rand_path(paths)  
        



