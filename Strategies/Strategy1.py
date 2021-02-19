# code implementation of strategy 1
from Preliminaries import AStar
from Preliminaries import mazeGenerator
# very simple algo: just use A* to get a path and then move agent along the path while incrementing fire
# fire generation included in algo

# returns position died in
def doStrategyOne(maze,flammabilityRate):
    mazeGenerator.initializeFire(maze)
    # path given by A*
    path = AStar.aStarGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))

    for step in path:
        # first step logic
        if step[0]==0 and step[1]==0:
            # then we just move the agent and continue
            maze[step[0]][step[1]] = 2
            continue
        # we just move agent and then increment the fire
        # because we used bfs, we cannot possibly hit an obstacle, but we might hit fire and die
        if maze[step[0]][step[1]]==-1:
            # return the failed pos
            return step
        else:
            # then we move the agent and increment the fire
            maze[step[0]][step[1]]=2
            if step == (len(maze)-1,len(maze)-1):
                # agent Survived!
                break
            mazeGenerator.lightMaze(maze,flammabilityRate)
            # checking if fire is on the step we just moved to
            if maze[step[0]][step[1]]==-1:
                return step
    # if we reached the end we can just return the last point
    return (len(maze)-1,len(maze)-1)

# gradual printing of strategy 1 on a maze on fire
def printStrategyOneStep(maze, flammabilityRate, path):
    if path is None:
        mazeGenerator.initializeFire(maze)
        path =AStar.aStarGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
        locToMove = path.popleft()
        maze[locToMove[0]][locToMove[1]]=2
        return True,path
    else:
        locToMove=path.popleft()
        if maze[locToMove[0]][locToMove[1]]==-1:
            # agent burns
            return False,path
        # moving agent
        maze[locToMove[0]][locToMove[1]]=2
        # generating fire
        litSpots=mazeGenerator.lightMaze(maze,flammabilityRate);
        if locToMove in litSpots:
            # agent burned up
            return False,path
        if locToMove ==(len(maze)-1,len(maze)-1):
            return False,path
        else:
            return True,path


def printStrategyOne(maze,flammabilityRate):
    path=None
    while True:
        result = printStrategyOneStep(maze,flammabilityRate,path)
        path=result[1]
        mazeGenerator.printMaze(maze)
        if not result[0]:
            break
    # printing final state
    mazeGenerator.printMaze(maze)

def printEntireStrategyOne(maze,flammabilityRate):
    doStrategyOne(maze,flammabilityRate)
    mazeGenerator.printMaze(maze)