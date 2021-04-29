#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import simpy
import random
import statistics
#import networkx as nx
#import Networkx
#import numpy as np


# create an environment object to manage the simulation time and move the simulation through time steps
shop_times=[]
arrival_times = []
departure_times = []
#1env = simpy.Environment()

# next we need to pass in the variables that will act as paramaters.
# parameters are the things we vary to see how the systems changes (people in the space)
# env: the environment object to schedule the process of events
# shoppers : the list of shoppers in the shop and where they are in space
# shopper_arrival : rate at which shoppers arrive
class Aldi(object):
    def __init__(self, env, num_tills, num_section,num_baristas):
        self.env = env
        #self.G = np.zeros((8,7))
        #self.customers_at_nodes = {node: [] for node in self.G}  # creates a dictionary with an empty list of nodes in the graph
        self.till = simpy.Resource(env, num_tills)
        self.section = simpy.Resource(env, num_section)
        self.barista = simpy.Resource(env, num_baristas)

    def purchase_items(self, shopper):  # the process of buying items at the till mimiced to time out
        yield self.env.timeout(random.randint(1,3))

# people waiting at a node in the store deciding if they want an item representing this time as really small
# past as 3/60 as simpy works in minutes so specify 3 seconds
    def wait_node(self, shopper):
        yield self.env.timeout(10 / 60)

# queue times for coffee between 1 and 8 mins randomly
    def stop_coffee(self,shopper):
        yield self.env.timeout(random.randint(1,8))

# shopper controlled by env so this is first arg
# shopper arg tracks each shopper as they are in the system
#aldi gives access to the processes defined in class def
# arrival time stores the time at which each shopper arrives in the shop
#need each shop process to hbe requested in the go_to_shop function

def go_to_shop(env,shopper,aldi):
    #shopper arrives at aldi
    arrival_time = env.now
    arrival_times.append(arrival_time)

    with aldi.till.request() as request: # requests use of a till
        yield request # shopper waits for available till
        yield env.process(aldi.purchase_items(shopper)) # shopper uses an available till to purchase items

    with aldi.section.request() as request: # requests viwing a section
        yield request # shopper waits for available section
        yield env.process(aldi.wait_node(shopper)) # shopper uses an available section to look at items

    if random.choice([True,False]):
        with aldi.barista.request() as request: # requests viwing a section
            yield request # shopper waits for available section
            yield env.process(aldi.stop_coffee(shopper)) # shopper uses an available section to look at items

    #shopper leaves shop
    departure_time = env.now
    departure_times.append(departure_time)
    shop_times.append(env.now - arrival_time)

def run_aldi(env,num_tills, num_section, num_baristas):
    aldi = Aldi(env, num_tills,num_section,num_baristas)

    #start with 5 shoppers in shop
    for shopper in range(5):
        env.process(go_to_shop(env,shopper, aldi))

    while True:
        yield env.timeout(0.1) # wait before generating new shopper, every 1 minute

    shopper += 1
    env.process(go_to_shop(env,shopper,aldi))

#def get_average_shop_times(shop_times): # function to calculate average shop time
#    average_shop = statistics.mean(shop_times)

#allow nicer output of time in shop in minutes and seconds
def calculate_shop_time(arrival_times,departure_times):
    average_shop = statistics.mean(shop_times)
    #pretty print the results
    minutes, frac_minutes = divmod(average_shop,1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def get_user_input():
    num_tills = input("Input # of tills: ")
    num_section = input("Input # of sections in the shop: ")
    num_baristas = input("Input # of baristas serving coffee: ")
    params = [num_tills, num_section, num_baristas]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:",
            "\n1 tills, 9 sections, 1 barista.",
        )
        params = [1, 9, 1]
    return params

#main function
def main():
  # Setup
  random.seed(42) # set up env by declaring random seed
  num_tills, num_section, num_baristas = get_user_input() # get user inputs

  # Run the simulation
  env = simpy.Environment() # create environments
  env.process(run_aldi(env, num_tills, num_section, num_baristas)) # run the shop function
  env.run(until=120) # for 2 hours

  # View the results
  mins, secs = calculate_shop_time(arrival_times,departure_times)
  print(
      "Running simulation...",
      f"\nThe average shop time is {mins} minutes and {secs} seconds.",
  )

if __name__ == '__main__':
      main()