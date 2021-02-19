# code implementation of strategy 2
# recalculating bfs at each step
from Preliminaries import mazeGenerator, DFS, BFS, AStar

def doStrategyTwo(maze,flammabilityRate):
   # initialize random starting point for fire
   # mazeGenerator.initializeFire(maze)
   currPosition = (0,0)

   while True:
      #first spot is the start, so we pick the next one
      path = AStar.aStarGetPath(maze, currPosition, (len(maze)-1,len(maze)-1))
      if len(path) > 1:
         posToPick = path[1]
      else:
         return currPosition
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
         currPosition = posToPick
         maze[currPosition[0]][currPosition[1]]=2
         mazeGenerator.lightMaze(maze,flammabilityRate)
         # checking if the spot is on fire now
         if maze[currPosition[0]][currPosition[1]]==-1:
            # returning the position because the agent will burn
            return currPosition


# returns a list of tuples corresponding to each obstacle density incremented by 0.05
# sample size is the number of times to run the test for each blocking density
# dim is the dimension of the maze to use for probability helper
def strategyTwoProbabilityHelper(dim,sampleSize):
    #inputOutput is our list of tuples
    goal = (dim - 1, dim - 1)
    inputOutput=[]
    desiredDensity = 0.3
    currFlammability = 0.0
    while currFlammability <= 1:
        strategyTwoSuccessCount = 0
        for i in range(sampleSize):
            
            # generating maze
            maze = mazeGenerator.generateMaze(dim, desiredDensity)
            fireLoc = mazeGenerator.initializeFire(maze)
            # Generate mazes and fire until there is a path from agent to goal and from agent to the fire
            while not (DFS.dfs(maze, (0,0), goal) and DFS.dfs(maze, (0,0), fireLoc)):
                maze = mazeGenerator.generateMaze(dim, desiredDensity)
                fireLoc = mazeGenerator.initializeFire(maze)
            print("fire: ", fireLoc)
            endingLoc = doStrategyTwo(maze, currFlammability)
            print("Loc: ", endingLoc)
            if endingLoc == goal:
                strategyTwoSuccessCount += 1
                print("success")
            print("fin trial", i+1)
        print("flammability:", currFlammability)
        # now we have the probability for this flammability
        probability = strategyTwoSuccessCount/sampleSize
        inputOutput.append((currFlammability,probability))
        currFlammability = round(currFlammability + 0.05, 2)
    # returning our list of tuples to use with mathplotlib for plotting a graph

    return inputOutput
