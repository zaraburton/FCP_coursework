
#''This code attempts to simulate a random walk, which is defined as the process of taking successive steps in a randomised fashion. Here I am experimenting with a simplified random walk, starting at an origin and defining a discrete step size, chosen from [-1,0,1] where each step size has an equal probability of being actioned. Starting points are given '+' and end points are given 'o'.'' 


#these are the modules needed to be installed to allow for the code to work (numpy and matplotlib)
get_ipython().run_line_magic('pylab', 'inline')
from itertools import cycle
from mpl_toolkits.mplot3d import Axes3D
#creating a colours matrix for use later in plotting 
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')

#1d random walk 
#start at y=0 and choose a step to move for each step in the simulation, where each step has equal prob 
# setting constants for the walk 
#dimensions
dims = 1
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
fig = plt.figure(figsize = (8,4),dpi=200)
ax = fig.add_subplot(111)

#plotting a scatter graph with the x axis being numbeer of steps and then y being the bath 
ax.scatter(np.arange(step_n+1),path, alpha = 0.25, s=0.5)

#plotting the path and specifying the type of line ect
ax.plot(path,alpha=0.5,lw=0.5,linestyle = '-');
#plotting start and stop 
ax.plot(0, start,'red', marker='+')
ax.plot(step_n, stop, c='black', marker='o')
plt.title('1D Random Walk')
plt.tight_layout(pad=0)
#saving fig to the area 
#plt.savefig('random_walk_1d.png',dpi=250);




