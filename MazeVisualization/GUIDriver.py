#import for testing
from Preliminaries.mazeGenerator import generateMaze
from Preliminaries.DFS import dfs
#tkinter for simple GUI
import tkinter
# idea: first show matrix with obstacles/initial fire
# then, as moves are taken, fire grows and GUI is updated automatically
# if goal found, success text displayed, otherwise failure text

# widget to represent our maze, complete with dim label, obstacleDensity label, and fireRate label
class Maze(tkinter.Tk):
   # the maze itself is a grid of cells (cells are tkinter labels)
   def __init__(self,  maze, obstacleDensity, flammabilityRate):
      super().__init__()
      dim = len(maze)
      self.dim=dim
      self.maze=maze
      self.obstacleDensity=obstacleDensity
      self.flammabilityRate=flammabilityRate
      self.mazeFrame=tkinter.Frame(self)
      self.mazeFrame.grid(column=0,row=0)
      self.labelFrame=tkinter.Frame(self)
      self.labelFrame.grid(column=0,row=1)
      for i in range(dim):
         for j in range(dim):
            if maze[i][j]==1:
               cell=tkinter.Label(self.mazeFrame,bg="black",text=maze[i][j],borderwidth=2,relief="solid")
            elif maze[i][j]==-1:
               cell=tkinter.Label(self.mazeFrame,bg="red",text=maze[i][j],borderwidth=2,relief="solid")
            elif maze[i][j]==2:
               cell = tkinter.Label(self.mazeFrame, bg="blue", text=maze[i][j], borderwidth=2, relief="solid")
            else:
               cell = tkinter.Label(self.mazeFrame, bg="white", text=maze[i][j], borderwidth=2, relief="solid")
            cell.config(height=2,width=10)
            cell.grid(column=j,row=i)
      #adding labels to bottom of window
      obstacle=tkinter.Label(self.labelFrame,text="Obstacle Density:"+str(obstacleDensity))
      flame = tkinter.Label(self.labelFrame,text="Flammability Rate:"+str(flammabilityRate))
      obstacle.grid(row=0,column=1)
      flame.grid(row=0,column=0)
      self.mainloop()
   def updateMaze(self):
      # method to just redraw the maze after every step
      self.update()

# test for now
testMaze= generateMaze(10, 0.3)
hi = Maze(testMaze,0.3,0)

print(dfs(testMaze,(0,0),(9,9)))