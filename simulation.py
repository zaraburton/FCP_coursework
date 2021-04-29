#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import simpy
import random
import statistics
import networkx as nx
import Networkx



# create an environment object to manage the simulation time and move the simulation through time steps
env = simpy.Environment()

# next we need to pass in the variables that will act as paramaters.
# parameters are the things we vary to see how the systems changes (people in the space)
# env: the environment object to schedule the process of events
# shoppers : the list of shoppers in the shop and where they are in space
# shopper_arrival : rate at which shoppers arrive



class Aldi(object):
    def __init__(self, env, G, path_chosen, num_cashiers, num_items):
        self.env = env
        self.G = G.copy()
        self.path = simpy.Resource(env, path_chosen)  # the path taken defines what's in the shopper's 'basket'
        self.pack = simpy.Resource(env, num_items)  # time taken to pack is based on the number of items a customer has.
        self.customers_at_nodes = {node: [] for node in
                                   self.G}  # creates a dictionary with an empty list of nodes in the graph

    def take_path(self, shopper):  # the path that the shopper chooses from the network
        yield self.env.timeout(
            path_chosen)  # tells simpy to trigger this event after a certain time has passed, time could be weighting of the path?

    def purchase_items(self, shopper):  # the process of buying items at the till
        yield self.env.timeout(SCAN_TIME * num_items)

    def pack_items(self, shopper):  # the process of packing items away
        yield self.env.timeout(PACK_TIME * num_items)

    def go_to_shop(env, shopper, Aldi):  # shopper arrives at ALdi

    arrival_time = env.now  # makes note of the time

    with Aldi.path.request() as request:  # generates a 'request' for a path
        yield request  # waits for the path to become available if max customers are on the path
        yield env.process(Aldi.take_path(shopper))  # uses the path once it becomes available

    with Aldi.buy.request() as request:
        yield request
        yield env.process(Aldi.purchase_items(shopper))

    with Aldi.pack.request() as request:
        yield request
        yield env.process(Aldi.pack_items(shopper))

    # shopper leaves Aldi
    # adding list to contain the total amount of time each shopper is in the shop
    time_in_shop = []
    time_in_shop.append(env.now - arrival_time)


def shopper(env, infected: bool, Aldi,
            path_chosen)  # shopper defined based on whether or not they are infected and the path they chose


def move_shopper(env, Aldi, path_chosen, start, end)
    start = path_chosen[0]
    end = path_chosen[end]
    while pos < len(path_chosen)
        pos = node in path_chosen
        node = + 1


# the main process - making the simulation happen
def run_Aldi(env, path_chosen, num_cashiers, num_items):
    aldi = Aldi(env, path_chosen, num_cashiers, num_items)

    for shopper in range(3):  # up to three people could be waiting outside before the shop opens
        env.process(go_to_shop(env, shopper, aldi))  # moves the shoppers through Aldi

    while True:
        yield env.timeout(0.5)  # a new shopper is generated every 30 seconds

        shopper += 1
        env.process(go_to_shop(env, shopper, aldi))


def inputs:
    path_chosen = rand_path(paths)
    num_cashiers = input("Input no. cashiers on shift: ")
    num_items =  # weighting of that path




