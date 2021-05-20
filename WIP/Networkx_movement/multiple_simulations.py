import Initial_Simulation as sim
import numpy as np
import matplotlib.pyplot as plt
import argparse 



def main(args):

    # Use argparse to handle parsing the command line arguments.
    #   https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Plot change in covid transmission with respect to chosen simulation variable')
    parser.add_argument('--change', type=int, metavar='name', default=2,
                        help='Name of simulation input argument to vary in each run of the simulation. Key: 0 = entry, 1 = duration, 2 = max_shoppers, 3 = prob_of_i, 4 = chance_person_wears_mask, 5 = level_of_covid_in_area') #with default type for string
    parser.add_argument('--path_system', action='store_true',
                        help='Investigate effect of one-way system') #with default type for string
    args = parser.parse_args(args)
    
    chosen_sim_arg = args.change

    #wether looking at effect of pathsystem or other variable
    if args.path_system:
        plot_results(2, 1)
    else:
        plot_results(chosen_sim_arg, 0)

    


def get_increment_points(chosen_sim_arg):
    """takes chosen simulation input argument and generates a list of increments points specific to the chosen variable's limits"""

    #each possible chosen input's [minimum value, maximul value, and increment size]
    variable_limits = [ [1,100,1], #max people entering in one time step
                       [50,500,3], #duration
                       [10, 100, 1], #max_shoppers
                       [0.05,1,0.005], #prob_of_i
                       [0.02, 0.98, 0.02], #chance_person_wears_mask
                       [0.02,1,0.02], #level_of_covid_in_area 
    ]
    
    min_var = variable_limits[chosen_sim_arg][0]
    max_var = variable_limits[chosen_sim_arg][1]
    inc = variable_limits[chosen_sim_arg][2]
    increment_points = np.arange(min_var, max_var, inc)

    return increment_points
  
                        
def calc_sim_results_mask(simulation):
    """calculates the percentage of people who caught covid out of number who were susceptible wearing masks"""   
    # number of people who left suseptible (didn't catch covid)
    num_not_infected_in_mask = simulation.left_shop.count(0)
    num_caught_covid_in_mask = simulation.left_shop.count(4)

    if num_caught_covid_in_mask == 0:
        caught_in_mask_percent = 0

    else: 
        num_initially_suseptible_in_mask = num_not_infected_in_mask + num_caught_covid_in_mask

        caught_in_mask_percent = (num_caught_covid_in_mask / num_initially_suseptible_in_mask)*100

    return caught_in_mask_percent


def calc_sim_results_wo_mask(simulation):
    """calculates the percentage of people who caught covid out of number who were susceptible without masks"""   
    # number of people who left suseptible (didn't catch covid)
    num_not_infected_wo_mask = simulation.left_shop.count(1)
    num_caught_covid_wo_mask = simulation.left_shop.count(5)

    if num_caught_covid_wo_mask == 0:
        caught_wo_mask_percent = 0
    else:
        num_initially_suseptible_wo_mask = num_not_infected_wo_mask + num_caught_covid_wo_mask

        caught_wo_mask_percent = (num_caught_covid_wo_mask / num_initially_suseptible_wo_mask)*100

    return caught_wo_mask_percent

def calc_sim_results(simulation):
    """calculates the percentage of people who caught covid out of number who were susceptible overall"""   
    # number of people who left suseptible (didn't catch covid)
    num_not_infected = simulation.left_shop.count(1) + simulation.left_shop.count(0)
    # number of people who left that caught covid while shopping
    num_caught_covid = simulation.left_shop.count(5) + simulation.left_shop.count(4)

    if num_caught_covid == 0:
        caught_covid_percent = 0
    else:
        # number of people who've left that were initially suseptible
        num_initially_suseptible = num_not_infected + num_caught_covid   

        caught_covid_percent = (num_caught_covid / num_initially_suseptible)*100

    return caught_covid_percent


def run_multiple_simulations(chosen_sim_arg, variable_values, path_system):
    """runs multiple simulations """
    
    #array to be filled with results from each simulation
    
    sim_inputs_dict = {0 : 3,   #max people entering in one time step
                    1: 150, #duration
                    2: 30, #max_shoppers
                    3 : 0.4, #prob_of_i
                    4 : 0.5, #chance_person_wears_mask
                    5 : 0.3} #level_of_covid_in_area

    #array to be filled with results from each simulation
    mask_results_values = []
    no_mask_results_values = []
    results_values = []

    #for loop to run the simulation for all increment values of the changing variable
    for sim_inputs_dict[chosen_sim_arg] in variable_values:
           
        #setting up varibales for simulation
        max_entry = sim_inputs_dict[0]
        duration = sim_inputs_dict[1]
        max_shoppers = sim_inputs_dict[2]  
        prob_of_i = sim_inputs_dict[3]
        chance_person_wears_mask = sim_inputs_dict[4]
        level_of_covid_in_area = sim_inputs_dict[5]
        path_system = path_system 

        #initiates simulation w/ variables set
        simulation = sim.simulation(max_entry, duration, max_shoppers, path_system, prob_of_i,chance_person_wears_mask, level_of_covid_in_area)
        #add first shopper(s) to shop simulation
        simulation.add_new_shopper(1)
        #update simulation for each timestep
        while simulation.time_step < duration:
            simulation.update()

        #percentage of people who caught covid in this simulation run
        sim_result_m = calc_sim_results_mask(simulation)
        sim_result_n_m = calc_sim_results_wo_mask(simulation)
        sim_result = calc_sim_results(simulation)

        #adding result to array of all results
        mask_results_values.append(sim_result_m)
        no_mask_results_values.append(sim_result_n_m)
        results_values.append(sim_result)

    return mask_results_values, no_mask_results_values, results_values


def get_plot_labels(chosen_sim_arg):
    """returns label for scatter plot x-axis from input argument"""
    #dictionary of possible variable names
    input_arg_names = {0 : 'Maximum number of people who can enter the shop in one timestep',   #max people entering in one time step
                    1 : 'Number of time steps to run simulation for', #duration
                    2 : 'Maximum number of people permitted in the shop at one time', #max_shoppers
                    3 : 'Probability a suseptible person catching covid', #prob_of_i
                    4 : 'Probability shoppers are wearing a mask', #chance_person_wears_mask
                    5 : 'Probability a new shopper is infected'} #level_of_covid_in_area
   #dict of poss title names
    title_dict = {0 : 'How Covid Transmission Rate Changes With Increasing Max Entry ',   #max people entering in one time step
                    1 : 'How Model Prediction Converges With Incresed Time Steps', #duration
                    2 : 'How Covid Transmission Rate Changes With Shop Capacity', #max_shoppers
                    3 : 'How Covid Transmission Changes with Probability of Infection', #prob_of_i
                    4 : 'How Covid Transmission Changes with Increased Mask Wearing', #chance_person_wears_mask
                    5 : 'How Covid Transmission Changes with Initially Infected Shoppers'} #level_of_covid_in_area


    #selecting correct name from dictionary using input arg
    x_axis_label = input_arg_names[chosen_sim_arg]
    title_label = title_dict[chosen_sim_arg]

    return x_axis_label, title_label 

        
def plot_results(chosen_sim_arg, path_system):
    """plots the results of each simulation run at each increment value of the chosen simulation argument"""
    if path_system == 0:
        #run multiple simulations
        variable_values = get_increment_points(chosen_sim_arg)
        results = run_multiple_simulations(chosen_sim_arg, variable_values, 3)
        mask_results = results[0]
        no_mask_results = results[1]
        overall_results = results[2]

        #specifying if double or single line plot 
        two_line = 0
        if chosen_sim_arg < 4:
            two_line += 1
        if chosen_sim_arg == 1:
            two_line -= 1

        # once all simulations have run, plot results as scatter plot
        if two_line == 1:
            #plot line graph with 2 lines (one for mask wearers, one without)
            fig=plt.figure()
            ax=fig.add_subplot(1, 1, 1)
            ax.plot(variable_values, no_mask_results, label = "Not wearing a mask", color='r')
            ax.plot(variable_values, mask_results, label = "Wearing a mask", color='b')      
            ax.legend(['No mask', 'Mask'], loc = 'lower right')
            x_axis_label = get_plot_labels(chosen_sim_arg)[0]
            ax.set_xlabel(x_axis_label)
            ax.set_ylabel('Probability of catching COVID (%)')
            title = get_plot_labels(chosen_sim_arg)[1]
            ax.set_title(title )

        else:
            #plot one line graph 
            fig=plt.figure()
            ax=fig.add_subplot(1, 1, 1)
            ax.plot(variable_values, overall_results, color='green')       
            x_axis_label = get_plot_labels(chosen_sim_arg)[0]
            ax.set_xlabel(x_axis_label)
            ax.set_ylabel('Probability of catching COVID (%)')
            title = get_plot_labels(chosen_sim_arg)[1]
            ax.set_title(title )

        plt.show()


    #plot results of 2 lines (one with one way system (2)/ one without (3)) for how prob of catching covid changes with shop capacity (2)
    if path_system == 1:

        variable_values = get_increment_points(2)


        normal_results = run_multiple_simulations(2, variable_values, 3)
        normal_results = normal_results[2]

        one_way_results = run_multiple_simulations(2, variable_values, 2)
        one_way_results = one_way_results[2]


        fig=plt.figure()
        ax=fig.add_subplot(1, 1, 1)
        ax.plot(variable_values, one_way_results, label = "Not wearing a mask", color='r')
        ax.plot(variable_values, normal_results, label = "Wearing a mask", color='b')      
        ax.legend(['with one way system', 'as normal'], loc = 'lower right')
        x_axis_label = get_plot_labels(2)[0]
        ax.set_xlabel(x_axis_label)
        ax.set_ylabel('Probability of catching COVID (%)')
        title = get_plot_labels(2)[1]
        ax.set_title(title)

        plt.show()


if __name__ == "__main__":

    import sys
    main(sys.argv[1:])
