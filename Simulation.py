import numpy as np
#import random as rd
from numpy.random import random, randint
# Import path generation from other file
import Networkx_random_path_example as path_gen
# Import aldi layout for other file
import Networkx_aldi_layout as lay
import Simulation as simulation


# ----------------------------------------------------------------------------#
#                  Simulation class                                          #
# ----------------------------------------------------------------------------#

class simulation:
    """Simulation of the spread of covid within a matrix, representing a supermarket.

    The supermarket is represented as an 8 x 7 x 6 grid.
    The 8 x 7 x 2 array reprensents the shop space.

    There is one entrance at the bottom left and two exits at the top right of the grid.
    The number in each position denotes the number of people in each location within the shop.

    - The 'update()' method advances the simulation by one timestep (minute).
    - The 'update_infection_risk()' method updates matrix for risk of infection at each node in the shop.
    - The 'get_number_of_shoppers_entering()' method finds the number of people who can enter the shop at a time step.
    - The 'add_new_shopper()' method introduces a new shopper into the store simulation based on number of shoppers entering.
    - The 'get_node_status()' method extracts the number of people with each status at each timestep.
    - The 'get_shop_numbers()' method records the state of the simulation at each time_step.
    
    """
    #vectors used for keeping track of states
    left_shop = [] # statuses of people who have left
    shoppers = [] # vector containg instance of each person currently in the shop
    people_at_time_step = []     # array storing number of people in shop at each time step
    shopping_count = [] #vector to count number of people who are in shop
    shopping_time = [] # vector to contain length of shopping time per person
    # vectors to record total number of people at t with each SIR level
    sus_w_mask_t = []
    sus_wo_mask_t = []
    inf_w_mask_t = []
    inf_wo_mask_t = []
    caught_cov_m = []
    caught_cov_nm = []

    # Status codes to store in the numpy array representing the state.
    SUSCEPTABLE_W_MASK = 0
    SUSCEPTABLE_WO_MASK = 1
    INFECTED_W_MASK = 2
    INFECTED_WO_MASK = 3
    CAUGHT_COV_IN_SHOP_M = 4
    CAUGHT_COV_IN_SHOP_NM = 5

    STATUSES = {
        'Susceptible with a mask': SUSCEPTABLE_W_MASK,
        'Susceptible without a mask': SUSCEPTABLE_WO_MASK,
        'Infected with a mask': INFECTED_W_MASK,
        'Infected without a mask': INFECTED_WO_MASK,
        'Caught COVID w mask': CAUGHT_COV_IN_SHOP_M,
        'Caught COVID wo a mask': CAUGHT_COV_IN_SHOP_NM,
    }

    COLOURMAP = {
        'Susceptible with a mask': 'yellow',
        'Susceptible without a mask': 'green',
        'Infected with a mask': 'red',
        'Infected without a mask': 'magenta',
        'Caught COVID w mask': 'cyan',
        'Caught COVID wo a mask': 'blue',
    }
    COLOURMAP_RGB = {
        'yellow': (255, 255, 0),
        'green': (0, 255, 0),
        'red': (255, 0, 0),
        'magenta': (255, 0, 255),
        'cyan': (0, 255, 255),
        'blue': (0, 0, 255),
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
    shop_infection_risk = np.zeros((2, 8, 7))


    def __init__(self, entry, duration, max_shoppers, path_system, prob_of_i, chance_person_wears_mask,
                 level_of_covid_in_area):
        # Basic simulation perameters:
        self.max_entry = entry  # max number of people who can enter at once
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

        # update the infection risk matrix now that people have moved
        self.update_infection_risk()

        # assign new SIR level to every shopper based on everyone new position
        [person.new_SIR_level() for person in simulation.shoppers if person.SIR_level < 2]

        # assign number of shoppers to enter at this timestep
        number_of_new_shoppers = self.get_number_of_shoppers_entering()

        # adding the new people to the shop
        self.add_new_shopper(number_of_new_shoppers)

        simulation.people_at_time_step.append(len(self.shoppers))
        self.get_shop_numbers()

        simulation.infected = (person.cords[2] + person.cords[3] + person.cords[4] + person.cords[5])
        # add one to the time step counter

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
            number_of_shoppers_entering = randint(0, self.max_entry + 1)


        elif len(simulation.shoppers) < self.max_shoppers:
            # max number of people that can enter
            max_entry_to_meet_capacity = self.max_shoppers - len(simulation.shoppers)
            # randomly picking number of new people to enter shop that wont go over maximum capacity
            number_of_shoppers_entering = randint(0, max_entry_to_meet_capacity + 1)

        else:
            number_of_shoppers_entering = 0

        return number_of_shoppers_entering

    def add_new_shopper(self, number_of_shoppers_entering):
        """adds new person the the shop"""
        # creates a new instance of a person thats either
        # suseptible or infected, based on the "level of covid
        # in the area" and adds them to the list of shoppers

        shoppers_to_add = np.arange(number_of_shoppers_entering)

        if self.path_system == 2:  # when user has specified 1 way simulation
            speed = 2  # assign one way paths
        elif self.path_system == 1:  # when all shoppers move quickly
            speed = 1  # assign speed being quick
        elif self.path_system == 0:  # when all shoppers move slowly
            speed = 0
        elif self.path_system == 3:
            speed = randint(0, 1)  # assign shoppers slow and quick paths randomly

        for shopper in shoppers_to_add:
            # add infected person
            if self.level_of_covid_in_area > random():
                if self.chance_person_wears_mask > random():
                    # add infected person with mask
                    mask = 1
                    simulation.shoppers.append(person((0, 0), 2, speed, mask))
                else:
                    # add infected person without mask
                    mask = 0
                    simulation.shoppers.append(person((0, 0), 3, speed, mask))

            # add suseptible person
            else:
                if self.chance_person_wears_mask > random():
                    # add suseptible person w/ mask
                    mask = 1
                    simulation.shoppers.append(person((0, 0), 0, speed, mask))
                else:
                    # add suseptible person w/o mask
                    mask = 0
                    simulation.shoppers.append(person((0, 0), 1, speed, mask))

    def get_node_status(self):

        simgrid = person.cords[0] + person.cords[1] + person.cords[2] + person.cords[3] + person.cords[4] + person.cords[5]  # total people in shop
        state = person.cords
        total_people = np.sum(simgrid)
        #called percentages but actually is a count of the people
        percentages = {}
        for status, statusnum in self.STATUSES.items():
            count = np.sum(simgrid[statusnum])  # taking each state of person from the stacked array
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
            caught_covid_mask = person.cords[4]
            simulation.caught_covid_mask = caught_covid_mask
            caught_covid_n_mask = person.cords[5]
            simulation.caught_covid_mask = caught_covid_n_mask

            simulation.susceptible = (sus_no_mask + sus_mask)  # counting susceptible people for animation
            simulation.infected = (inf_mas + inf_no_mask + caught_covid_mask +caught_covid_n_mask)  # counting infected people for animation
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

            caught_m = np.sum(caught_covid_mask)
            simulation.caught_cov_m.append(caught_m)

            caught_nm = np.sum(caught_covid_n_mask)
            simulation.caught_cov_nm.append(caught_nm)


# ----------------------------------------------------------------------------#
#                  Person class                                              #
# ----------------------------------------------------------------------------#

class person:
    """ Class representing the shoppers within the supermarket.

        The cords array has 5 layers, each of size 8 x 7, which contain the number of people at each position within the shop.
        Each layer represents a Covid status:
        in level 0: each element records the number of people at that node who are suseptible wearing a mask
        in level 1: each element records the number of people at that node who are suseptible and not wearing a mask
        in level 2: each element records the number of people at that node who are infected & wearing a mask
        in level 3: each element records the number of people at that node infected and not wearing a mask
        in level 4: each element records the number of people at that node who have caught covid whilst wearing a mask
        in level 5: each element records the number of people at that node who have caught covid whilst not wearing a mask

        The __init__() function defines all of the attributes of a shopper:
        - their position
        - current step on their path journey
        - their covid status
        - their speed of movement (based on the length of their path) and whether there is a one-way system in place
        - whether or not they are wearing a mask

        The move_path() function moves the person along their allocated path. If they are at the end of their path,
        they (along with their attributes) are removed from the simulation.

        The new_SIR_level() function simulates people becoming infected and hence being moved to level 4 of the cords array
        i.e. their SIR_level becomes 4.

    """
    cords = np.zeros((6, 8, 7))
    # all possible paths that could be taken by a person through the shop
    paths = path_gen.possible_paths(lay.aldi_layout(), (0, 0), [(6, 6), (7, 6)])
    slow_paths = path_gen.slow_paths(lay.aldi_layout(), (0, 0), [(6, 6), (7, 6)])
    fast_paths = path_gen.fast_paths(lay.aldi_layout(), (0, 0), [(6, 6), (7, 6)])
    one_way_paths = path_gen.possible_paths_oneway(lay.aldi_layout(), (0, 0), [(6, 6), (7, 6)])

    # Setting initial varibles for each person
    def __init__(self, pos, covid_status, speed, mask):
        self.pos = pos  # Position in network
        self.n = 0  # current step in path (0 is the entrance of the shop)
        self.SIR_level = covid_status  # their SIR level (0=suseptible (w/m) 1= s (w/o m) 2= Infected (w/ mask) 3= infected (w/o mask) 4= removed)
        self.speed = speed  # 0 = slow walker 1 = quick walker 2 = one way path system
        self.mask = mask  # 1 = wearing mask, 0 = no mask

        if self.speed == 0:  # if assignment of speed is zero then person with slow path
            rand_int = randint(0, len(person.slow_paths))
            self.path = person.paths[rand_int]
        elif self.speed == 1:  # if random assignment of speed is 1 then person has a quick path
            rand_int = randint(0, len(person.fast_paths))
            self.path = person.fast_paths[rand_int]
        elif self.speed == 2:  # if path system is one way
            rand_int = randint(0, len(person.one_way_paths))
            self.path = person.one_way_paths[rand_int]

        self.shop_time = len(self.path)

        # status is their path and covid status in one thats used in the cords array
        # eg path of [(0,0), (0,1), (0,2)] for an infected person becomes
        # a status of [(1,0,0), (1,0,1), (1,0,2)]
        # the for loop takes each element in the paths list, turns it from a tuple to a list to edit it,
        # then back into a tuple, then adds it to the self.status list
        self.status = []
        for t in self.path:
            node = list(t)
            new_list = [self.SIR_level] + node
            x = tuple(new_list)
            self.status.append(x)

        # setting the persons position in the cords array
        self.pos = self.status[0]
        person.cords[(self.pos)] += 1

    def move_path(self):
        # if someones at the end o their path then ...
        if self.n == (len(self.status) - 1):
            # remove them from current position in cords array
            person.cords[(self.pos)] -= 1

            # takes info from them
            leaving_info = self.SIR_level
            shopping_time_p = len(self.path)
            shopping_time_p = self.shop_time
            simulation.shopping_time.append(shopping_time_p)
            # and stores it in the left_shop array in the simulation class
            simulation.left_shop.append(leaving_info)
            # then remove them from the list of current shoppers
            simulation.shoppers.remove(self)

        # move the person if they're not at the end of their path
        if self.n < (len(self.status) - 1):
            # remove them from current position in cords array
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

