# Data structure for BFS fringe
from queue import Queue
# Additional data structure for path
from collections import deque

from Preliminaries import mazeGenerator


# Method to find a path between loc1 and loc2
# returns true if loc2 is reachable from loc1, false otherwise
# loc1 and loc2 are tuples of form (row,column)
def bfs(maze, loc1, loc2):
    dim = len(maze)
    if loc1 == loc2:
        return True
    # Data structure for fringe
    fringe = Queue()
    fringe.put(loc1)
    # closed set implemented as python collection set
    closed = set()
    while not fringe.empty():
        item = fringe.get()
        if item in closed:
            continue
        # checking if item is loc2
        if item == loc2:
            return True
        # adding neighbors to fringe if they arent in closed set and if they arent blocked
        # 4 neighbors for each cell
        neighbors = []
        neighbors.append((item[0] - 1, item[1]))  #cell left
        neighbors.append((item[0], item[1] - 1))  #cell up
        neighbors.append((item[0] + 1, item[1]))  #cell right
        neighbors.append((item[0], item[1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]] != 1:
                        fringe.put(neighbor)
        closed.add(item)
    return False

# method to get an actual path from bfs (uses parent structure, i.e a dictionary that holds each parent for traceback)
# returns a deque structure which is the path found from loc1 to loc2
def bfsGetPath(maze,loc1,loc2):
    # dictionary to keep source->parent pairs will help when going back
    parents={}
    dim = len(maze)
    # Data structure for fringe
    fringe = Queue()
    fringe.put(loc1)
    # closed set implemented as python collection set
    closed = set()
    while not fringe.empty():
        item = fringe.get()
        if item in closed:
            continue

        # checking if item is loc2
        if item == loc2:
            break
        # adding neighbors to fringe if they arent in closed set and if they arent blocked
        # 4 neighbors for each cell
        neighbors = []

        neighbors.append((item[0] - 1, item[1]))  #cell left
        neighbors.append((item[0], item[1] - 1))  #cell up
        neighbors.append((item[0] + 1, item[1]))  #cell right
        neighbors.append((item[0], item[1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]] != 1 and maze[neighbor[0]][neighbor[1]]!=-1:
                    if neighbor not in parents:
                        fringe.put(neighbor)
                        # then this neighbor wasnt even visited yet
                        # updating parent
                        if neighbor != loc1:
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
# sample size is the number of times to run the test for each blocking density
# dim is the dimension of the maze to use for probability helper
def bfsProbabilityHelper(dim,sampleSize):
    # idea just generate maze sampleSize times per blocking factor, do bfs from (0,0) to (dim-1,dim-1)
    # count average number of nodes explored
    # keep incrementing obstacle density by 0.05 and we will eventually have a pretty cool graph
    #inputOutput is our list of tuples
    inputOutput=[]
    currDensity = 0.0
    while currDensity <= 1:
        bfsStepCountAverage = 0.0
        for i in range(sampleSize):
            nodesExplored = 0
            # generating maze
            maze = mazeGenerator.generateMaze(dim, currDensity)
            # checking dfs
            nodesExplored = bfsGetNodesExplored(maze, (0,0), (dim - 1, dim - 1))
            bfsStepCountAverage += nodesExplored

            print("Steps: ", nodesExplored)
            print("trial end: ", i)
        # now we have the steps taken for this obstacle density
        bfsStepCountAverage = bfsStepCountAverage / sampleSize
        inputOutput.append((currDensity, bfsStepCountAverage))
        currDensity = round(currDensity + 0.05, 2)
        print("density: ", currDensity)
    # returning our list of tuples to use with mathplotlib for plotting a graph

    return inputOutput


# Method to find nodes explored when doing BFS between loc1 and loc2
# returns number of nodes explored in an attempt to find a solution
# loc1 and loc2 are tuples of form (row,column)
def bfsGetNodesExplored(maze, loc1, loc2):
    nodesExplored = 0
    dim = len(maze)
    if loc1 == loc2:
        return True
    # Data structure for fringe
    fringe = Queue()
    fringe.put(loc1)
    # closed set implemented as python collection set
    closed = set()
    while not fringe.empty():
        item = fringe.get()
        nodesExplored += 1
        if item in closed:
            continue
        # checking if item is loc2
        if item == loc2:
            return nodesExplored
        # adding neighbors to fringe if they arent in closed set and if they arent blocked
        # 4 neighbors for each cell
        neighbors = []
        neighbors.append((item[0] - 1, item[1]))  #cell left
        neighbors.append((item[0], item[1] - 1))  #cell up
        neighbors.append((item[0] + 1, item[1]))  #cell right
        neighbors.append((item[0], item[1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]] != 1:
                        fringe.put(neighbor)
        closed.add(item)
    
    return nodesExplored
