
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Animation:
    """Class to run the line and grid animation"""
    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration

        self.figure = plt.figure(figsize=(16, 4)) # setting up figure with 2 plots
        self.axes_grid = self.figure.add_subplot(1, 2, 1)
        self.axes_line = self.figure.add_subplot(1, 2, 2)
        self.gridanimation = GridAnimation(self.axes_grid, self.simulation) # calling grid animation class
        self.lineanimation = LineAnimation(self.axes_line, self.simulation, duration) # calling line animation class

    def show(self):
        """Run the animation on screen"""
        animation = FuncAnimation(self.figure, self.update, frames=range(self.duration),
                init_func = self.init, blit=True, interval=200,repeat = False) # using funcanimation to run the animation
        plt.tight_layout()
        plt.show()

    def init(self):
        """Initialise the animation (called by FuncAnimation)"""
        actors = []
        actors += self.gridanimation.init()
        actors += self.lineanimation.init()
        return actors

    def update(self, framenumber):
        """Update the animation (called by FuncAnimation) and the respective grid / line animation classes"""
        self.simulation.update()
        actors = []
        actors += self.gridanimation.update(framenumber)
        actors += self.lineanimation.update(framenumber)
        return actors


class GridAnimation:
    """Animate a grid showing the infected people moving round the shop
    and the number of infected people in each node"""

    def __init__(self, axes, simulation):
        self.axes = axes
        self.simulation = simulation
        infected = self.simulation.infected # retrieving infected grid from simulation
        self.shop = np.empty((infected.shape)) # setting up shop as an empty array the same shape as the simulation shop
        infected_range = np.arange(self.simulation.max_shoppers) # retrieving the max_no_shoppers possibly in shop
        self.values = np.unique(infected.ravel()) # retrieving the number of people in each node
        # and storing as a unique integer
        for i in infected_range:
            self.shop[infected == i] = i # making the shop an array
        # where the number corresponds to the number of infected people
        self.image = self.axes.imshow(self.shop, cmap = 'Reds') # choosing a red colour map to align with graphing
        self.axes.set_title('Infected people moving round the shop')
        # get the colors of the values, according to the colormap used by imshow
        colors = [self.image.cmap(self.image.norm(value)) for value in self.values]
        # create a patch (proxy artist) for every color
        for i in range(len(self.values)):
            self.patches = [mpatches.Patch(color=colors[i], label="No infected people in the node: {l}".format(l=self.values[i])) for i in range(len(self.values))]
        self.axes.legend(handles=self.patches, bbox_to_anchor=(1.04, 1), loc=2)

    def init(self):
        return self.update(0)

    def update(self, framenum):
            minute = framenum
            infected = self.simulation.infected
            self.shop = np.empty((infected.shape))
            infected_range = np.arange(self.simulation.max_shoppers)
            self.shop = np.empty((infected.shape))
            self.values = np.unique(infected.ravel()) # working out the range of numbers of people within each node
            for i in infected_range:
                self.shop[infected == i] = i # appending infected number to shop
            self.image.set_array(self.shop) # updating shop image
            return [self.image]


class LineAnimation:
    """Animate a line series showing numbers of people in each status in the shop at each time step"""

    def __init__(self, axes, simulation, duration):
        self.axes = axes
        self.simulation = simulation
        self.duration = duration
        self.xdata = []
        self.ydata = {status: [] for status in simulation.STATUSES} #setting up poss statuses
        self.line_mpl = {}
        for status, colour in simulation.COLOURMAP.items():
            [line] = self.axes.plot([], [],color=colour, label=status, linewidth=1) # this would
            # be better as a stack plot however cant be animated
            self.line_mpl[status] = line
        self.axes.legend(bbox_to_anchor=(1.04, 1), loc=2)
        self.axes.set_xlabel('Time steps (minutes)')
        self.axes.set_ylabel('No of shoppers')
        self.axes.set_title('Number of people in the shop with each infection level')

    def init(self):
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, self.simulation.max_shoppers])
        # setting the y lim so that no matter the proportion
        #can visualise the number of shoppers
        return []

    def update(self,framenum):
        percents = self.simulation.get_node_status() # getting the statuses of each node
        print(percents)
        self.xdata.append(len(self.xdata))
        for status, percent in percents.items():
            self.ydata[status].append(percent)
            self.line_mpl[status].set_data(self.xdata, self.ydata[status]) # getting the number of people at each infection level
        return list(self.line_mpl.values())

