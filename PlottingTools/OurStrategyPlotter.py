# this serves as a driver to generate a plot for our strategy using matplotlib

# calls my dfs probability helper function and uses it to generate a plot

from Strategies import OurStrategy

import matplotlib.pyplot as plt



result = OurStrategy.ourStrategyProbabilityHelper(100, 20)
# now performing matplotlib logic to generate the graph

#including data points

plt.scatter(*zip(*result))
plt.plot(*zip(*result))
plt.title("probability of success via ourStrategy (0.2 tolerance) vs flammabilityRate (on maze of size 100)")
plt.xlabel("flammability rate")
plt.ylabel("probability of success (from 20 trials at each 0.05 increment in flammability rate) ")
plt.xticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.yticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.grid()
plt.show()
