'SIMULATING TRANSMISSION OF COVID-19 IN A SHOP SPACE TO ASSESS THE IMPACT OF SHOPPING RESTRICTIONS'
A project completed by: Zara Burton, Will Smy, Ebony Stephenson and Hannah Spurgeon

Inorder to run the script the following packages have to be installed: 
numpy, argparse, statistics, matplotlib, networkx, itertools


Main.py function should be used for running a simulation of COVID spreading in a supermarket.
Running the Main.py function runs a simulation and shows the user an animation of it for visualisation. 
The programme can also be run with a GUI : WILL ADD NOTE HERE 

The shop is simulated as a 3d array 8 nodes by 7 nodes in 6 layers. 
Multiple people can be in the same node at the same time.

The 6 layers correspond to 6 states of people being simulated:
- Susceptible with masks
- Susceptible without masks 
- Infected with masks 
- Infected without masks 
- Caught COVID in shop with mask 
- Caught COVID in shop without a mask

Nodes are representative of a section in a shop, hence multiple people can be present eg. meat counter.
There are a number of input arguments which can explored.
Changing these shows the impact of different restrictions on the proportion of people who get infected in a shop:
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

An analysis of varying the restrictions was completed by running the simulation for multiple iterations.
The results of this are presented in the report also appended in this repositary.