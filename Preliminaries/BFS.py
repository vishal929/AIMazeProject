# Data structure for BFS fringe
from queue import Queue
# Additional data structure for path
from collections import deque

# Method to find a path between loc1 and loc2
# returns true if loc2 is reachable from loc1, false otherwise
# loc1 and loc2 are tuples of form (row,column)
from Preliminaries import mazeGenerator


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
                        if neighbor!=(0,0):
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
    print("REACHED HERE")
    path.appendleft(traced)
    return path

# showing bfs on a maze
def printedBFS(maze):
    path =bfsGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
    for loc in path:
        # marking agents path
        maze[loc[0]][loc[1]]=2
    mazeGenerator.printMaze(maze)