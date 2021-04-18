#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import simpy
import random
import statistics
import Networkx as nx
import Networkx random path generation.py

time_in_shop = []
SCAN_TIME = 12/60 # let's say it takes 12 seconds to scan each 'item'
PACK_TIME = 1/60 # let's say it takes 1 second to pack each 'item'

env = simpy.Environment()

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


class Aldi(object):
    def __init__(self, env, G, path_chosen, num_cashiers, num_items):
        
        self.env = env
        self.G = G.copy()
        self.path = simpy.Resource(env, path_chosen) # the path taken defines what's in the shopper's 'basket'
        self.buy = simpy.Resource(env, num_cashiers) # buying time is determined by the number of cashiers avaailable
        self.pack = simpy.Resource(env, num_items) 
        
        
        
    def take_path(self, shopper): # the path that the shopper chooses from the network
        yield self.env.timeout(path_chosen) # tells simpy to trigger this event after a certain time has passed, time could be weighting of the path?
        
    def purchase_items(self, shopper): # the process of buying items at the till
        yield self.env.timeout(num_cashiers) 
        
    def pack_items(self, shopper): # the process of packing items away
        yield self.env.timeout(PACK_TIME * num_items)
        
      
    def go_to_shop(env, shopper, Aldi): # shopper arrives at ALdi
    
    arrival_time = env.now  # makes note of the time
    
    with Aldi.path.request() as request:              # generates a 'request' for a path
        yield request                                 # waits for the path to become available if max customers are on the path
        yield env.process(Aldi.take_path(shopper))    # uses the path once it becomes available
        
    with Aldi.buy.request() as request:
        yield request
        yield env.process(Aldi.purchase_items(shopper))
        
    with Aldi.pack.request() as request:
        yield request
        yield env.process(Aldi.pack_items(shopper))
        
        
    # shopper leaves Aldi
    time_in_shop.append(env.now - arrival_time)
    

    
def shopper(env, infected: bool, Aldi, path_chosen)


# the main process - making the simulation happen
def run_Aldi(env, path_chosen, num_cashiers, num_items):
    aldi = Aldi(env, path_chosen, num_cashiers, num_items)
    
    for shopper in range (3):   # up to three people could be waiting outside before the shop opens
        env.process(go_to_shop(env, shopper, aldi))   # moves the shoppers through Aldi
        
    while True: 
        yield env.timeout(0.5)   # a new shopper is generated every 30 seconds
        
        shopper += 1
        env.process(go_to_shop(env, shopper, aldi))

        
def inputs:        
    path_chosen = rand_path(paths)
    num_cashiers = input("Input no. cashiers on shift: ")
    num_items = # weighting of that path
    

        
        
        


# In[ ]:




