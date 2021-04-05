
# ''This code attempts to simulate multiple random walks in the same space, which is defined as the process of taking successive steps in a randomised fashion. Here I am experimenting with a simplified random walk, starting at an origin and defining a discrete step size, chosen from [-1,0,1] where each step size has an equal probability of being actioned. Starting points are given '+' and end points are given 'o'.'' #Random 2D walk 
# Now as we are in 2d, instead of there being 3 options for movement, there are nine, a bit like degrees of freedom, each step now has another dimension available. The code is identical, just with the dims number making a difference to the step shape and therefore the path 
# 
# 


#these are the modules needed to be installed to allow for the code to work
get_ipython().run_line_magic('pylab', 'inline')
from itertools import cycle
import numpy as np
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')

#2d random walk 
#start at y=0 and choose a step to move for each step in the simulation, where each step has equal prob 
# setting constants for the walk 

#dimensions
dims = 2
#step number
step_n=10000
#the available step sizes 
step_set = [-1,0,1]
#setting up an array 
origin = np.zeros((1,dims))

# simulating the steps 
#the number of steps to be taken and the number of dimensions
step_shape = (step_n,dims)
# using numpy to make a random choice from step set as to what step to take
steps = np.random.choice(a=step_set, size =step_shape)
#plotting the path by combbining the origin and the steps matrix 
path = np.concatenate([origin, steps]).cumsum(0)
#path is now a 10,000 by 1 matrix with all the steps at each step included in it
#set the start and end to be the first and last points in path 
start = path[:1]
stop = path[-1:]

# plot the path on a graph, specifying the fig size and the axis 
fig = plt.figure(figsize = (8,8),dpi=200)
ax = fig.add_subplot(111)

#plotting a scatter graph with the x axis being numbeer of steps and then y being the bath 
ax.scatter(path[:,0], path[:,1],c='blue', alpha = 0.25, s=0.05);
ax.plot(path[:,0],path[:,1], c='blue', alpha = 0.5, lw=0.25,ls='-');
ax.plot(start[:,0], start[:,1], c='red', marker = '+')
ax.plot(stop[:,0],stop[:,1], c='black',marker='o')

plt.title('2D Random Walk')
plt.tight_layout(pad=0)
#plt.savefig('Random_walk_2d')

# define number of runs 
n_runs = 10
runs = np.arange(n_runs)
i = 250

for i, col in zip(runs, colors):
    # Simulate steps
    origin = np.random.randint(low=-10,high=10,size=(1,dims))
    steps = np.random.choice(a=step_set, size=step_shape)
    path = np.concatenate([origin, steps]).cumsum(0)
    start = path[:1]
    stop = path[-1:]
    
#plotting a scatter graph with the x axis being numbeer of steps and then y being the bath 
ax.scatter(path[:,0], path[:,1],c=col, alpha = 0.15, s=1);
ax.plot(path[:,0],path[:,1], c=col, alpha = 0.25, lw=0.25);
ax.plot(start[:,0], start[:,1], c=col, marker = '+')
ax.plot(stop[:,0],stop[:,1], c=col,marker='o')

plt.title('2D Random Walk with 10 people')
plt.tight_layout(pad=0)
plt.savefig('Random_walk_2d', dpi = 250)




