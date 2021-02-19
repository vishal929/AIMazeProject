
# Additional data structure for path
from collections import deque

# Data structure for A* fringe
import heapq
import math

# Method to find path from loc1 to loc2 using A*
# returns true if loc2 is reachable from loc1, false otherwise
from Preliminaries import mazeGenerator

# Method to find path from loc1 to loc2 using A*
# returns true if loc2 is reachable from loc1, false otherwise
def aStar(maze, loc1, loc2):
    dim = len(maze)
    if loc1 == loc2:
        return True
    # Data structure for fringe
    fringe = []
    lookup ={}
    # Fringe stored as tuples in the form (distance from loc1 to loc2, ((loc1 x, loc1 y),distanceFromParent))
    heapq.heappush(fringe, (0,(loc1,0)))
    # closed set implemented as python collection set
    closed = set()
    # helping to determine when to push to fringe or not
    lastDistance={}
    while fringe:
        tup = heapq.heappop(fringe)
        item = tup[1][0]
        if item in closed:
            continue
        # checking if item is loc2
        if item == loc2:
            return True

        # adding neighbors to fringe if they arent in closed set and if they arent blocked (cell value of 1)
        # 4 neighbors for each cell
        neighbors = []
        neighbors.append((item[0] - 1, item[1]))  #cell left
        neighbors.append((item[0], item[1] - 1))  #cell up
        neighbors.append((item[0] + 1, item[1]))  #cell right
        neighbors.append((item[0], item[1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]] != 1 and maze[neighbor[0]][neighbor[1]]!=-1:
                        lastDistance[neighbor]=tup[1][1]+1
                        # updating distance of nodes
                        heapq.heappush(fringe,(getHeuristic(neighbor, loc2)+((tup[1])[1])+1, (neighbor,tup[1][1]+1)))
        closed.add(item)
    return False


# method to get an actual path from A* (uses parent structure, i.e a dictionary that holds each parent for traceback)
# returns a deque structure which is the path found from loc1 to loc2
def aStarGetPath(maze, loc1, loc2):
    parents={}
    dim = len(maze)
    if loc1 == loc2:
        return True
    # Data structure for fringe
    fringe = []
    # Fringe stored as tuples in the form (distance from loc1 to loc2, ((loc1 x, loc1 y),distanceFromParent))
    heapq.heappush(fringe, (0,(loc1,0)) )
    # closed set implemented as python collection set
    closed = set()
    lastDistance={}
    while fringe:
        tup = heapq.heappop(fringe)
        item = tup[1][0]
        if item in closed:
            continue
        # checking if item is loc2
        if item == loc2:
            break

        # adding neighbors to fringe if they arent in closed set and if they arent blocked (cell value of 1)
        # 4 neighbors for each cell
        neighbors = []
        neighbors.append((item[0] - 1, item[1]))  #cell left
        neighbors.append((item[0], item[1] - 1))  #cell up
        neighbors.append((item[0] + 1, item[1]))  #cell right
        neighbors.append((item[0], item[1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]] != 1 and maze[neighbor[0]][neighbor[1]]!=-1:
                    if neighbor in lastDistance:
                        if lastDistance[neighbor]<tup[1][1]+1:
                            # we found some better path
                            continue
                    lastDistance[neighbor]=tup[1][1]+1
                    # updating distance of nodes
                    heapq.heappush(fringe,(getHeuristic(neighbor, loc2)+((tup[1])[1])+1, (neighbor,tup[1][1]+1)))
                    # updating parent
                    if (neighbor != loc1):
                        parents[neighbor] = item
        closed.add(item)
    # logic for returning a path
    # going through traceback from (item)
    traced = loc2
    path = deque()
    while traced in parents:
        path.appendleft(traced)
        traced = parents[traced]
    # last item is starting point
    path.appendleft(traced)
    return path

# Method for returning the heuristic between loc1 and loc2
# Alternative heuristics can be added later if desired (ex. manhattan distance)
def getHeuristic(loc1, loc2):
    heuristic = getEuclideanDistance(loc1, loc2)
    return heuristic

# Calcualted the Euclidean (straight line) distance between loc1 and loc2
def getEuclideanDistance(loc1, loc2):
    return math.sqrt( ((loc2[0] - loc1[0]) ** 2) + ((loc2[1] - loc1[1]) ** 2))


# returns a list of tuples corresponding to each obstacle density incremented by 0.05
# sample size is the number of times to run the test for each blocking density
# dim is the dimension of the maze to use for probability helper
def aStarProbabilityHelper(dim,sampleSize):
    # idea just generate maze sampleSize times per blocking factor, do A* from (0,0) to (dim-1,dim-1)
    # count average number of nodes explored
    # keep incrementing obstacle density by 0.05 and we will eventually have a pretty cool graph
    #inputOutput is our list of tuples
    inputOutput=[]
    currDensity = 0.0
    while currDensity <= 1:
        aStarStepCountAverage = 0.0
        for i in range(sampleSize):
            nodesExplored = 0
            # generating maze
            maze = mazeGenerator.generateMaze(dim, currDensity)

            nodesExplored = aStarGetNodesExplored(maze, (0,0), (dim - 1, dim - 1))
            aStarStepCountAverage += nodesExplored

            print("Steps: ", nodesExplored)
            print("trial end: ", i)
        # now we have the steps taken for this obstacle density
        aStarStepCountAverage = aStarStepCountAverage / sampleSize
        inputOutput.append((currDensity, aStarStepCountAverage))
        currDensity = round(currDensity + 0.05, 2)
        print("density: ", currDensity)
    # returning our list of tuples to use with mathplotlib for plotting a graph

    return inputOutput


# Method to find nodes explored when doing A* between loc1 and loc2
# returns number of nodes explored in an attempt to find a solution
# loc1 and loc2 are tuples of form (row,column)
def aStarGetNodesExplored(maze, loc1, loc2):
    nodesExplored = 0
    dim = len(maze)
    if loc1 == loc2:
        return nodesExplored
    # Data structure for fringe
    fringe = []
    lookup ={}
    # Fringe stored as tuples in the form (distance from loc1 to loc2, ((loc1 x, loc1 y),distanceFromParent))
    heapq.heappush(fringe, (0,(loc1,0)))
    # closed set implemented as python collection set
    closed = set()
    # helping to determine when to push to fringe or not
    lastDistance={}
    while fringe:
        tup = heapq.heappop(fringe)
        nodesExplored += 1
        item = tup[1][0]
        if item in closed:
            continue
        # checking if item is loc2
        if item == loc2:
            return nodesExplored

        # adding neighbors to fringe if they arent in closed set and if they arent blocked (cell value of 1)
        # 4 neighbors for each cell
        neighbors = []
        neighbors.append((item[0] - 1, item[1]))  #cell left
        neighbors.append((item[0], item[1] - 1))  #cell up
        neighbors.append((item[0] + 1, item[1]))  #cell right
        neighbors.append((item[0], item[1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]] != 1 and maze[neighbor[0]][neighbor[1]]!=-1:
                        lastDistance[neighbor]=tup[1][1]+1
                        # updating distance of nodes
                        heapq.heappush(fringe,(getHeuristic(neighbor, loc2)+((tup[1])[1])+1, (neighbor,tup[1][1]+1)))
        closed.add(item)
    return nodesExplored

# showing A* on a maze
def printedAStar(maze):
    path =aStarGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
    for loc in path:
        # marking agents path
        maze[loc[0]][loc[1]]=2
    mazeGenerator.printMaze(maze)
