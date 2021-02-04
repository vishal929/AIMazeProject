# GUI versions of our algorithms for visualization
# GUI versions will definitely not run as fast, but will be better for visualization

# idea is to call step(), redraw GUI canvas, call step() and continue
from collections import deque

from Preliminaries import DFS, BFS, AStar, mazeGenerator

import OurStrategy

# this will just run our dfs get path method and go through the whole path
# this algo is FOR NO FIRE SITUATIONS!
# returns true if path finding was successful,false otherwise
def guiDFS(maze):
    path = DFS.dfsGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
    lastLoc=None
    for loc in path:
        lastLoc=loc
        # for shading path agent takes blue in the canvas
        maze[loc[0]][loc[1]]=2
    if lastLoc!=(0,0):
        return False
    return True

# same as above method, but with BFS instead (so this should be shortest path)
def guiBFS(maze):
    path=BFS.bfsGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
    lastLoc = None
    for loc in path:
        lastLoc = loc
        # for shading path agent takes blue in the canvas
        maze[loc[0]][loc[1]] = 2
    if lastLoc != (0, 0):
        return False
    return True


# flame generation strategies below adapted from other files for GUI use
# path of tuples is included here so that the agent can take a single step
    # path is a deque data structure in python for optimized popleft()
# true is returned if agent successfully moved and fire did not burn him
# false is returned if the agent is burned by the fire or if the agent reaches the end
# we move agent from first and then generate fire spread
# second part of tuple that is returned is agents current position
def guiStrategyOne(maze,flammabilityRate,path):
   if path==None:
       path=BFS.bfsGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
       # moving agent to start
       path.popleft()
       maze[0][0]=2
       # initializing fire
       mazeGenerator.initializeFire(maze)
       return (True,(0,0))
   if not path:
       # then we hit the end
       return False, (len(maze) - 1, len(maze) - 1)
   # checking where agent will move
   locToMove = path.popleft()
   if maze[locToMove[0]][locToMove[1]]==-1:
       # then the agent moved into fire
       return (False,(locToMove))
   else:
       # then we move agent and generate fire
       maze[locToMove[0]][locToMove[1]]=2
       fireSpots=mazeGenerator.lightMaze(maze,flammabilityRate)
       if locToMove in fireSpots:
           return (False,(locToMove))

# same step implementation as above, but with strategy 2 mentality
# i.e after each step we recalculate the shortest path
# ran with currLoc starting equal to NONE
def guiStrategyTwo(maze,flammabilityRate,currLoc):
    if currLoc==None:
        # starting the agent
        maze[0][0]=2
        # initializing fire
        mazeGenerator.initializeFire(maze)
        # returning bool,currLoc
        return (True,(0,0))
    # if currLoc is not none, we recalculate and pick first step
    locToMove = BFS.bfsGetPath(maze,currLoc,(len(maze)-1,len(maze)-1)).popleft()
    if maze[locToMove[0]][locToMove[1]]==-1:
        return (False,locToMove)
    else:
        # moving agent
        maze[locToMove[0]][locToMove[1]]=2
        # checking for fire after generation
        litSpots=mazeGenerator.lightMaze(maze,flammabilityRate)
        if locToMove in litSpots:
            return (False,locToMove)
    if locToMove == (len(maze)-1,len(maze)-1):
        # we are done now
        return (False,locToMove)
