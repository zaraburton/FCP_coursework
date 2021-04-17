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
    # ent = Position of entrance node
    # ext = Position of exit node
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
    return indv_path


#  TO DO: Add input sanitisation for function

#-----------------------------------------------------------------------------


# Inline callback for functions in this file
# Using these lines in other scripts will call functions from this file
#paths = possible_paths(G, (0,0),[(6,6),(7,6)])
#rand_path(paths)  




