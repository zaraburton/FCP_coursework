
import argparse
import numpy as np
#import random as rd
from numpy.random import random, randint

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Import path generation from other file
import Networkx_random_path_example as path_gen
# Import aldi layout for other file
import Networkx_aldi_layout as lay


def main(args):
#changing the argument input to allow the command line to ask the user to input
    max_entry , duration = get_user_input()
    #using argpas to handing parsing command line arguments
    #parser = argparse.ArgumentParser(description='Animate an epidemic')
    #parser.add_argument('--max_entry', metavar='N', type=int, default=4,
    #                    help='Maximum of N people can enter at once')
    #parser.add_argument('--duration', metavar='N', type=int, default=100,
    #                    help='Run simulation for N time steps')
    #args = parser.parse_args(args)

    #setting up simulation
    sim = simulation(max_entry, duration)
    #starts out with 1 shopper 
    sim.add_new_shopper()

    results(sim, duration)


#----------------------------------------------------------------------------#
#                  Simulation class                                          #
#----------------------------------------------------------------------------#

class simulation:

    #vector that will contain SIR status of each person who leaves the shop
    left_shop = []
    #vector what contains instance of each person currently in the shop
    shoppers = []
    
    def __init__(self, entry, duration):
        # Basic simulation perameters:
        self.max_entry = entry  #max number of people who can enter at once
        self.duration = duration
        self.time_step = 0


    def update(self): 
        """advances the simulation by 1 time step"""
        # for all people in the shop, update them 
        #(uses the update_shopper function in person class)
        for i in simulation.shoppers:
            i.update_shopper()
        
        # randomly picking number of new people to enter the shop
        number_of_shoppers_entering = randint(0, self.max_entry)
        for j in range(number_of_shoppers_entering):
            self.add_new_shopper()
        
        #add one to the time step counter 
        self.time_step += 1
    
    def add_new_shopper(self):
        """adds new person the the shop"""
        #creates a new instance of a person thats either
        #suseptible or infected, based on the "level of covid
        #in the area" and adds them to the list of shoppers 
        level_of_covid_in_area = 0.3
        if level_of_covid_in_area > random():
            speed = randint(0, 1) # randomly assigning speed to the person appended
            simulation.shoppers.append(person((0,0),1,speed))
        else:
            speed = randint(0, 1) # randomly assigns speed to the person appended
            simulation.shoppers.append(person((0,0),0,speed))


#----------------------------------------------------------------------------#
#                  Person class                                              #
#----------------------------------------------------------------------------#

class person:
    # Array representing network for aldi layout
    # it has 3 "levels" to it, each one is 8x7 where each element represents a shop node from the network x shop diagram
    # in level 0: each element records the number of people at that node who are suseptible
    # in level 1: each element records the number of people at that node who are infected
    # in level 2: each element records the number of people at that node who have caught covid whilst shopping
    cords = np.zeros((3,8,7))

    # all possible paths that could be taken by a person through the shop
    paths = path_gen.possible_paths(lay.aldi_layout(), (0,0),[(6,6), (7,6)])
    slow_paths = path_gen.slow_paths(lay.aldi_layout(), (0,0),[(6,6), (7,6)])
    fast_paths = path_gen.fast_paths(lay.aldi_layout(), (0,0),[(6,6), (7,6)])

    # Setting initial varibles for each person
    # Add all variables for each person here
    def __init__(self, pos, covid_status,speed):
        self.pos = pos            # Position in network
        self.n = 0                # current step in path (0 is the entrance of the shop)
        self.SIR_level = covid_status     #their SIR level (0=suseptible 1=infected 2=removed)
        self.speed = speed

        if speed == 0: # if random assignment of speed is zero then person with long path
            rand_int = randint(0, len(person.slow_paths))
            self.path = person.paths[rand_int]
        elif speed == 1: # if random assignment of speed is 1 then person has a quick path
            rand_int = randint(0, len(person.fast_paths))
            self.path = person.fast_paths[rand_int]

            #status is their path and covid status in one thats used in the cords array
        #eg path of [(0,0), (0,1), (0,2)] for an infected person becomes
        # a status of [(1,0,0), (1,0,1), (1,0,2)]
        #the for loop takes each element in the paths list, turns it from a tuple to a list to edit it,
        #then back into a tuple, then adds it to the self.status list
        self.status = []
        for t in self.path:
            node = list(t)
            new_list = [self.SIR_level] + node
            x = tuple(new_list)
            self.status.append(x)
        
        #setting the persons position in the cords array 
        self.pos = self.status[0] 
        person.cords[(self.pos)] += 1

    
    def update_shopper(self):
        """moves a person, then calculates their SIR level"""
        #this is whats called by the simulation class
        self.move_path()
        self.new_SIR_level()


    def move_path(self):
        #if someones at the end o their path then ...
        if self.n == (len(self.status)-1):
            #remove them from current position in cords array
            person.cords[(self.pos)] -= 1

            #takes info from them
            leaving_info = self.SIR_level
            #and stores it in the left_shop array in the simulation class
            simulation.left_shop.append(leaving_info)
            #then remove them from the list of current shoppers 
            simulation.shoppers.remove(self)
        
        #move the person if they're not at the end of their path
        if self.n < (len(self.status)-1):
            #remove them from current position in cords array
            person.cords[(self.pos)] -= 1
            # picks next step in their path 
            self.n += 1
            # updates their position to the next step in their path
            self.pos = self.status[self.n]
            # Adds new node position into coordinate array
            person.cords[(self.pos)] += 1


    def new_SIR_level(self):
        """simulates people catching covid"""
        probability_of_infection = 0.2 # this should be set as an input argument later
        #calculate the number of infected people at the persons current position in the shop
        number_of_infected_at_node = person.cords[1, self.pos[1], self.pos[2]]
        #infect them if they are susceptible and there are infected people at their location
        #should probably think of a more accurate way to do this later
        if self.SIR_level == 0 and number_of_infected_at_node >= 1 and probability_of_infection > random():
            #change their SIR level from 0 to 2 
            self.SIR_level = 2 
            #now have to change their status for the cords array
            self.change_status()

    def change_status(self):
        """for every element in the status list, this changes the 1st element of the tuple from 0 to 2"""
        new_status = []
        for t in self.status:
            list_of_status = list(t)
            list_of_status[0] = self.SIR_level
            tuple_of_status = tuple(list_of_status)
            new_status.append(tuple_of_status)
        self.status = new_status
  


def results(simulation, duration):  
    #this will probably be turned into the animation class 


    #run the simulation for as many time steps as the duration 
    while simulation.time_step < duration: 
        # print(person.cords)
        # uncomment this^^^ too see how people move through the shop in the cords array
        simulation.update()

    #count the number of people who've left the shop
    num_left_shop = len(simulation.left_shop)   
    print("Number of people who've left the shop:", num_left_shop)


    # from those who've left the shop, count the number of them who entred with covid
    num_initially_infected = simulation.left_shop.count(1) 
    percentage_initially_infected = (num_initially_infected / num_left_shop)*100
    # ^^ this will mess up if no ones left the shop
    # need to set minimum for duration argument or find work around

    # number of people who left suseptible (didn't catch covid)
    num_not_infected = simulation.left_shop.count(0)
    # number of people who left that caught covid while shopping
    num_caught_covid = simulation.left_shop.count(2)
    # number of people who've left that were initially suseptible
    num_initially_suseptible = num_not_infected + num_caught_covid
    # calculate % of people who entered the shop suseptile who left with covid
    percentage_who_caught_covid = (num_caught_covid / num_initially_suseptible)*100

    print("Out of those,", percentage_initially_infected, "% entered the shop infected")
    print("Out of those initially suseptible", percentage_who_caught_covid, "% caught covid")

#function for getting user input
def get_user_input():
    entry = input("Maximum number of people who can enter the shop at once: ")
    duration = input("Number of time steps to run the simulation for: ")
    params = [entry, duration]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:",
            "\n10 people max entry at one time and the simulation will run for 120 time steps.",
        )
        params = [10, 120]
    return params



if __name__ == "__main__":

    import sys
    main(sys.argv[1:])


