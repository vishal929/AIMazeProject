#import for testing
import Strategy1
import Strategy2
from Preliminaries.AStar import aStar
from Preliminaries.mazeGenerator import generateMaze
from Preliminaries   import BFS
from Preliminaries import DFS
from MazeVisualization import GUIAgentStep
#tkinter for simple GUI
import tkinter
# idea: first show matrix with obstacles/initial fire
# then, as moves are taken, fire grows and GUI is updated automatically
# if goal found, success text displayed, otherwise failure text

# widget to represent our maze, complete with dim label, obstacleDensity label, and fireRate label

class CanvasMaze(tkinter.Tk):
   # the maze itself is a grid of cells (cells are tkinter labels)
   def __init__(self,  dim, obstacleDensity, flammabilityRate):
      super().__init__()
      self.cellSize=30
      self.dim=dim
      self.maze=generateMaze(dim,obstacleDensity)
      self.width=self.cellSize*len(self.maze)
      self.height=self.cellSize*len(self.maze)
      self.obstacleDensity=obstacleDensity
      self.flammabilityRate=flammabilityRate
      self.mazeCanvas=ResizingCanvas(self,width=self.width,height=self.height,background="white")
      self.mazeCanvas.bind()
      self.mazeCanvas.pack(expand="yes")
      self.rectangles=[]
      # initializing rectangles
      for i in range(self.dim):
         x=i*self.cellSize
         rects=[]
         for j in range(self.dim):
            y=j*self.cellSize
            rec=self.mazeCanvas.create_rectangle(x, y, x + self.cellSize, y + self.cellSize, fill="white")
            rects.append(rec)
         self.rectangles.append(rects)
   # method to update canvas
   def updateDrawing(self):
      for i in range(self.dim):
         x=i*self.cellSize
         for j in range(self.dim):
            y=j*self.cellSize
            if self.maze[i][j]==1:
               self.mazeCanvas.itemconfig(self.rectangles[i][j],fill="black")
            elif self.maze[i][j]==-1:
               self.mazeCanvas.itemconfig(self.rectangles[i][j], fill="red")
            elif self.maze[i][j]==2:
               self.mazeCanvas.itemconfig(self.rectangles[i][j], fill="blue")
            else:
               self.mazeCanvas.itemconfig(self.rectangles[i][j], fill="white")
      self.mazeCanvas.addtag_all("all")
   # method to run dfs on our canvas
   def showDFS(self):
      GUIAgentStep.guiDFS(self.maze)
      self.updateDrawing()
      self.title("DFS on"+"Maze with obstacleDensity="+str(self.obstacleDensity)+" flameDensity="+str(self.flammabilityRate))
      self.mainloop()

   # method to run bfs on our canvas
   def showBFS(self):
      GUIAgentStep.guiBFS(self.maze)
      self.updateDrawing()
      self.title("BFS on" + "Maze with obstacleDensity=" + str(self.obstacleDensity) + " flameDensity=" + str(self.flammabilityRate))
      self.mainloop()

   # should be the same as BFS above, just could be faster due to pruning with euclidean distance
   def showAStar(self):
      GUIAgentStep.guiAStar(self.maze)
      self.updateDrawing()
      self.title("A* on" + "Maze with obstacleDensity=" + str(self.obstacleDensity) + " flameDensity=" + str(
         self.flammabilityRate))
      self.mainloop()
   # method to gradually show fire steps for strategy 1
   def showStrategyOneStep(self,path):
      toContinue=GUIAgentStep.guiStrategyOne(self.maze,self.flammabilityRate,path)
      self.updateDrawing()
      if toContinue[0]:
         self.after(1000,self.showStrategyOneStep,toContinue[2])

   # driver for above method
   def showGradualStrategyOne(self):
      self.showStrategyOneStep(None)
      self.mainloop()


   # below method does not show gradually
   def showEntireStrategyOne(self):
       Strategy1.doStrategyOne(self.maze,self.flammabilityRate)
       self.updateDrawing()
       self.mainloop()


   # method to gradually show fire steps for strategy 2
   def showStrategyTwoStep(self,currLoc):
      toContinue = GUIAgentStep.guiStrategyTwo(self.maze, self.flammabilityRate,currLoc)
      self.updateDrawing()
      if toContinue[0]:
         self.after(1000, self.showStrategyTwoStep, toContinue[1])

   # driver for above method
   def showGradualStrategyTwo(self):
      self.showStrategyTwoStep(None)
      self.mainloop()

   # method that does not show gradually below
   def showEntireStrategyTwo(self):
      Strategy2.doStrategyTwo(self.maze,self.flammabilityRate)
      self.updateDrawing()
      self.mainloop()





#resizing canvas code from
   # https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
class ResizingCanvas(tkinter.Canvas):
   def __init__(self, parent, **kwargs):
      tkinter.Canvas.__init__(self, parent, **kwargs)
      self.bind("<Configure>", self.on_resize)
      self.height = self.winfo_reqheight()
      self.width = self.winfo_reqwidth()

   def on_resize(self, event):
      # determine the ratio of old width/height to new width/height
      wscale = float(event.width) / self.width
      hscale = float(event.height) / self.height
      self.width = event.width
      self.height = event.height
      # resize the canvas
      self.config(width=self.width, height=self.height)
      # rescale all the objects tagged with the "all" tag
      self.scale("all", 0, 0, wscale, hscale)


# test for now

# hi = CanvasMaze(10,0.1,0.1)
# hi.showGradualStrategyTwo()
# hi.mainloop()




