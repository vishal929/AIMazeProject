# stack needed for dfs
from collections import deque
# maze generation needed for probability helper


# fringe is a stack for dfs
# returns true if loc2 is reachable from loc1, false otherwise
# loc1 and loc2 are tuples of form (row,column)
from Preliminaries import mazeGenerator


def dfs(maze, loc1, loc2):
    dim = len(maze)
    if loc1 == loc2:
        return True
    # stack for fringe
    fringe = deque()
    fringe.append(loc1)
    # closed set implemented as python collection set
    closed = set()
    while fringe:
        item = fringe.pop()

        # checking if item is loc2
        if item == loc2:
            return True
        # adding neighbors to fringe if they arent in closed set and if they arent blocked
        # 4 neighbors for each cell
        neighbors = []
        neighbors.append((item[0] - 1, item[1]))
        neighbors.append((item[0], item[1] - 1))
        neighbors.append((item[0] + 1, item[1]))
        neighbors.append((item[0], item[1] + 1))

        for neighbor in neighbors:
            if neighbor[0]<dim and neighbor[0]>=0 and neighbor[1]<dim and neighbor[1]>=0:
                if maze[neighbor[0]][neighbor[1]]!=1:
                    if neighbor not in closed:
                        fringe.append(neighbor)
        closed.add(item)
    return False



# method to get an actual path from dfs (uses parent structure, i.e a dictionary that holds each parent for traceback)
# returns a deque structure which is the path found from loc1 to loc2
def dfsGetPath(maze,loc1,loc2):
    # dictionary to keep source->parent pairs will help when going back
    parents={}
    # same logic for dfs below
    dim = len(maze)
    # stack for fringe
    fringe = deque()
    fringe.append(loc1)
    # closed set implemented as python collection set
    closed = set()
    while fringe:
        item = fringe.pop()
        # checking if item is loc2
        if item == loc2:
            break
        # adding neighbors to fringe if they arent in closed set and if they arent blocked
        # 4 neighbors for each cell
        neighbors = []

        neighbors.append((item[0] - 1, item[1]))
        neighbors.append((item[0], item[1] - 1))
        neighbors.append((item[0] + 1, item[1]))
        neighbors.append((item[0], item[1] + 1))
        for neighbor in neighbors:
            if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]] != 1:
                    if neighbor not in closed:
                        fringe.append(neighbor)
                        # updating parent
                        parents[neighbor]=item
        closed.add(item)
    # logic for returning a path
    # going through traceback from (item)
    traced=loc2
    path = deque()
    while traced in parents:
       path.appendleft(traced)
       traced=parents[traced]
    # last item is starting point
    path.appendleft(traced)
    return path



# returns a list of tuples corresponding to each obstacle density incremented by 0.05
# so far the best size for not painfully slow computation is size 1000
# sample size is the number of times to run the test for each blocking density
# dim is the dimension of the maze to use for probability helper
def dfsProbabilityHelper(dim,sampleSize):
    # idea just generate maze 100 times, do dfs from (0,0) to (dim-1,dim-1)
    # count number of successes and that is our probability
    # keep incrementing obstacle density by 0.05 and we will eventually have a pretty cool graph
    #inputOutput is our list of tuples
    inputOutput=[]
    # with blocking density of 0 we will always find a path from start to goal
    inputOutput.append((0,1))
    currDensity = 0.05
    while currDensity < 1:
        dfsSuccessCount = 0
        for i in range(sampleSize):
            # generating maze
            maze = mazeGenerator.generateMaze(dim, currDensity)
            # checking dfs
            if dfs(maze, (0, 0), (dim - 1, dim - 1)):
                dfsSuccessCount += 1
        # now we have the probability for this obstacle density
        probability = dfsSuccessCount/sampleSize
        inputOutput.append((currDensity,probability))
        currDensity+=0.05
    # returning our list of tuples to use with mathplotlib for plotting a graph

    #with blocking factor of 1, we will not be able to find any path from start to goal
    inputOutput.append((1,0))
    return inputOutput



