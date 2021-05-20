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


if __name__ == "__main__":

    import sys
    main(sys.argv[1:])