# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 15:33:34 2021

@author: wills & hannahs
"""

import networkx as nx
import random
from itertools import chain, repeat


#-----------------------------------------------------------------------------

# Function which generates all possible paths for a given network G
# Inputs:
    # G = Network in the form of an nx graph
    # ent = Position of entrance node
    # ext = Position of exit node
# Outputs:
    # paths = List of all possible paths

#list of all possible paths in shop
def possible_paths(G, ent, ext):
    paths = []
    for i in nx.all_simple_paths(G,source = ent,target = ext):
        paths.append(i)
    return(paths)


#list of shortest paths in shop so for fast shoppers
def fast_paths(G,ent,ext):
    short_paths = []
    for i in nx.all_simple_paths(G,source = ent,target = ext):
        if len(i) <= 12:
            continue
        short_paths.append(i)
    return(short_paths)

def slow_paths(G,ent,ext):
    long_paths = []
    for i in nx.all_simple_paths(G,source = ent,target = ext):
        y = [2] * len(i)
        chain.from_iterable((repeat(item, count) for item, count in zip(i, y)))
        i = list(chain.from_iterable((repeat(item, cnt) for item, cnt in zip(i, y))))
        long_paths.append(i)
    return(long_paths)


def possible_paths_oneway(G, ent, ext):
    paths = []

    # Nx for loop which outputs every possible simple path
    # Each individual path in the for-loop is i
    for i in nx.all_simple_paths(G, source=ent, target=ext):

        # Defining logic terms for even and odd aisles
        logic_even = True
        logic_odd = True

        # Each individual path, i, is made up from a list of tuples, which are coordinates on the nx plot
        # The for-loop iterates for each tuple in the individual path
        # count is the position of the tuple in the individual path
        # n is the tuple itself
        for count, n in enumerate(i):

            # if the first coordinate (x) in tuple is positive
            # then the second coordinate (y) in tuple is stored
            # then variable setup called p which represents the next tuple in the individual path
            if (n[0]) % 2 == 0:
                previous_y_even = n[1]
                p = count + 1

                # If statement to stop code running when the exit nodes are reached
                if p > len(i) - 2:
                    break
                else:

                    # If the second coordinate in next tuple is smaller than second coordinate in initial tuple
                    # Then the path must be moving down an even aisle which is against the one way system
                    if i[p][1] < previous_y_even:

                        # Then the even aisle logic is set to false and the route will not be appended
                        logic_even = False
                        break
                    else:
                        continue
                    break


            # Same code as before but looking at odd aisles

            else:
                previous_y_odd = n[1]
                p = count + 1
                if p > len(i) - 2:
                    break
                else:
                    if i[p][1] > previous_y_odd:
                        logic_even = False
                        break
                    else:
                        continue
                    break

        # If throughout all loops both logics are true, then the oneway system was adhered to and the route is added to list

        if logic_even == True and logic_odd == True:
            paths.append(i)
            continue
        else:
            continue
    return (paths)


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




