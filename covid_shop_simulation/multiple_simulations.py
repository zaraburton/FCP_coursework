import Initial_Simulation as sim
import numpy as np
import matplotlib.pyplot as plt


def covid_results_calculation(simulation):
    """calculates the percentage of people who caught covid out of number who were susceptible"""   
    # number of people who left suseptible (didn't catch covid)
    num_not_infected = simulation.left_shop.count(0) + simulation.left_shop.count(1)
    # number of people who left that caught covid while shopping
    num_caught_covid = simulation.left_shop.count(4)
    # number of people who've left that were initially suseptible
    num_initially_suseptible = num_not_infected + num_caught_covid
    # calculate % of people who entered the shop suseptile who left with covid
    percentage_who_caught_covid = (num_caught_covid / num_initially_suseptible)*100

    return percentage_who_caught_covid

#def limit(n, minn, maxn):
  #  """sets min and max values for variable"""""
  #  return max(min(maxn, n), minn)

#currently got it working for changing the max_shoppers variable 

#generating different values of the changing variable
min_variable = 10
max_variable = 200
increment = 5

# array of all values of the changing variable to run the simulation for 
variable = np.arange(min_variable, max_variable, increment)

#array to be filled with results from each simulation
results = []



#for loop to run the simulation for all increment values of the changig variable
for i in variable:
    #changing variable in simulation
    var = i 

    #setting up varibales for simulation
    max_entry = 10
    duration = 100
    max_shoppers = var
    prob_of_i = 0.1
    chance_person_wears_mask = 0.6
    level_of_covid_in_area = 0.2
    path_system = 1

    #initiates simulation w/ variables set
    simulation = sim.simulation(max_entry, duration, max_shoppers, prob_of_i, chance_person_wears_mask, level_of_covid_in_area, path_system)
    #add first shopper(s) to shop simulation
    simulation.add_new_shopper()
    #update simulation for each timestep
    while simulation.time_step < duration:
        simulation.update()
    
    #percentage of people who caught covid in this simulation run
    result = covid_results_calculation(simulation)
    results.append(result)

# once all simulations have run 
# plot results as scatter plot
fig=plt.figure()
ax=fig.add_subplot(1, 2, 1)
ax.scatter(variable, results, color='r')
ax.set_xlabel('variable value')
ax.set_ylabel('risk of catching covid')
ax.set_title('scatter plot')

plt.show()