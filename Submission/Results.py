#import random as rd
from statistics import mean


# Import path generation from other file
# Import aldi layout for other file

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