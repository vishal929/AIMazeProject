from MazeVisualization import GUIDriver
from Preliminaries import mazeGenerator
# driver will take care of our user interface
# a bunch of questions will be asked:
    # 0) do you want GUI display or not?
    # 1) enter dim for maze
    # 2) enter blocking factor
    # 3) do you want fire or not?
        # if so:
            # 4) enter the flammability rate
            # 5) choose a strategy
            # 6) Ask if they only want final result or gradual showing of fire spread?
        # if not:
            # do you want bfs or A star or dfs to find a path?



#functions below to gather data from user input
# returns 0 for no GUI or 1 for GUI, valueError if user doesnt input y or n
def askForGUI():
    while True:
        try:
            user =input("Do you want a GUI for output? (Y/N)")
            user=user.lower()
            if user=="y":
                return 1
            elif user=="n":
                return 0
            else:
                raise ValueError("Must answer with Y/N!")
        except ValueError as inst:
           print(inst)

# returns users input of dimension of maze, if invalid raises valueError
def askDim():
    while True:
        try:
            user =input("Please enter a dimension for the square maze (i.e 2 or 3 and so on)")
            if not user.isdigit():
                raise ValueError("Must enter a valid natural number for the maze side!")
            user=int(user)
            if user<=1:
                raise ValueError("Must enter a size greater than 1 ! (or it wouldnt be much of a maze)")
            return user
        except ValueError as inst:
            print(inst)

# returns blocking factor or raises valueError if invalid entry
def askBlockingFactor():
    while True:
       try:
            user=input("Please enter a blocking factor from 0 to 1 (0 being no blocking, and 1 being every square is blocked)")
            try:
                user=float(user)
            except:
                raise ValueError("Please enter a value from 0 to 1!")
            return user
       except ValueError as inst:
           print(inst)

# returns result of if user wants fire or not
def askFire():
    while True:
        try:
            user = input("Would you like to simulate fire for the maze? (Y/N)")
            user = user.lower()
            if user == "y":
                return 1
            elif user == "n":
                return 0
            else:
                raise ValueError("Must answer with Y/N!")
        except ValueError as inst:
            print(inst)

# returns flammability rate or raises error
def askFlammabilityRate():
    while True:
        try:
            user = input("Please input the desired flammability rate from 0 to 1")
            try:
                user=float(user)
            except:
                raise ValueError("Please enter a value from 0 to 1!")
            if user<0 or user>1:
                raise ValueError("Please enter a value from 0 to 1 !")
            return user
        except ValueError as inst:
            print(inst)

#returns strategy or raises error
def askStrategy():
    while True:
        try:
            user = input("Enter 1 to use first strategy, 2 for second strategy, and 3 to use our custom strategy")
            try:
                user=int(user)
            except:
                # then user entered something invalid
                raise ValueError("Please enter a value from 1 to 3 which represents the strategy to use !")
            if user<1 or user>3:
                raise ValueError("Please enter a value from 1 to 3 which represents the strategy to use !")
            return user
        except ValueError as inst:
            print(inst)

# returns desired search pathway for non flame tests
def askNoFireSearch():
    while True:
        try:
            user = input("Enter 1 for dfs, 2 for bfs, and 3 for A* ")
            if not user.isdigit():
                raise ValueError("Please enter a value from 1 to 3 which represents the search to use!")
            user = int(user)
            if user<1 or user>3:
                raise ValueError("Please enter a value from 1 to 3 which represents the search to use!")
            return user
        except ValueError as inst:
            print(inst)


# ask if user wants to only see final result, or gradual showing and steps of fire in GUI
def askGradual():
    user = input("Would you like to see gradual results, or only the final result of the strategy? (Y/N)").lower()
    return user


# below code to drive our user interface
guiYesNo=askForGUI()
blockingFactor=askBlockingFactor()
dim=askDim()
fireYesNo=askFire()
if fireYesNo==1:
    flammabilityRate=askFlammabilityRate()
    strategy=askStrategy()
    gradual=askGradual()
    if guiYesNo==1:
        # GUI output
        if strategy==1:
            if gradual=="y":
                maze = GUIDriver.CanvasMaze(dim,blockingFactor,flammabilityRate)
                maze.showGradualStrategyOne()
            else:
                maze = GUIDriver.CanvasMaze(dim, blockingFactor, flammabilityRate)
                maze.showEntireStrategyOne()
        elif strategy==2:
            if gradual=="y":
                maze = GUIDriver.CanvasMaze(dim, blockingFactor, flammabilityRate)
                maze.showGradualStrategyTwo()
            else:
                maze = GUIDriver.CanvasMaze(dim, blockingFactor, flammabilityRate)
                maze.showEntireStrategyTwo()
        else:
            # our strategy
            if gradual=="y":
                pass
            else:
                pass
    else:
        # CLI output
        if strategy==1:
            maze = mazeGenerator.generateMaze(dim,blockingFactor)
            mazeGenerator.printStrategyOne(maze,flammabilityRate)
        elif strategy==2:
            maze = mazeGenerator.generateMaze(dim, blockingFactor)
            mazeGenerator.printStrategyTwo(maze, flammabilityRate)
        else:
            # our strategy
            pass
else:
    noFireStrategy = askNoFireSearch()
    if guiYesNo==1:
        if noFireStrategy==1:
            #dfs
            maze = GUIDriver.CanvasMaze(dim,blockingFactor,0)
            maze.showDFS()
        elif noFireStrategy==2:
            # bfs
            maze = GUIDriver.CanvasMaze(dim,blockingFactor,0)
            maze.showBFS()
        else:
            # A Star
            maze = GUIDriver.CanvasMaze(dim, blockingFactor, 0)
            maze.showAStar()
    else:
        # CLI output
        if noFireStrategy==1:
            maze=mazeGenerator.generateMaze(dim,blockingFactor)
            mazeGenerator.printedDFS(maze)
        elif noFireStrategy==2:
            maze = mazeGenerator.generateMaze(dim, blockingFactor)
            mazeGenerator.printedBFS(maze)
        else:
            maze = mazeGenerator.generateMaze(dim, blockingFactor)
            mazeGenerator.printedAStar(maze)

