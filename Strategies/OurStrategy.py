from Preliminaries import mazeGenerator, AStar
# importing copy for an alternate strategy
import copy

# idea: first generate a path with AStar
# then, count the number of steps in the path
# simulate the fire spread several times
# count the probability of any square catching on fire in the path
# if the probability passes a certain tolerance, we remove the square from the path and calculate again
    # keep track of the path with the lowest probabilities of catching on fire
# if no path can be found where probability of any square in the path catching on fire is under the tolerance level
    # then we traverse the path we stored above with lowest probabilities and wish for the best
def evenMoreAlternateStrategy(maze,flammabilityRate,tolerance,numTrials):
    pathSatisfiesTolerance=False
    bestPathSoFar=None
    # stats below is organized as: (# of squares that have nonzero probability to ignite, totalSumOfProbability)
    bestPathSoFarStats=None
    # closed set for removing nodes that exceed our level of tolerance
    closedSet = set()
    # for each node in the closed set, we just simulate it as an obstacle so AStar avoids it
    # at the end, we just revert these spaces back to free spaces
    mazeGenerator.initializeFire(maze)
    while not pathSatisfiesTolerance:
        # setting to true, will be set to false later if the generated path doesnt satisfy the constraints
        # adjusting based on closed set
        for loc in closedSet:
            # simulating blocking to tell AStar not to generate path through here
            maze[loc[0]][loc[1]]=1
        path = AStar.aStarGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
        # NEED TO CHECK IF A VALID PATH IS RETURNED OR NOT
        if len(path)==1:
            # then only the goal is in the backtrack
            break
        # initializing to all zeroes (will increment this and then divide by 100 for final probabilities)
        pathProbs = [0.0 for i in range(len(path))]
        # we do not count the start
        numSteps = len(path)-1
        # generating fire for this number of steps 100 times for getting probability
        for j in range(numTrials):
            copyMaze = copy.deepcopy(maze)
            for i in range(numSteps):
                # spreading fire
                litSpots = mazeGenerator.lightMaze(copyMaze,flammabilityRate)
                for i in range(len(path)):
                    if i!=0 and path[i] in litSpots:
                        # we shouldnt count the start
                        pathProbs[i] +=1
        # now we have all the sums --> converting to probabilities
        # if we find any probability that is greater than or equal to our tolerance, we can add it to a closed set and recalculate
        # number of nonzero probability spots
        numNonZeroProbability=0
        probabilitySum=0
        numViolated=0
        for i in range(len(path)):
            if i==0:
                continue
            if pathProbs[i]!=0:
                numNonZeroProbability+=1
                pathProbs[i]=pathProbs[i]/numTrials
                probabilitySum+=pathProbs[i]
                if pathProbs[i]>=tolerance:
                    # then we add this to our closed set for artificially setting the values to 1
                    closedSet.add(path[i])
                    numViolated+=1
        if numViolated>0:
            pathSatisfiesTolerance=False
        else:
            # then this path satisfies our requirements
            bestPathSoFar=path
            break
        # setting best path so far (best means least sum of probability of going on fire and least number of squares which have a chance to ignite)
        consideredTuple=(numNonZeroProbability,probabilitySum)
        if bestPathSoFar==None:
            bestPathSoFar=path
            bestPathSoFarStats=consideredTuple
        else:
            if consideredTuple[0]<bestPathSoFarStats[0] and consideredTuple[1]<bestPathSoFarStats[1]:
                # then this is the new best path to try
                bestPathSoFar=path
                bestPathSoFarStats=consideredTuple
    # now we have a path or not path, but regardless we should reset all the closed set "artificial values"
    for loc in closedSet:
        maze[loc[0]][loc[1]]=0
    # returning best path found, or None if no possible path
    return bestPathSoFar


# execution of our strategy
def doOurAlternateStrategy(maze,flammabilityRate,tolerance,numTrials):
   path = evenMoreAlternateStrategy(maze,flammabilityRate,tolerance,numTrials)
   if path is not None:
      # then we can do stuff
      mazeGenerator.initializeFire(maze)
      # path given by bfs
      bfsPath = AStar.aStarGetPath(maze, (0, 0), (len(maze) - 1, len(maze) - 1))

      for step in bfsPath:
          # first step logic
          if step[0] == 0 and step[1] == 0:
              # then we just move the agent and continue
              maze[step[0]][step[1]] = 2
              continue
          # we just move agent and then increment the fire
          # because we used bfs, we cannot possibly hit an obstacle, but we might hit fire and die
          if maze[step[0]][step[1]] == -1:
              # return the failed pos
              return step
          else:
              # then we move the agent and increment the fire
              maze[step[0]][step[1]] = 2
              if step == (len(maze) - 1, len(maze) - 1):
                  # agent Survived!
                  break
              mazeGenerator.lightMaze(maze, flammabilityRate)
              # checking if fire is on the step we just moved to
              if maze[step[0]][step[1]] == -1:
                  return step
      # if we reached the end we can just return the last point
      return (len(maze) - 1, len(maze) - 1)








def ourStrategyProbabilityHelper(dim,sampleSize):
    pass
    # idea just generate maze x times, do our strategy from flammability rate 0 to flammability rate 1
    # count number of successes and that is our probability
    # keep incrementing obstacle density by 0.05 and we will eventually have a pretty cool graph
    #inputOutput is our list of tuples
    inputOutput=[]
    # with blocking density of 0 we will always find a path from start to goal
    inputOutput.append((0,1))
    currFlammability = 0.05
    step=0
    while step<20:
        # rounding errors
        if currFlammability>1:
            currFlammability=1
        ourStratSuccessCount = 0
        print("Testing for Flammability:"+str(currFlammability))
        for i in range(sampleSize):
            print("On test:"+str(i))
            maze=None
            while True:
                # generating maze
                maze = mazeGenerator.generateMaze(dim, 0.3)
                # checking our strat for 50 fire generations
                path = evenMoreAlternateStrategy(maze,currFlammability,0.2,50)
                if path is None:
                    # then this is a dud, need to generate maze with some valid path
                    continue
                else:
                    break
            # checking if agent burns
            for j in range(len(path)):
                if j==0:
                    path.popleft()
                    maze[0][0]=2
                else:
                    loc=path.popleft()
                    if maze[loc[0]][loc[1]]!=-1 and loc==(len(maze)-1,len(maze)-1):
                        # success
                        maze[loc[0]][loc[1]]=2
                        ourStratSuccessCount+=1
                    else:
                        # checking for fire
                        if maze[loc[0]][loc[1]]==-1:
                            # failure
                            break
                        else:
                            # moving and then checking
                            maze[loc[0]][loc[1]]=2
                            mazeGenerator.lightMaze(maze,currFlammability)
                            if maze[loc[0]][loc[1]]==-1:
                                # failure
                                break
        # now we have the probability for this obstacle density
        probability = ourStratSuccessCount/sampleSize
        inputOutput.append((currFlammability,probability))
        currFlammability+=0.05
        step+=1
    # returning our list of tuples to use with mathplotlib for plotting a graph

    return inputOutput




# gradual printing of strategy 1 on a maze on fire
def printOurStrategyStep(maze, flammabilityRate, path):
    if path is None:
        path =evenMoreAlternateStrategy(maze,flammabilityRate,0.2,50)
        if path is None:
            # then no actual path was found
            return False
        locToMove = path.popleft()
        maze[locToMove[0]][locToMove[1]]=2
        return True
    else:
        locToMove=path.popleft()
        if maze[locToMove[0]][locToMove[1]]==-1:
            # agent burns
            return False
        # moving agent
        maze[locToMove[0]][locToMove[1]]=2
        # generating fire
        litSpots=mazeGenerator.lightMaze(maze,flammabilityRate);
        if locToMove in litSpots:
            # agent burned up
            return False
        if locToMove ==(len(maze)-1,len(maze)-1):
            return False
        else:
            return True

def printOurStrategy(maze,flammabilityRate):
    path = None
    while printOurStrategyStep(maze,flammabilityRate,path):
        mazeGenerator.printMaze(maze)
    mazeGenerator.printMaze(maze)


def printOurEntireStrategy(maze,flammabilityRate):
    path = None
    while printOurStrategyStep(maze, flammabilityRate, path):
        # just doing steps
        pass
    # final print
    mazeGenerator.printMaze(maze)
