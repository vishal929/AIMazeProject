import tkinter
# idea: first show matrix with obstacles/initial fire
# then, as moves are taken, fire grows and GUI is updated automatically
# if goal found, success text displayed, otherwise failure text

# widget to represent our maze, complete with dim label, obstacleDensity label, and fireRate label
class Maze(tkinter.Tk):
   # the maze itself is a grid of cells (cells are tkinter labels)
   def __init__(self, dim, maze, obstacleDensity, flammabilityRate):
      super().__init__()
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
            cell = tkinter.Label(self.mazeFrame,text=maze[i][j],borderwidth=2,relief="solid")
            cell.config(height=2,width=10)
            cell.grid(column=j,row=i)
      #adding labels to bottom of window
      obstacle=tkinter.Label(self.labelFrame,text="Obstacle Density:"+str(obstacleDensity))
      flame = tkinter.Label(self.labelFrame,text="Flammability Rate:"+str(flammabilityRate))
      obstacle.grid(row=0,column=1)
      flame.grid(row=0,column=0)
      self.update()
   def updateMaze(self):
      # method to just redraw the maze after every step
      self.update()


