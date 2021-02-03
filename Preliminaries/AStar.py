
# Data structure for A* fringe
from queue import PriorityQueue
# Additional data structure for path
from collections import deque

import math

# Method to find path from loc1 to loc2 using A*
# returns true if loc2 is reachable from loc1, false otherwise
def aStar(maze, loc1, loc2):
    dim = len(maze)
    if loc1 == loc2:
        return True
    # Data structure for fringe
    fringe = PriorityQueue()
    # Fringe stored as tuples in the form (distance from loc1 to loc2, (loc1 x, loc1 y))
    fringe.put((getHeuristic(loc1, loc2), loc1))
    # closed set implemented as python collection set
    closed = set()
    while fringe:
        item = fringe.get()
        # checking if item is loc2
        if item[1] == loc2:
            return True

        # adding neighbors to fringe if they arent in closed set and if they arent blocked (cell value of 1)
        # 4 neighbors for each cell
        neighbors = []
        neighbors.append((item[1][0] - 1, item[1][1]))  #cell left
        neighbors.append((item[1][0], item[1][1] - 1))  #cell up
        neighbors.append((item[1][0] + 1, item[1][1]))  #cell right
        neighbors.append((item[1][0], item[1][1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor not in closed:
                if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                    if maze[neighbor[0]][neighbor[1]] != 1:
                        fringe.put((getHeuristic(loc1, loc2), neighbor))
        closed.add(item[1])
    return False

# method to get an actual path from A* (uses parent structure, i.e a dictionary that holds each parent for traceback)
# returns a deque structure which is the path found from loc1 to loc2
def aStarGetPath(maze,loc1,loc2):
    # dictionary to keep source->parent pairs will help when going back
    parents={}
    dim = len(maze)
    # Data structure for fringe
    fringe = PriorityQueue()
    # Fringe stored as tuples in the form (distance to loc2 from loc1, (loc1 x, loc1 y))
    fringe.put((getHeuristic(loc1, loc2), loc1))
    # closed set implemented as python collection set
    closed = set()
    while fringe:
        item = fringe.get()
        # checking if item is loc2
        if item[1] == loc2:
            break
        # adding neighbors to fringe if they arent in closed set and if they arent blocked
        # 4 neighbors for each cell
        neighbors = []

        neighbors.append((item[1][0] - 1, item[1][1]))  #cell left
        neighbors.append((item[1][0], item[1][1] - 1))  #cell up
        neighbors.append((item[1][0] + 1, item[1][1]))  #cell right
        neighbors.append((item[1][0], item[1][1] + 1))  #cell down

        for neighbor in neighbors:
            if neighbor not in closed:
                if neighbor[0] < dim and neighbor[0] >= 0 and neighbor[1] < dim and neighbor[1] >= 0:
                    if maze[neighbor[0]][neighbor[1]] != 1:
                        fringe.put((getHeuristic(neighbor, loc2), neighbor))
                        # updating parent
                        parents[neighbor]=item[1]
        closed.add(item[1])
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

# Method for returning the heuristic between loc1 and loc2
# Alternative heuristics can be added later (ex. manhattan distance)
def getHeuristic(loc1, loc2):
    heuristic = getEuclideanDistance(loc1, loc2)
    return heuristic

# Calcualted the Euclidean (straight line) distance between loc1 and loc2
def getEuclideanDistance(loc1, loc2):
    return math.sqrt( (loc2[0] - loc1[0]) ** 2 + (loc2[1] - loc1[1]) ** 2)
