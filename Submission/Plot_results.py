import numpy as np
#import random as rd
import matplotlib.pyplot as plt


# Import path generation from other file
# Import aldi layout for other file
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
