from queue import PriorityQueue
from Preliminaries import mazeGenerator, AStar
from collections import deque
# importing copy for an alternate strategy
import copy

from Preliminaries.AStar import getEuclideanDistance


def ourStrategy(maze,flammabilityRate):
    # agents starts at (0,0)
    # fire is at random position at start
    agentPos=(0,0)
    maze[agentPos[0]][agentPos[1]]=2
    initialFire = mazeGenerator.initializeFire(maze)
    firePlaces=PriorityQueue()
    firePlaces.put(0,initialFire)
    fringe = PriorityQueue()
    closed=set()
    #putting agents initial position
    fringe.put((0,(0,0)))

    while fringe:
        item = fringe.get()
        if item[1]==(len(maze)-1,len(maze)-1):
            # then we reached our goal
            maze[agentPos[0]][agentPos[1]]=0
            agentPos=(len(maze)-1,len(maze)-1)
            maze[agentPos[0]][agentPos[1]] = 2
            return True
        #adding neighbors
        neighbors=[(0,(item[1][0],item[1][1]+1)),(0,(item[1][0]+1,item[1][1])),(0,(item[1][0],item[1][1]-1)),(0,(item[1][0]-1,item[1][1]))]
        lowestHeuristicNeighbor=None
        for neighbor in neighbors:
            if neighbor not in closed and neighbor[0]<len(maze) and neighbor[1]<len(maze) and neighbor[0]>=0 and neighbor[1]>=0:
                neighbor[0]=getHeuristic(neighbor[1],(len(maze)-1,len(maze)-1),firePlaces.get(),maze)
                if lowestHeuristicNeighbor==None:
                    lowestHeuristicNeighbor=neighbor[1]
                elif lowestHeuristicNeighbor[0]>neighbor[0]:
                    lowestHeuristicNeighbor=neighbor[1]
        # now we have neighbor with lowest heuristic
        # now we choose lowest neighbor and we do fire step

        #choosing the neighbor is just changing agent pos
        maze[agentPos[0]][agentPos[1]]=0
        agentPos=lowestHeuristicNeighbor[1]
        maze[agentPos[0]][agentPos[1]] =2

        #adding last item to closed set
        closed.add(item)

        #increment fire
        litSpots=mazeGenerator.lightMaze(maze,flammabilityRate)
        temp=PriorityQueue()
        while firePlaces:
            item = firePlaces.get()
            item[0]+=1
            temp.put(item)
        for spot in litSpots:
            temp.put((0,spot))
        firePlaces=temp
        # now old spots increased in priority in queue to push them further back
        # new spots start with priority 0
    if maze[agentPos[0]][agentPos[1]]==-1:
        return False
    # determine other way to express we were blocked vs going into fire



    #loc1 is tested cell,
    #loc2 is goal
    #loc3 is closest fire position
def getHeuristic(loc1,loc2,loc3,maze):
    dim = len(maze)
    euclidean = getEuclideanDistance(loc1,loc2)
    distFire = getEuclideanDistance(loc1,loc3)
    blockingFactorSum=0
    # checking if the location is blocked on several sides or not
    neighbors = [(loc1[0], loc1[1] + 1), (loc1[0] + 1, loc1[1]), (loc1[0], loc1[1] - 1), (loc1[0] - 1, loc1[1])]
    for neighbor in neighbors:
        if neighbor[0]<dim and neighbor>=0 and neighbor[1]<dim and neighbor>=0:
            if maze[neighbor[0]][neighbor[1]]==1:
               blockingFactorSum+=1
    return euclidean+distFire+blockingFactorSum

# alternate strategy for beating the fire (taking into account probability of a cell getting on fire)
# idea, i use A star heuristic on neighbors and I also take into account the probability of each cell getting on fire
def ourAlternateStrategy(maze,flammabilityRate):
    dim = len(maze)
    # fringe is a priority queue
    fringe = PriorityQueue()
    fringe.put((0,(0,0)))
    currAgentLoc=None
    while not fringe.empty():
        item = (fringe.get())[1]
        # moving agent
        maze[item[0]][item[1]]=2
        currAgentLoc=item
        # advancing fire
        if item==(0,0):
            # initializing fire
            mazeGenerator.initializeFire(maze)
        else:
            # spreading fire
            litSpots = mazeGenerator.lightMaze(maze,flammabilityRate)
            if item in litSpots:
                # then agent has burned up
                return False
        # getting neighbors
        neighbors = [(item[0] + 1, item[1]), (item[0] - 1, item[1]), (item[0], item[1] + 1), (item[0], item[1] - 1)]
        for neighbor in neighbors:
            if neighbor[0] < len(maze) and neighbor[0] >= 0 and neighbor[1] < len(maze) and neighbor[1] >= 0:
                if maze[neighbor[0]][neighbor[1]]!=-1 and maze[neighbor[0]][neighbor[1]]!=1:
                    # adding to priority queue
                    fringe.put((getAlternateHeuristic(maze,flammabilityRate,neighbor),neighbor))
    # checking if we reached the end
    if currAgentLoc==(len(maze)-1,len(maze)-1):
        return True
    else:
        return False


# idea, A star heuristic, but I also add the probability of this space getting on fire
# future idea: could implement a tolerance for probability
def getAlternateHeuristic(maze, flammabilityRate, locToTest):
    neighborsOnFire=0
    neighbors = [(locToTest[0] + 1, locToTest[1]), (locToTest[0] - 1, locToTest[1]), (locToTest[0], locToTest[1] + 1), (locToTest[0], locToTest[1] - 1)]
    for neighbor in neighbors:
        if neighbor[0]<len(maze) and neighbor[0]>=0 and neighbor[1]<len(maze) and neighbor[1]>=0:
            if maze[neighbor[0]][neighbor[1]]==-1:
                neighborsOnFire +=1
    probOfFire = 1-((1-flammabilityRate)**neighborsOnFire)
    euclideanDistance = getEuclideanDistance(locToTest,(len(maze)-1,len(maze)-1))
    return probOfFire+euclideanDistance

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

# test
hi = mazeGenerator.generateMaze(100,0.3)
print(evenMoreAlternateStrategy(hi,0.1,0.2,50))

