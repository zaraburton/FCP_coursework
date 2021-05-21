import argparse
#import random as rd
import matplotlib.pyplot as plt
# Import path generation from other file
# Import aldi layout for other file
import Infection_rate_data as inf_rate
from Simulation import simulation as simulation
from Results import results as results
from Animation import Animation as Animation
from Plot_results import plot_results as plot_results

'''Main function used for running a simulation of COVID spreading in a supermarket
The shop is simulated as a 3d array 8 nodes by 7 nodes in 5 layers. 
Multiple people can be in the same node at the same time.
Nodes set to represent a section in a shop eg. meat counter.
There are a number of input arguments which can be input:
 - max_entry is the number of people who can enter at once
 - duration is the time steps to run the simulation for (to simulate minutes)
 - max_shoppers is the maximum number of shoppers who can be in the shop space
 - month is used to set the infection rate, based off of COVID infection levels
in bristol where 320 is March 2020 (from 320 - 421) can not set to set specific level of covid
 - path_system 0 = slow walker 1 = quick walker 2 = one way path system, 3 = mixed speed scenario
 - level_of_covid is the probability of any individual in the area being infected 
 - prob_of_i is the probability of any individual getting infected from the shop
 - chance_a_person_wears_a_mask sets likelyhood of mask wearers (1 for all masked, 0 for no masked)
 - input --plot to retrieve plots from simulation instead of the animation which is the default
 
 
 The command line interface to the script makes it possible to run different
simulations without needing to edit the code e.g.:

    $ python Main.py                     # run simulation with default settings
    $ python Main.py --duration = 120    # have run for 120 time steps (minutes)
    $ python Main.py --help              # show all command line options
'''

def main(args):
    #using argpas to handing parsing command line arguments
    parser = argparse.ArgumentParser(description='Animate an epidemic')
    parser.add_argument('--max_entry', metavar='N', type=int, default=5,
                        help='Maximum of N people can enter at once')
    parser.add_argument('--duration', metavar='N', type=int, default=200,
                        help='Run simulation for N time steps')
    parser.add_argument('--max_shoppers', metavar='N', type=int, default=30,
                    help='Maximum number of shoppers in the shop')
    parser.add_argument('--month', metavar='myy', type=int, default=1120,
                    help='The month to use to represent the infection rate where 320 is March 2020 (from 320 - 421)')
    parser.add_argument('--path_system', metavar='N', type=int, default=0,
                    help='The type of path system 0 = slow walker 1 = quick walker 2 = one way path system, 3 = mixed scenario')
    parser.add_argument('--level_of_covid', metavar='P', type=float, default=0.25,
                    help='Probability of any individual in the area being infected')
    parser.add_argument('--prob_of_i', metavar='P', type=float, default=0.2,
                        help='Probability of any individual getting infected from the shop')
    parser.add_argument('--chance_person_wears_a_mask', metavar='P', type=float, default=0.4,
                        help='Probability of any individual wearing a mask')
    parser.add_argument('--plot', action='store_true',
                    help='Generate plots instead of animation')
    args = parser.parse_args(args)

    #if the user has specified a month to use for the infection rate basis
    if args.month:
        level_of_covid_in_area = inf_rate.infection_rate(args.month)
    #if month not set then the level of covid variable used to base likelyhood of new person being infected
    else:
        level_of_covid_in_area = args.level_of_covid



    sim = simulation(args.max_entry, args.duration, args.max_shoppers, args.path_system, args.prob_of_i, args.chance_person_wears_a_mask, level_of_covid_in_area)
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


if __name__ == "__main__":

    import sys
    main(sys.argv[1:])
