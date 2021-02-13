
# Additional data structure for path
from collections import deque

# Data structure for A* fringe
import heapq
import math

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
    heapq.heappush(fringe, (0,(loc1,0)))
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
                        lastDistance[neighbor]=tup[1][1]+1
                        # updating distance of nodes
                        heapq.heappush(fringe,(getHeuristic(neighbor, loc2)+((tup[1])[1])+1, (neighbor,tup[1][1]+1)))
                        # updating parent
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
# Alternative heuristics can be added later (ex. manhattan distance)
def getHeuristic(loc1, loc2):
    heuristic = getEuclideanDistance(loc1, loc2)
    return heuristic

# Calcualted the Euclidean (straight line) distance between loc1 and loc2
def getEuclideanDistance(loc1, loc2):
    return math.sqrt( ((loc2[0] - loc1[0]) ** 2) + ((loc2[1] - loc1[1]) ** 2))
