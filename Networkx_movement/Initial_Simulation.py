
import argparse
import numpy as np
#import random as rd
from numpy.random import random, randint
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Import path generation from other file
import Networkx_random_path_example as path_gen
# Import aldi layout for other file
import Networkx_aldi_layout as lay
import Infection_rate_data as inf_rate


def main(*args):
#changing the argument input to allow the command line to ask the user to input
    #max_entry , duration , max_shoppers = get_user_input()
    #using argpas to handing parsing command line arguments
    parser = argparse.ArgumentParser(description='Animate an epidemic')
    parser.add_argument('--max_entry', metavar='N', type=int, default=2,
                        help='Maximum of N people can enter at once')
    parser.add_argument('--duration', metavar='N', type=int, default=100,
                        help='Run simulation for N time steps')
    parser.add_argument('--max_shoppers', metavar='N', type=int, default=12,
                    help='Maximum number of shoppers in the shop')
    parser.add_argument('--month', metavar='N', type=int, default=1020,
                    help='The month to use to represent the infection rate')
    parser.add_argument('--path_system', metavar='N', type=int, default=2,
                    help='The type of path system that is used in the shop where 1 is any path and 2 is a one way system')
    args = parser.parse_args(args)

    #setting up simulation
    sim = simulation(args.max_entry, args.duration, args.max_shoppers, args.month, args.path_system)
    #starts out with 1 shopper 
    sim.add_new_shopper()
    results(sim, args.duration)
    animation = Animation(sim, args.duration)
    animation.show()

#----------------------------------------------------------------------------#
#                  Simulation class                                          #
#----------------------------------------------------------------------------#

class simulation:

    #vector that will contain SIR status of each person who leaves the shop
    left_shop = []
    #vector what contains instance of each person currently in the shop
    shoppers = []

    #vector to count number of people who are in shop
    shopping_count = []

    # probability of infection at each node in the shop
    # level 0 is probability of infection for people wearing a mask
    # level 1 is probability of infection for people without a mask
    shop_infection_risk = np.zeros((2,8,7))

    #vector to contain length of shopping time per person
    shopping_time = []

    def __init__(self, entry, duration, max_shoppers,month,path_system):
        # Basic simulation perameters:
        self.max_entry = entry  #max number of people who can enter at once
        self.duration = duration
        self.time_step = 0
        self.max_shoppers = max_shoppers
        self.month = month
        self.path_system = path_system



    def update(self): 
        """advances the simulation by 1 time step"""
        # for all people in the shop, move them, then calculate their new SIR level
        [person.move_path() for person in simulation.shoppers]

        #update the infection risk matrix now that people have moved
        self.update_infection_risk()

        #assign new SIR level to every shopper based on everyone new position
        [person.new_SIR_level() for person in simulation.shoppers if person.SIR_level < 2]
        

        # finding the number of people who can enter the shop in this time step
        if len(simulation.shoppers) < self.max_shoppers - self.max_entry:
            # randomly picking number of new people to enter the shop
            number_of_shoppers_entering = randint(0, self.max_entry)


        elif len(simulation.shoppers) < self.max_shoppers:
            # max number of people that can enter
            max_entry_to_meet_capacity = self.max_shoppers - len(simulation.shoppers)
            # randomly picking number of new people to enter shop that wont go over maximum capacity
            number_of_shoppers_entering = randint(0, max_entry_to_meet_capacity)
        # adding the new people to the shop
        for j in range(number_of_shoppers_entering):
            self.add_new_shopper()
        
        #add one to the time step counter and record the time step total
        self.time_step += 1


    def update_infection_risk(self):
        """updates matrix for risk of infection at each node in the shop"""
        #number of infected people ate ach shop node w/ mask
        i_w_mask = person.cords[2] # and again for 3 but without compensating for masks
        #number of infected people ate ach shop node w/o mask
        i_no_mask = person.cords[3]

        prob_of_i = 0.2 #chance of a person w/o mask catching covid from infected person w/o mask
        reduced_i_prob_w_mask = prob_of_i / 2 #chance of a person w/o mask catching covid from infected person w/ mask

        prob_of_i_from_i_w_mask = reduced_i_prob_w_mask * i_w_mask
        prob_of_i_from_i_no_mask = prob_of_i * i_no_mask

        risk_no_mask = prob_of_i_from_i_w_mask + prob_of_i_from_i_no_mask
        risk_in_mask = risk_no_mask / 2
        # capturing the state of the shop nodes for animation
        sus_no_mask = person.cords[0]
        sus_mask = person.cords[1]
        inf_mas = person.cords[2]
        inf_no_mask = person.cords[3]
        simulation.susceptible = sus_no_mask + sus_mask
        simulation.infected = -10*inf_mas + -10*inf_no_mask
        shopping_count = len(simulation.shoppers)

        # create 2 layer array of risk
        simulation.shop_infection_risk = np.stack((risk_in_mask, risk_no_mask))

    def add_new_shopper(self):
        """adds new person the the shop"""
        #creates a new instance of a person thats either
        #suseptible or infected, based on the "level of covid
        #in the area" and adds them to the list of shoppers 
        chance_person_wears_mask = 0.5
        level_of_covid_in_area = inf_rate.infection_rate(self.month)

        if self.path_system == 2: # when user has specified 1 way simulation
            speed = 2 # assign one way paths
        else:  # when all paths available
            speed = randint(0,2) # assign speed to people randomly


        #add infected person
        if level_of_covid_in_area > random():
            if chance_person_wears_mask > random():
                #add infected person with mask
                mask =  1
                simulation.shoppers.append(person((0,0),2,speed, mask))
            else:
                # add infected person without mask
                mask = 0
                simulation.shoppers.append(person((0,0),3,speed, mask))


        #add suseptible person
        else:
            if chance_person_wears_mask > random():
                # add suseptible person w/ mask
                mask = 1
                simulation.shoppers.append(person((0,0),0,speed, mask))
            else:
                # add suseptible person w/o mask
                mask = 0
                simulation.shoppers.append(person((0,0),1,speed, mask))

#----------------------------------------------------------------------------#
#                  Person class                                              #
#----------------------------------------------------------------------------#

class person:
    # Array representing network for aldi layout
    # it has 5 "levels" to it, each one is 8x7 where each element represents a shop node from the network x shop diagram
    # in level 0: each element records the number of people at that node who are suseptible wearing a mask
    # in level 1: each element records the number of people at that node who are suseptible and not wearing a mask
    # in level 2: each element records the number of people at that node who are infected & wearing a mask
    # in level 3: each element records the number of people at that node infected and not wearing a mask
    # in level 4: each element records the number of people at that node who have caught covid whilst shopping (removed)

    cords = np.zeros((5,8,7))

    # all possible paths that could be taken by a person through the shop
    paths = path_gen.possible_paths(lay.aldi_layout(), (0,0),[(6,6), (7,6)])
    slow_paths = path_gen.slow_paths(lay.aldi_layout(), (0,0),[(6,6), (7,6)])
    fast_paths = path_gen.fast_paths(lay.aldi_layout(), (0,0),[(6,6), (7,6)])
    one_way_paths = path_gen.possible_paths_oneway(lay.aldi_layout(), (0,0),[(6,6), (7,6)])

    # Setting initial varibles for each person
    # Add all variables for each person here
    def __init__(self, pos, covid_status,speed, mask):
        self.pos = pos            # Position in network
        self.n = 0                # current step in path (0 is the entrance of the shop)
        self.SIR_level = covid_status     #their SIR level (0=suseptible (w/m) 1= s (w/o m) 2= Infected (w/ mask) 3= infected (w/o mask) 4= removed)
        self.speed = speed
        self.mask = mask # 1 = wearing mask, 0 = no mask



        if speed == 0: # if random assignment of speed is zero then person with long path
            rand_int = randint(0, len(person.slow_paths))
            self.path = person.paths[rand_int]
        elif speed == 1: # if random assignment of speed is 1 then person has a quick path
            rand_int = randint(0, len(person.fast_paths))
            self.path = person.fast_paths[rand_int]
        elif speed == 2: # if path system is one way
            rand_int = randint(0 , len(person.one_way_paths))
            self.path = person.one_way_paths[rand_int]

        self.shop_time = len(self.path)
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



    def move_path(self):
        #if someones at the end o their path then ...
        if self.n == (len(self.status)-1):
            #remove them from current position in cords array
            person.cords[(self.pos)] -= 1

            #takes info from them
            leaving_info = self.SIR_level
            shopping_time = self.shop_time
            simulation.shopping_time.append(shopping_time)
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
        # get the persons probability of infection based on the infection risk matrix
        probability_of_infection = simulation.shop_infection_risk[self.pos]

        if probability_of_infection > random():
            #change their SIR level to 4 (removed)
            self.SIR_level = 4
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
        rgb_matrix = person.cords[0]
        # uncomment this^^^ too see how people move through the shop in the cords array
        simulation.update()

    #count the number of people who've left the shop
    num_left_shop = len(simulation.left_shop)   
    print("Number of people who've left the shop:", num_left_shop)

    # from those who've left the shop, count the number of them who entred with covid
    num_initially_infected = simulation.left_shop.count(2) + simulation.left_shop.count(3)
    percentage_initially_infected = (num_initially_infected / num_left_shop)*100
    # ^^ this will mess up if no ones left the shop
    # need to set minimum for duration argument or find work around

    # number of people who left suseptible (didn't catch covid)
    num_not_infected = simulation.left_shop.count(0) + simulation.left_shop.count(1)
    # number of people who left that caught covid while shopping
    num_caught_covid = simulation.left_shop.count(4)
    # number of people who've left that were initially suseptible
    num_initially_suseptible = num_not_infected + num_caught_covid
    # calculate % of people who entered the shop suseptile who left with covid
    percentage_who_caught_covid = (num_caught_covid / num_initially_suseptible)*100
    #function to calculate average of a list
    def Average(lst):
        return mean(lst)
    # calculated the avergage time in the shop
    average_shop_time = Average(simulation.shopping_time)

    print("Out of those,", percentage_initially_infected, "% entered the shop infected")
    print("Out of those initially suseptible", percentage_who_caught_covid, "% caught covid")
    print("Average time in shop", average_shop_time, "minutes in the shop")






#function for getting user input
def get_user_input():
    entry = input("Maximum number of people who can enter the shop at once: ")
    duration = input("Number of time steps to run the simulation for: ")
    max_shoppers = input("Maximum number of people allowed in the shop at once: ")
    #prob_infection = input("Probability of catching covid when within 2m of someone infected: ")
    params = [entry, duration, max_shoppers]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:",
            "\n10 people max entry at one time, 70 people max in the shop at one time, and the simulation will run for 200 time steps.",
            #"\n10 people max entry at one time, 50 people max in the shop at one time, and the simulation will run for 120 time steps.",
        )
        params = [10, 120, 50]
    return params

class Animation:
    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration
        self.figure = plt.figure(figsize=(8, 4))
        self.axes_grid = self.figure.add_subplot(1, 2, 1)
        self.axes_line = self.figure.add_subplot(1, 2, 2)


        self.gridanimation = GridAnimation(self.axes_grid, self.simulation)
        #self.lineanimation = LineAnimation(self.axes_line, self.simulation, self.duration)

    def show(self):
        """Run the animation on screen"""
        animation = FuncAnimation(self.figure, self.update, frames=range(100),
                init_func = self.init, blit=True, interval=100, repeat=False)
        plt.show()

    def init(self):
        """Initialise the animation (called by FuncAnimation)"""
        # numer of *animation objects.
        actors = []
        actors += self.gridanimation.init()
        #actors += self.lineanimation.init()
        return actors

    def update(self, framenumber):
        """Update the animation (called by FuncAnimation)"""
        self.simulation.update()
        actors = []
        actors += self.gridanimation.update(framenumber)
        #actors += self.lineanimation.update(framenumber)
        return actors


class GridAnimation:
    """Animate a grid showing status of people at each position"""

    def __init__(self, axes, simulation):
        self.axes = axes
        self.simulation = simulation
        susceptible = self.simulation.susceptible
        infected = self.simulation.infected
        shop = infected+susceptible
        self.image = self.axes.imshow(shop, cmap='coolwarm')
        self.axes.set_xticks([])
        self.axes.set_yticks([])


    def init(self):
        return self.update(0)

    def update(self, framenum):
            minute = framenum
            susceptible = self.simulation.susceptible
            infected = self.simulation.infected
            shop = infected+susceptible
            self.image.set_array(shop)
            return [self.image]


class LineAnimation:
    """Animate a line series showing numbers of people in each status"""

    def __init__(self, axes, simulation, duration):
        self.axes = axes
        self.simulation = simulation
        self.duration = duration
        self.shopping_no = []
        self.time = []
        self.line = 0
        self.axes.plot(self.simulation.time_step, linewidth=2)


    def init(self):
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, 20])
        return []

    def update(self,framenum):
        #framenum = self.simulation.time_step
        #self.shopping_no.append(self.simulation.shopping_time)
        #self.time.append(self.simulation.time_step)
        #self.line = self.line.set_data(self.shopping_no,self.time)
        self.axes.plot(self.simulation.time_step)
        return self.axes



if __name__ == "__main__":

    import sys
    main(*sys.argv[1:])



