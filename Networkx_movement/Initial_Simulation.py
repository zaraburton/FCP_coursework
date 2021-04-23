# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 16:08:08 2021

@author: wills
"""
import numpy as np
import random as rd

# Import path generation from other file
import Networkx_random_path_example as path_gen
# Import aldi layout for other file
import Networkx_aldi_layout as lay

# Defining shop layout as a networkx network with list of all possible paths
G = lay.aldi_layout()
paths = path_gen.possible_paths(G, (0,0),[(6,6),(7,6)])

# Array representing network for aldi layout
# Array also shows number of people in each node
cords = np.zeros((8,7))

# List of all people who leave shop
# Currently has 1 column with covid risk
# More columns can be added with other parameters
covid_exposure = np.zeros((2,2))

#setting initial defaul parametre for time
time = 20

# Have different function for different types of shoppers
# i.e. long shoppers have lower probability of skipping nodes
# short shoppers have higher probability of skipping nodes
# Skipping nodes is a way of randomising time spent shopping



class person:
    # Setting initial varibles for each person 
    # Add all variables for each person here
    def __init__(self, pos, name):
        self.pos = pos                                          # Position in network
        self.n = 1                                              # Next step in path which is to be moved to (step counter)
        self.covid_risk = 0                                     # Example blank variable for covid risk
        self.name = name                                        # Numbering people in class
        global paths
        self.path = path_gen.rand_path(paths)                   # Generates random path for each person
        cords[(self.pos)] += 1                                  # Sets position of person in coordinate array
    
    # Moves the person along the path
    def move_path(self):
        
        # Carry out movement if the node is less than the one before the exit
        if self.n < (len(self.path) - 1):
        
            # Random 50% chance of skipping node
            # If random number = 1, node doesn't skip
            # This is a way of randomly changing the duration of time in shop
            
            if rd.randint(1,2) == 1:
                
                # Removes old node position from coordinate array
                cords[(self.pos)] -= 1
                # Finds next node position from the path function
                self.pos = self.path[self.n]
                # Adds new node position into coordinate array
                cords[(self.pos)] += 1
                # Updates the step counter
                self.n += 1
            else:
                # If random number = 2, node skips
                # This can be thought of as the user walking past a shelf without picking up any items
                
                # Removes old node position from coordinate array
                cords[(self.pos)] -=1
                # Updates the step counter
                self.n += 1
                # Finds next node position from the path function
                self.pos = self.path[self.n]
                # Adds new node position into coordinate array
                cords[(self.pos)] += 1
                # Updates the step counter again (Effectivly skipping one node)
                self.n += 1
                
        # If statement actives when you reach the node before the exit
        # Basically we don't want to have any chance of skipping the exit node
        if self.n == len(self.path) - 1:
            cords[(self.pos)] -= 1
            self.pos = self.path[self.n-2]
            cords[(self.pos)] += 1
            self.n += 1
        
        # If statement actives when you reach the exit node    
        if self.n == len(self.path):
            cords[(self.pos)] -= 1
            self.pos = self.path[self.n-1]
            cords[(self.pos)] += 1
            self.n += 1
            # Way of moving person from active array to storage (could be live counter for how many people have been in shop)
            global covid_exposure
            covid_exposure = np.append(covid_exposure, [[self.name, self.covid_risk]], axis = 0)
            # During testing, this code worked when people were added inline but not from the console
            # This error needs to be debugged at a later time

# Inline way of creating people in the simulation
person_1 = person((0,0), 1)
#person_2 = person((0,0), 2)
#person_2.move_path()


# HS experimenting with for loop to call move path
######Doesnt work right now, trying to get the position to update with iterations of t (time)
person_1_path =  person_1.path
person_1_journey = []
person_1_position_list =[]
person_1_position = person_1.pos

# for loop to run for persons path and append their journey to a list of co-ords of their path through the shop
# need to make it a fuction

for i in person_1_path:
    while i != (7,6): # while the x axis co-ord is greater or equal to zero
        person_1.move_path()   # move the person
        person_1_journey.append(cords)     #person_1_position_list.append(person_1_position)
        person_1_position = person_1.pos # update person 1 position
        if person_1_position == (7, 6):
            break

print(person_1_journey)