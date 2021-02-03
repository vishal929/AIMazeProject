from queue import PriorityQueue
from Preliminaries import mazeGenerator
from collections import deque

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