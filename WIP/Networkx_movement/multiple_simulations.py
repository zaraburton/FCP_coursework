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
    args = parser.parse_args(args)
    
    chosen_sim_arg = args.change 
   
    plot_results(chosen_sim_arg)
    


def get_increment_points(chosen_sim_arg):
    """takes chosen simulation input argument and generates a list of increments points specific to the chosen variable's limits"""

    #each possible chosen input's [minimum value, maximul value, and increment size]
    variable_limits = [ [1,20,1], #max people entering in one time step
                       [50,500,5], #duration
                       [10,200, 5], #max_shoppers
                       [0.05,1,0.05], #prob_of_i
                       [0.02, 0.98, 0.02], #chance_person_wears_mask
                       [0.05,1,0.05], #level_of_covid_in_area 
    ]
    
    min_var = variable_limits[chosen_sim_arg][0]
    max_var = variable_limits[chosen_sim_arg][1]
    inc = variable_limits[chosen_sim_arg][2]
    increment_points = np.arange(min_var, max_var, inc)

    return increment_points
  
                        
def calc_sim_results(simulation):
    """calculates the percentage of people who caught covid out of number who were susceptible"""   
    # number of people who left suseptible (didn't catch covid)
    num_not_infected = simulation.left_shop.count(0) + simulation.left_shop.count(1)
    # number of people who left that caught covid while shopping
    num_caught_covid = simulation.left_shop.count(4)
    if num_caught_covid == 0:
        num_caught_covid += 0.01
    # number of people who've left that were initially suseptible
    num_initially_suseptible = num_not_infected + num_caught_covid
    # calculate % of people who entered the shop suseptile who left with covid
    percentage_who_caught_covid = (num_caught_covid / num_initially_suseptible)*100

    return percentage_who_caught_covid


def run_multiple_simulations(chosen_sim_arg, variable_values):
    """doc string"""
    
    #array to be filled with results from each simulation
    
    sim_inputs_dict = {0 :5,   #max people entering in one time step
                    1: 150, #duration
                    2: 40, #max_shoppers
                    3 : 0.25, #prob_of_i
                    4 : 0.6, #chance_person_wears_mask
                    5 : 0.25} #level_of_covid_in_area

 
    #array to be filled with results from each simulation
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
        path_system = 1 # different plot needed for this changing

        #initiates simulation w/ variables set
        simulation = sim.simulation(max_entry, duration, max_shoppers, prob_of_i, chance_person_wears_mask, level_of_covid_in_area, path_system)
        #add first shopper(s) to shop simulation
        simulation.add_new_shopper(1)
        #update simulation for each timestep
        while simulation.time_step < duration:
            simulation.update()

        #percentage of people who caught covid in this simulation run
        sim_result = calc_sim_results(simulation)
        #adding result to array of all results
        results_values.append(sim_result)
    return results_values


def get_x_axis_label(chosen_sim_arg):
    """returns label for scatter plot x-axis from input argument"""
    #dictionary of possible variable names
    input_arg_names = {0 : 'Maximum number of people who can enter the shop in one timestep',   #max people entering in one time step
                    1 : 'Number of time steps to run simulation for', #duration
                    2 : 'Maximum number of people permitted in the shop at one time', #max_shoppers
                    3 : 'Probability a suseptible person catching covid', #prob_of_i
                    4 : 'Probability shoppers are wearing a mask', #chance_person_wears_mask
                    5 : 'Probability a new shopper is infected'} #level_of_covid_in_area

    #selecting correct name from dictionary using input arg
    x_axis_label = input_arg_names[chosen_sim_arg]
    print(x_axis_label)

    return x_axis_label

        
def plot_results(chosen_sim_arg):
    """scatter plot the results of each simulation run at each increment value of the chosen simulation argument"""
    #run multiple simulations

    variable_values = get_increment_points(chosen_sim_arg)
    results_values = run_multiple_simulations(chosen_sim_arg, variable_values)
    # once all simulations have run 
    # plot results as scatter plot
    fig=plt.figure()
    ax=fig.add_subplot(1, 1, 1)
    ax.scatter(variable_values, results_values, color='r')

    x_axis_label = get_x_axis_label(chosen_sim_arg)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel('Risk of catching COVID')
    #ax.set_title('''scatter plot')

    plt.show()


if __name__ == "__main__":

    import sys
    main(sys.argv[1:])