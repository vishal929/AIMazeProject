# this serves as a driver to generate a plot for the dfs using matplotlib

# calls my dfs probability helper function and uses it to generate a plot

from Preliminaries.DFS import dfsProbabilityHelper
import matplotlib.pyplot as plt

# will increment blocking factor from 0.05 to 1 in steps of 0.05, then it will generate a maze of dim 1000
    # then it will run the preliminary dfs implementation
    # this is repeated 100 times for every new matrix to get a solid probability
    # the results are outputted in an array of tuples in the form [(blockingFactor,probSuccess),...]
    # these results will make the graph easy to plot and we will have a solid number of points of data

#for now this is just a test with maze dim of 5x5 and sample size of 1000
result = dfsProbabilityHelper(5,1000)
# now performing matplotlib logic to generate the graph

#including data points

plt.scatter(*zip(*result))
plt.plot(*zip(*result))
plt.title("probability of success via DFS vs blocking factor (on maze of size 1000)")
plt.xlabel("blocking factor")
plt.ylabel("probability of success (from 1000 trials) ")
plt.xticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.yticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.grid()
plt.show()
