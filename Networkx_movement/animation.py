# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 10:08:08 2021

Animation class to animate the simulation of person and shop classes.

@author: hanspurge
"""
import numpy as np
import random as rd
import networkx as nx
import matplotlib.animation as animation
import matplotlib.pyplot as plt


# Import path generation from other file
import Networkx_random_path_example as path_gen
# Import aldi layout for other file
import Networkx_aldi_layout as lay
# Import aldi layout for other file
import Initial_Simulation as sim

# pulling graph from aldilayout
G = lay.aldi_layout()

class NetworkAnimation:
    ''' Animate network showing movement of people'''
    def __init__(self,axes,sim):
        self.axes = axes
        self.sim = sim
#function to enable the animation of movement from person
# i is the number of frames the animation needs
# a frame is like a still image of the network at each point in sim
# defining list of colours for the graph
    colours = ['r', 'b', 'g', 'y', 'w', 'm']
    def animate(self, i):
        nx.draw_networkx(G,pos = sim.pos,node_color = [random.choice(colors) for j in range(9)])
    nx.draw(G)
    fig = plt.gcf()
# anim repeated calls animate function, incrementing i in each iteration
# frames defines the number of times we call animate - should be time increment relating to sim when we have it
#20 for now as no time in sim class
# interval is the interval between each call, default set to 20 for now
# blit true just makes sure we only change the network parts that have change
    anim = animation.FuncAnimation(fig,animate,frames = 20 , interval =20 , blit=True)
