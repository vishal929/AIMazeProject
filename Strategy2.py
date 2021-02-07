# code implementation of strategy 2
# recalculating bfs at each step
from Preliminaries import mazeGenerator, AStar
from Preliminaries import BFS

def doStrategyTwo(maze,flammabilityRate):
   # initialize random starting point for fire
   mazeGenerator.initializeFire(maze)
   currPosition=(0,0)


   while True:
      #first spot is the start, so we pick the next one
      posToPick=AStar.aStarGetPath(maze,currPosition,(len(maze)-1,len(maze)-1))[1]

      #checking goal status
      if posToPick==(len(maze)-1,len(maze)-1):
         # then the agent has found his way to the goal
         maze[posToPick[0]][posToPick[1]]=2
         return posToPick

      if maze[posToPick[0]][posToPick[1]]==-1:
         # return this pos because the agent will burn here
         return posToPick
      else:
         # then we move agent here and advance fire
         currPosition=posToPick
         maze[currPosition[0]][currPosition[1]]=2
         mazeGenerator.lightMaze(maze,flammabilityRate)
         # checking if the spot is on fire now
         if maze[currPosition[0]][currPosition[1]]==-1:
            # returning the position because the agent will burn
            return currPosition


