
import argparse
import numpy as np
#import random as rd
from numpy.random import random, randint
from statistics import mean
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



# Import path generation from other file
import Networkx_random_path_example as path_gen
# Import aldi layout for other file
import Networkx_aldi_layout as lay
import Infection_rate_data as inf_rate


def main(args):
    #max_entry , duration , max_shoppers = get_user_input()
    #using argpas to handing parsing command line arguments
    parser = argparse.ArgumentParser(description='Animate an epidemic')
    parser.add_argument('--max_entry', metavar='N', type=int, default=5,
                        help='Maximum of N people can enter at once')
    parser.add_argument('--duration', metavar='N', type=int, default=200,
                        help='Run simulation for N time steps')
    parser.add_argument('--max_shoppers', metavar='N', type=int, default=30,
                    help='Maximum number of shoppers in the shop')
    parser.add_argument('--month', metavar='myy', type=int,
                    help='The month to use to represent the infection rate where 320 is March 2020 (from 320 - 421)')
    parser.add_argument('--path_system', metavar='N', type=int, default=1,
                    help='The type of path system 0 = slow walker 1 = quick walker 2 = one way path system, 3 = mixed scenario')
    parser.add_argument('--level_of_covid', metavar='P', type=float, default=0.4,
                    help='Probability of any individual in the area being infected')
    parser.add_argument('--plot', action='store_true',
                    help='Generate plots instead of animation')
    args = parser.parse_args(args)

    #TD: make parser args for next variables

    #TD: something to say you cant have level of covid and month given at same time? or just pick on or the other? (Will automatically go by the month if thats given)
    #set level_of_covid_in_area (prob of infected person entering the shop) as infection rate for that month
    if args.month:
        level_of_covid_in_area = inf_rate.infection_rate(args.month)
    else:
        level_of_covid_in_area = args.level_of_covid
        #running the simulation based off of argument inputs instead
    prob_of_i = 0.2
    chance_person_wears_mask = 0.4
    sim = simulation(args.max_entry, args.duration, args.max_shoppers, args.path_system, prob_of_i,chance_person_wears_mask, level_of_covid_in_area)
    sim.add_new_shopper(1)
    results(sim, args.duration)

    #plotting the graphs or animation based off of user input showing simulation results
    if args.plot:
        plot_results(sim, args.duration)
        plt.show()
    else:
    # calling the animation class to plot the animation if the user hasnt specified they want the plots
        animation = Animation(sim, args.duration)
        animation.show()




#----------------------------------------------------------------------------#
#                  Simulation class                                          #
#----------------------------------------------------------------------------#

class simulation:

    """Simulation of the spread of covid within a matrix, representing a supermarket.

    The supermarket is represented as an 8 x 7 grid. Once a person enters the shop, there position on the grid
    is denoted by a 1 at that location. There are two layers to this grid: shoppers wearing a mask, and shoppers without a mask.

    The state of one layer of the grid (shoppers wearing masks for example) might look like this:

    0 0 0 0 0 0 1 1
    0 1 0 0 1 0 2 0
    0 2 0 0 1 0 1 0
    0 0 0 0 0 0 1 1
    0 1 0 0 1 0 2 0
    0 2 0 0 1 0 1 0
    1 0 0 0 0 0 0 0

    There is one entrance at the bottom left and two exits at the top right of the grid. The number in each 
    position denotes the number of people in each location within the shop.

    The update() method advances the simulation by one timestep (minute), moving a person along their 'path' on the grid.
    
    The update_infection_risk() method assigns a risk to each shop node based on whether there is a person present at
    that node, and based on whether they are in the layer storing people with masks, or in the layer storing people
    without masks. The risk of infection is set and halved for people wearing a mask.
    The method then adds these layers to the person array which stores all five possible states:
    susceptible (with and without a mask), infected (with and without a mask) and removed (caught covid).
    
    The add_new_shopper() method introduces a new shopper into the store simulation.

    

    Example
    =======

    Create a simulation with the following parameters:
    - Up to two people can enter the shop at any one time
    - The simulation lasts for 100 minutes
    - Up to 12 shoppers can be in the shop at once
    - The simulation is run in November
    - No path system is in place

    >>> sim = Simulation(3, 100, 12, 1120, 0) # not quite sure how to input the months??
    >>> sim.add_new_shopper()  # adds a new shopper
    >>> results(sim, args.duration)
    {Number of people who've left the shop:32, Out of those, 93.75% entered infected, 
    Out of those initially suseptible 0.0% caught covid, Average time in shop 23.375
    minutes.}

    """


    #vector that will contain SIR status of each person who leaves the shop
    left_shop = []
    #vector what contains instance of each person currently in the shop
    shoppers = []
    #array storing each time step
    time_step_counter = []
    #array storing number of people in shop at each time step
    people_at_time_step = []
    #vector to count number of people who are in shop
    shopping_count = []
    #vector to record time steps
    time = []

    #vectors to record total number of people at t with each SIR level
    sus_w_mask_t = []
    sus_wo_mask_t = []
    inf_w_mask_t = []
    inf_wo_mask_t = []
    caught_cov = []

    # Status codes to store in the numpy array representing the state.
    SUSCEPTABLE_W_MASK = 0
    SUSCEPTABLE_WO_MASK = 1
    INFECTED_W_MASK = 2
    INFECTED_WO_MASK = 3
    CAUGHT_COV_IN_SHOP = 4

    STATUSES = {
        'Susceptable with a mask': SUSCEPTABLE_W_MASK,
        'Susceptable without a mask': SUSCEPTABLE_WO_MASK,
        'Infected with a mask': INFECTED_W_MASK,
        'Infected without a mask': INFECTED_WO_MASK,
        'Caught COVID in shop': CAUGHT_COV_IN_SHOP,
    }

    COLOURMAP = {
        'Susceptable with a mask': 'yellow',
        'Susceptable without a mask': 'green',
        'Infected with a mask': 'red',
        'Infected without a mask': 'magenta',
        'Caught COVID in shop': 'cyan',
    }
    COLOURMAP_RGB = {
        'yellow': (255, 255, 0),
        'green': (0, 255, 0),
       'red': (255, 0, 0),
       'magenta': (255, 0, 255),
        'cyan': (0, 255, 255),
     }
    # colour map for sus vs inf plots
    INF_COLOURMAP_RGB = {
        'yellow': (255, 255, 0),
        'red': (255, 0, 0),
        'cyan': (0, 255, 255),
    }


    # probability of infection at each node in the shop
    # level 0 is probability of infection for people wearing a mask
    # level 1 is probability of infection for people without a mask
    shop_infection_risk = np.zeros((2,8,7))

    #vector to contain length of shopping time per person
    shopping_time = []

    def __init__(self, entry, duration, max_shoppers, path_system, prob_of_i,chance_person_wears_mask, level_of_covid_in_area):
        # Basic simulation perameters:
        self.max_entry = entry  #max number of people who can enter at once
        self.duration = duration
        self.time_step = 0
        self.max_shoppers = max_shoppers
        self.path_system = path_system
        self.time_array = np.arange(self.duration)
        self.prob_of_i = prob_of_i
        self.chance_person_wears_mask = chance_person_wears_mask
        self.level_of_covid_in_area = level_of_covid_in_area


    def update(self): 
        """advances the simulation by 1 time step"""
        # for all people in the shop, move them, then calculate their new SIR level
        [person.move_path() for person in simulation.shoppers]

        #update the infection risk matrix now that people have moved
        self.update_infection_risk()

        #assign new SIR level to every shopper based on everyone new position
        [person.new_SIR_level() for person in simulation.shoppers if person.SIR_level < 2]
        
        #assign number of shoppers to enter at this timestep
        number_of_new_shoppers = self.get_number_of_shoppers_entering()

        # adding the new people to the shop
        self.add_new_shopper(number_of_new_shoppers)

        simulation.people_at_time_step.append(len(self.shoppers))


        #simulation.sus_wo_mask_t.append(np.sum(self.person.cords[0]))
        #simulation.sus_w_mask_t.append(np.sum(self.person.cords[1]))
        #simulation.inf_w_mask_t.append(np.sum(self.person.cords[2]))
        #simulation.inf_wo_mask_t.append(np.sum(self.person.cords[3]))
        #simulation.caught_cov.append(np.sum(self.person.cords[4]))
        self.get_shop_numbers()

        simulation.infected = (person.cords[2] + person.cords[3] + person.cords[4] + person.cords[5])
        #add one to the time step counter

        self.time_step += 1


    def update_infection_risk(self):

        """updates matrix for risk of infection at each node in the shop"""
        #number of infected people at each shop node w/ mask
        i_w_mask = person.cords[2] 
        #number of infected people ate ach shop node w/o mask
        i_no_mask = person.cords[3]

     #   prob_of_i = 0.2 #chance of a person w/o mask catching covid from infected person w/o mask
        reduced_i_prob_w_mask = self.prob_of_i / 4 #chance of a person w/o mask catching covid from infected person w/ mask

        prob_of_i_from_i_w_mask = reduced_i_prob_w_mask * i_w_mask
        prob_of_i_from_i_no_mask = self.prob_of_i * i_no_mask

        risk_no_mask = prob_of_i_from_i_w_mask + prob_of_i_from_i_no_mask
        risk_no_mask = np.clip(risk_no_mask,0, 0.95)

        risk_in_mask = risk_no_mask / 4
        risk_in_mask = np.clip(risk_in_mask,0, 0.95)


        # create 2 layer array of risk
        simulation.shop_infection_risk = np.stack((risk_in_mask, risk_no_mask))




    def get_number_of_shoppers_entering(self):
        """finding the number of people who can enter the shop in this time step"""
        if len(simulation.shoppers) < self.max_shoppers - self.max_entry:
            # randomly picking number of new people to enter the shop
            number_of_shoppers_entering = randint(0, self.max_entry +1)


        elif len(simulation.shoppers) < self.max_shoppers:
            # max number of people that can enter
            max_entry_to_meet_capacity = self.max_shoppers - len(simulation.shoppers)
            # randomly picking number of new people to enter shop that wont go over maximum capacity
            number_of_shoppers_entering = randint(0, max_entry_to_meet_capacity +1)

        else:
            number_of_shoppers_entering = 0

        return number_of_shoppers_entering



    def add_new_shopper(self, number_of_shoppers_entering):
        """adds new person the the shop"""
        #creates a new instance of a person thats either
        #suseptible or infected, based on the "level of covid
        #in the area" and adds them to the list of shoppers

        shoppers_to_add = np.arange(number_of_shoppers_entering)

        if self.path_system == 2: # when user has specified 1 way simulation
            speed = 2 # assign one way paths
        elif self.path_system == 1 :  # when all shoppers move quickly
            speed = 1 # assign speed being quick
        elif self.path_system == 0: # when all shoppers move slowly
            speed = 0
        elif self.path_system == 3: # when user has not specified a speed of shopper
            speed = randint(0,1)  # assign shoppers slow and quick paths randomly


        for shopper in shoppers_to_add:    
            #add infected person
            if self.level_of_covid_in_area > random():
                if self.chance_person_wears_mask > random():
                    #add infected person with mask
                    mask =  1
                    simulation.shoppers.append(person((0,0),2,speed, mask))
                else:
                    # add infected person without mask
                    mask = 0
                    simulation.shoppers.append(person((0,0),3,speed, mask))

            #add suseptible person
            else:
                if self.chance_person_wears_mask > random():
                    # add suseptible person w/ mask
                    mask = 1
                    simulation.shoppers.append(person((0,0),0,speed, mask))
                else:
                    # add suseptible person w/o mask
                    mask = 0
                    simulation.shoppers.append(person((0,0),1,speed, mask))

    def get_node_status(self):


        simgrid = person.cords[0] + person.cords[1] + person.cords[2] + person.cords[3] + person.cords[4] + person.cords[5] # total people in shop
        state = person.cords
        total_people = np.sum(simgrid)

        percentages = {}
        for status, statusnum in self.STATUSES.items():
            count = np.sum(simgrid[statusnum]) # taking each state of person from the stacked array
            percentages[status] = count
        return percentages

    def get_shop_numbers(self):
        if self.time_step < self.duration:
            sus_no_mask = person.cords[0]
            simulation.sus_no_mask = sus_no_mask
            sus_mask = person.cords[1]
            simulation.sus_mask = sus_mask
            inf_mas = person.cords[2]
            simulation.inf_mas = inf_mas
            inf_no_mask = person.cords[3]
            simulation.inf_no_mask = inf_no_mask
            caught_covid = person.cords[4] + person.cords[5]
            simulation.caught_covid = caught_covid

            simulation.susceptible = (sus_no_mask + sus_mask)  # counting susceptible people for animation
            simulation.infected = (inf_mas + inf_no_mask + caught_covid)  # counting infected people for animation
            no_sus_at_t = np.sum(sus_mask) + np.sum(sus_no_mask)
            no_inf_at_t = np.sum(inf_mas) + np.sum(inf_no_mask)
            shoppers_total = np.sum(person.cords)
            simulation.shopping_count.append(shoppers_total)

            # calculation the susceptible people and storing in array

            sus_no_maskt = np.sum(sus_no_mask)
            simulation.sus_wo_mask_t.append(sus_no_maskt)

            sus_w_maskt = np.sum(sus_mask)
            simulation.sus_w_mask_t.append(sus_w_maskt)

            inf_no_maskt = np.sum(inf_no_mask)
            simulation.inf_wo_mask_t.append(inf_no_maskt)

            inf_w_maskt = np.sum(inf_mas)
            simulation.inf_w_mask_t.append(inf_w_maskt)

            caught = np.sum(caught_covid)
            simulation.caught_cov.append(caught)

#----------------------------------------------------------------------------#
#                  Person class                                              #
#----------------------------------------------------------------------------#

class person:

    """ Class representing the shoppers within the supermarket.
        
        The cords array has 5 layers, each of size 8 x 7, which contain the number of people at each position within the shop.
        Each layer represents a Covid status:
        in level 0: each element records the number of people at that node who are suseptible wearing a mask
        in level 1: each element records the number of people at that node who are suseptible and not wearing a mask
        in level 2: each element records the number of people at that node who are infected & wearing a mask
        in level 3: each element records the number of people at that node infected and not wearing a mask
        in level 4: each element records the number of people at that node who have caught covid whilst shopping wearing mask(removed)
        in level 5: each element records the number of people at that node who have caught covid whilst shopping without a mask(removed)

        The __init__() method defines all of the attributes of a shopper:
        - their position
        - current step on their path journey
        - their covid status
        - their speed of movement (based on the length of their path) and whether there is a one-way system in place
        - whether or not they are wearing a mask

        The move_path() method moves the person along their allocated path. If they are at the end of their path, 
        they (along with their attributes) are removed from the simulation.

        The new_SIR_level() method simulates people becoming infected and hence being moved to level 4 of the cords array
        i.e. their SIR_level becomes 4.

        The change_status() method ... # not too sure

        The results() method runs the simulation for as many time steps as the duration and obtains the following results:
        - number of people who've left the shop
        - number of peoplpe who left the shop that were intially infected
        - % of people who left the shop that were intially infected
        - number of people who did not catch covid
        - number of people who left that caught covid while shopping
        - number of people who've left that were initially suseptible
        - % of people who entered the shop suseptile who left with covid
        - average shopping time
    """
    

    cords = np.zeros((6,8,7))

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
        self.speed = speed # 0 = slow walker 1 = quick walker 2 = one way path system
        self.mask = mask # 1 = wearing mask, 0 = no mask



        if self.speed == 0: # if assignment of speed is zero then person with slow path
            rand_int = randint(0, len(person.slow_paths))
            self.path = person.paths[rand_int]
        elif self.speed == 1: # if random assignment of speed is 1 then person has a quick path
            rand_int = randint(0, len(person.fast_paths))
            self.path = person.fast_paths[rand_int]
        elif self.speed == 2: # if path system is one way
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
            shopping_time_p = len(self.path)
            shopping_time_p = self.shop_time
            simulation.shopping_time.append(shopping_time_p)
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
            if self.mask == 0:
                self.SIR_level = 5 # removed not wearing mask
            else:
                self.SIR_level = 4 #removved wearing mask

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
    # TD:add docstring

    #run the simulation for as many time steps as the duration 
    while simulation.time_step < duration:
        #rgb_matrix = person.cords[0]
        # uncomment this^^^ too see how people move through the shop in the cords array
        # --------------------------------please put into own function??----------------------------------------------------#


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

    # to avoid dividing by zero
    if num_caught_covid == 0:
        num_caught_covid += 0.001
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

#creating a new function to plot still graphs of the results
def plot_results(simulation,duration):
    # setting up the arrays for plotting
    x = np.arange(duration)
    shoppers_at_step = simulation.people_at_time_step
    sus_w_mask = simulation.sus_w_mask_t
    sus_wo_mask = simulation.sus_wo_mask_t
    inf_w_mask_t = simulation.inf_w_mask_t
    inf_wo_mask_t = simulation.inf_wo_mask_t
    caught_covid_t = simulation.caught_cov

    leaving_status = []
    leave_sus = simulation.left_shop.count(0) + simulation.left_shop.count(1)
    leave_caught_covid = simulation.left_shop.count(4)
    leave_initially_infected = simulation.left_shop.count(2) + simulation.left_shop.count(3)
    leaving_status.extend([leave_sus,leave_initially_infected,leave_caught_covid])


    #setting up the plots
    fig, axs = plt.subplots(2, 2, figsize=(12,8)) # making a large figure to show the plots
    #Plotting shoppers within the shop at each time step in simulation
    axs[0, 0].plot(x, shoppers_at_step, '-k') # plotting shoppers with full black line
    axs[0, 0].set_title('Number of People in the shop at each time step') # labelling the plot
    axs[0,0].legend(['Number of Shoppers'])
    #plotting a stacked plot of the shoppers in the shop at each time step in proportion of their status
    axs[0, 1].stackplot(x, sus_wo_mask, sus_w_mask, inf_w_mask_t, inf_wo_mask_t, caught_covid_t,
                        labels=['Susceptable w mask', 'Susceptable wo mask', 'Infected w mask', 'Infected wo mask',
                                'Caught COV in shop'], colors = simulation.COLOURMAP_RGB)
    axs[0,1].legend()
    axs[0, 1].set_title('Total shoppers in the shop with respective status at each time step') # setting title
    axs[0,1].set(xlabel='Time steps (minutes)', ylabel='Shoppers')

    #plotting the number of people who have caught COVID
    axs[1, 0].plot(x, caught_covid_t, ':c')
    axs[1, 0].plot(x, inf_w_mask_t, ':r')
    axs[1, 0].plot(x, inf_wo_mask_t, ':m')
    axs[1, 0].set_title('Number of people who are infected in the shop at t')
    axs[1,0].set(xlabel='Time steps (minutes)', ylabel='Shoppers')
    axs[1,0].legend(['People who caught COVID', 'Infected with a mask', 'Infected without a mask'])

    #pie chart representing how many people left the shop with each end status
    axs[1, 1].pie(leaving_status, colors = simulation.INF_COLOURMAP_RGB)
    axs[1, 1].set_title('Proportion of each SIR level when leaving')
    axs[1, 1].legend(['Left the shop susceptible', 'Left the shop infected','Left the shop having caught COVID'], loc = 'upper right')
    # tight layout ensures all the legeds and titles fit within fig
    fig.tight_layout()


#function for getting user input if prompted
def get_user_input():
    entry = input("Maximum number of people who can enter the shop at once: ")
    duration = input("Number of time steps to run the simulation for: ")
    max_shoppers = input("Maximum number of people allowed in the shop at once: ")
    month = input("The month of data to retrieve COVID infection rate for: ")
    path_system = input("The type of path system 0 = slow walker 1 = quick walker 2 = one way path system, 3 = mixed speed scenario: ")
    params = [entry, duration, max_shoppers,month,path_system]
    if all(str(i).isdigit() for i in params):  # Check input is valid
        params = [int(x) for x in params]
    else:
        print(
            "Could not parse input. The simulation will use default values:",
            "\n5 people max entry at one time, 30 people max in the shop at one time, and the simulation will run for 200 time steps "
            "using the month of 1120 for data, slow walkers and each individual having a 25% chance of entering the shop with infected.",
        )
        params = [5, 200, 30,1120,0]
    return params

class Animation:
    """Class to run the line and grid animation"""
    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration

        self.figure = plt.figure(figsize=(16, 4)) # setting up figure with 2 plots
        self.axes_grid = self.figure.add_subplot(1, 2, 1)
        self.axes_line = self.figure.add_subplot(1, 2, 2)
        self.gridanimation = GridAnimation(self.axes_grid, self.simulation) # calling grid animation class
        self.lineanimation = LineAnimation(self.axes_line, self.simulation, duration) # calling line animation class

    def show(self):
        """Run the animation on screen"""
        animation = FuncAnimation(self.figure, self.update, frames=range(self.duration),
                init_func = self.init, blit=True, interval=200,repeat = False) # using funcanimation to run the animation
        plt.tight_layout()
        plt.show()

    def init(self):
        """Initialise the animation (called by FuncAnimation)"""
        actors = []
        actors += self.gridanimation.init()
        actors += self.lineanimation.init()
        return actors

    def update(self, framenumber):
        """Update the animation (called by FuncAnimation) and the respective grid / line animation classes"""
        self.simulation.update()
        actors = []
        actors += self.gridanimation.update(framenumber)
        actors += self.lineanimation.update(framenumber)
        return actors


class GridAnimation:
    """Animate a grid showing the infected people moving round the shop
    and the number of infected people in each node"""

    def __init__(self, axes, simulation):
        self.axes = axes
        self.simulation = simulation
        infected = self.simulation.infected # retrieving infected grid from simulation
        self.shop = np.empty((infected.shape)) # setting up shop as an empty array the same shape as the simulation shop
        infected_range = np.arange(self.simulation.max_shoppers) # retrieving the max_no_shoppers possibly in shop
        self.values = np.unique(infected.ravel()) # retrieving the number of people in each node
        # and storing as a unique integer
        for i in infected_range:
            self.shop[infected == i] = i # making the shop an array
        # where the number corresponds to the number of infected people
        self.image = self.axes.imshow(self.shop, cmap = 'Reds') # choosing a red colour map to align with graphing
        self.axes.set_title('Infected people moving round the shop')
        # get the colors of the values, according to the colormap used by imshow
        colors = [self.image.cmap(self.image.norm(value)) for value in self.values]
        # create a patch (proxy artist) for every color
        for i in range(len(self.values)):
            self.patches = [mpatches.Patch(color=colors[i], label="No infected people in the node: {l}".format(l=self.values[i])) for i in range(len(self.values))]
        self.axes.legend(handles=self.patches, bbox_to_anchor=(1.04, 1), loc=2)

    def init(self):
        return self.update(0)

    def update(self, framenum):
            minute = framenum
            infected = self.simulation.infected
            self.shop = np.empty((infected.shape))
            infected_range = np.arange(self.simulation.max_shoppers)
            self.shop = np.empty((infected.shape))
            self.values = np.unique(infected.ravel())
            for i in infected_range:
                self.shop[infected == i] = i
            self.image.set_array(self.shop)
            return [self.image]


class LineAnimation:
    """Animate a line series showing numbers of people in each status"""

    def __init__(self, axes, simulation, duration):
        self.axes = axes
        self.simulation = simulation
        self.duration = duration
        self.xdata = []
        self.ydata = {status: [] for status in simulation.STATUSES} #setting up poss statuses
        self.line_mpl = {}
        for status, colour in simulation.COLOURMAP.items():
            [line] = self.axes.plot([], [],color=colour, label=status, linewidth=1) # this would
            # be better as a stack plot however cant be animated
            self.line_mpl[status] = line
        self.axes.legend(bbox_to_anchor=(1.04, 1), loc=2)
        self.axes.set_xlabel('Time steps (minutes)')
        self.axes.set_ylabel('No of shoppers')
        self.axes.set_title('Number of people in the shop with each infection level')

    def init(self):
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, self.simulation.max_shoppers]) # setting the y lim so that no matter the proportion
        #can visualise the number of shoppers
        return []

    def update(self,framenum):
        percents = self.simulation.get_node_status() # getting the statuses of each node
        self.xdata.append(len(self.xdata))
        for status, percent in percents.items():
            self.ydata[status].append(percent)
            self.line_mpl[status].set_data(self.xdata, self.ydata[status]) # getting the percentages of
            # people at each infection level
        return list(self.line_mpl.values())



if __name__ == "__main__":

    import sys
    main(sys.argv[1:])


