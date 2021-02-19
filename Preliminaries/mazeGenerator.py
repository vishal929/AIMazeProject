# mazeGenerator.py includes functions directly related to the maze
# need random number generator for obstacleDensity
from random import random
from random import randint

# grid is just list of ints, if 0 then the grid is free, if 1 then its blocked, if -1 then it is on fire
#if the entry is 2, then the agent is present


# just populates a maze based on dimension and obstacleDensity
# if dim<2 then exception raised
# obstacleDensity is a probability from 0 to 1, if anything else inputted, then exception is raised


def generateMaze(dim, obstacleDensity):
    if dim<2:
        raise ValueError("Dimension cannot be less than 2!")
    if obstacleDensity<0 or obstacleDensity>1:
        raise ValueError("Blocking factor must be a probability from 0 to 1!")
    # so far we passed checks, so generating list
    maze=[]
    for i in range(dim):
        toAdd=[]
        for j in range(dim):
            if i==0 and j==0:
                # top left corner is the start
                toAdd.append(0)
            elif i==dim-1 and j==dim-1:
                # bottom right corner is the end
                toAdd.append(0)
            else:
                # generating random number for obstacleDensity probability
                randomNumber = random()
                if randomNumber<obstacleDensity:
                    # then this is an obstacle entry
                    toAdd.append(1)
                else:
                    # then this is a free entry
                    toAdd.append(0)
        # appending the row list to the maze
        maze.append(toAdd)
    return maze

# method below for initializing fire in the maze
def initializeFire(maze):
    dim = len(maze)
    row = randint(0,dim-1)
    col = randint(0,dim-1)
    # randomly chosen position above will be the starting point for the fire
    if row==len(maze)-1 and col==len(maze)-1:
       # then i just pick the position above it
       row=row-1
       maze[row][col]=-1
    elif row==0 and col==0:
        # then I pick the position to the right
        col=col+1
        maze[row][col]=-1
    else:
        maze[row][col]=-1
    return (row,col)



# method below for performing fire generation given flammability rate
def lightMaze(maze,flammabilityRate):
    newFireSpots=[]
    dim = len(maze)
    if flammabilityRate<0 or flammabilityRate>1:
        raise ValueError("Flammability rate must be between 0 and 1 (inclusive)!")
   # iterating and adjusting fire
    for i in range(dim):
        for j in range(dim):
            if maze[i][j]!=1 and maze[i][j]!=-1:
                # then I need to check neighbors
                neighbors = []
                numFire=0
                neighbors.append((i+1, j))
                neighbors.append((i-1, j))
                neighbors.append((i, j+1))
                neighbors.append((i, j-1))
                for neighbor in neighbors:
                    if neighbor[0]<dim and neighbor[0]>=0 and neighbor[1]<dim and neighbor[1]>=0:
                        # then this is valid neighbor to check
                        if maze[neighbor[0]][neighbor[1]]==-1:
                            numFire += 1
                probFire = 1-((1-flammabilityRate)**numFire)
                if random()<probFire:
                    # then now this cell is on fire
                    newFireSpots.append((i,j))
    # after counting all the new fire spots, we set them
    for toLight in newFireSpots:
       maze[toLight[0]][toLight[1]]=-1
    return newFireSpots

# prints the maze to stdout
# O=open/free, F=fire, B=blocked, A=agent
def printMaze(maze):
    dim = len(maze)
    for i in range(dim):
        for j in range(dim):
            print("|",end="")
            if maze[i][j]==0:
                # o for open
                print("0",end="")
            elif maze[i][j]==-1:
                # f for fire
                print("\u001b[31m"+"F"+"\033[0m",end="")
            elif maze[i][j]==2:
                #A for agent
                print("\u001b[34m"+ "A"+"\033[0m",end="")
            else:
                # b for blocked
                print("\u001b[32m"+"B"+"\033[0m",end="")
            print("|",end="")
        print("")
    for i in range(dim):
        print("---",end="")
    print("")
