#import for testing
from Preliminaries.mazeGenerator import generateMaze
from Preliminaries import DFS
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
      tkinter.Grid.rowconfigure(self,0,weight=1)
      tkinter.Grid.columnconfigure(self,0,weight=1)
      dim = len(maze)
      self.dim=dim
      self.maze=maze
      self.obstacleDensity=obstacleDensity
      self.flammabilityRate=flammabilityRate
      self.mazeFrame=tkinter.Frame(self)
      self.mazeFrame.grid(column=0,row=0,sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
      self.labelFrame=tkinter.Frame(self)
      self.labelFrame.grid(column=0,row=1)
      for i in range(dim):
         tkinter.Grid.rowconfigure(self.mazeFrame,i,weight=1)
         for j in range(dim):
            tkinter.Grid.columnconfigure(self.mazeFrame,j,weight=1)
            if maze[i][j]==1:
               cell=tkinter.Label(self.mazeFrame,bg="black",text=maze[i][j],borderwidth=2,relief="solid")
            elif maze[i][j]==-1:
               cell=tkinter.Label(self.mazeFrame,bg="red",text=maze[i][j],borderwidth=2,relief="solid")
            elif maze[i][j]==2:
               cell = tkinter.Label(self.mazeFrame, bg="blue", text=maze[i][j], borderwidth=2, relief="solid")
            else:
               cell = tkinter.Label(self.mazeFrame, bg="white", text=maze[i][j], borderwidth=2, relief="solid")
            cell.config(height=2,width=10)
            cell.grid(column=j,row=i,sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
      #adding labels to bottom of window
      obstacle=tkinter.Label(self.labelFrame,text="Obstacle Density:"+str(obstacleDensity))
      flame = tkinter.Label(self.labelFrame,text="Flammability Rate:"+str(flammabilityRate))
      obstacle.grid(row=0,column=1)
      flame.grid(row=0,column=0)
      tkinter.Scrollbar(self.labelFrame,orient="horizontal")
      tkinter.Scrollbar(self.labelFrame, orient="vertical")

class CanvasMaze(tkinter.Tk):
   # the maze itself is a grid of cells (cells are tkinter labels)
   def __init__(self,  maze, obstacleDensity, flammabilityRate):
      super().__init__()
      dim = len(maze)
      self.cellSize=30
      self.dim=dim
      self.maze=maze
      self.width=self.cellSize*len(maze)
      self.height=self.cellSize*len(maze)
      self.obstacleDensity=obstacleDensity
      self.flammabilityRate=flammabilityRate
      self.mazeCanvas=ResizingCanvas(self,width=self.width,height=self.height,background="white")
      self.mazeCanvas.bind()
      self.mazeCanvas.pack(expand="yes")
      for i in range(dim):
         x=i*self.cellSize
         for j in range(dim):
            y=j*self.cellSize
            if maze[i][j]==1:
               self.mazeCanvas.create_rectangle(x,y,x+self.cellSize,y+self.cellSize,fill="black")
            elif maze[i][j]==-1:
               self.mazeCanvas.create_rectangle(x, y, x + self.cellSize, y + self.cellSize, fill="red")
            elif maze[i][j]==2:
               self.mazeCanvas.create_rectangle(x, y, x + self.cellSize, y + self.cellSize, fill="blue")
            else:
               self.mazeCanvas.create_rectangle(x, y, x + self.cellSize, y + self.cellSize, fill="white")
      self.mazeCanvas.addtag_all("all")


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
testMaze= generateMaze(100, 0.2)
path = DFS.dfsGetPath(testMaze,(0,0),(len(testMaze)-1,len(testMaze)-1))
for tup in path:
   testMaze[tup[0]][tup[1]]=2
hi = CanvasMaze(testMaze,0.2,0)
hi.title("Maze with obstacleDensity=0.2 flameDensity=0")
hi.mainloop()