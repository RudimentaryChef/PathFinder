#Credit to Tech with Tim for the implementation idea and the youtube course that teaches a lot.

#Importing Necessary Modules
import pygame
import math 
from queue import PriorityQueue
#Setting Screen Size as a 800 x 800 square
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")
RED= (255,0,0)
GREEN= (0,255,0)
BLUE = (0,255,0)
YELLOW =(255,255,0)
WHITE =(255,255,255)
BLACK =(0,0,0)
PURPLE =(128,128,128)
ORANGE =(255,160,0)
GREY =(128,127,126)
TURQUOISE =(64,224,208)
#Keep track of color of spots and the space it is in
#Indexing using rows and columns
#y,x instead of x,y
class Spot:
    #Gives the properties for a spot
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    #gets Position
    def get_pos(self):
        return self.row, self.col
    #if the path is closed/eliminated then red
    def is_closed(self):
        return self.color == RED
    #open/ongoing path = green
    def is_open(self):
        return self.color == GREEN
    #wall is black
    def is_barrier(self):
        return self.color == BLACK
    #start point
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
    #goal point
        return self.color == TURQUOISE
    #default color
    def reset(self):
        self.color = WHITE
    #same thing except instead of returning color it Makes the block the color
    def make_start(self):
        self.color = ORANGE
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    #draws a rectangle. (A spot in window)
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    #All spots have a neighbours
    def update_neighbors(self,grid):
        self.neighbors = []
        #Is it below and NOT A barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): 
            self.neighbors.append(grid[self.row + 1][self.col])
        #Is it above and NOT a barrier
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): 
            self.neighbors.append(grid[self.row - 1][self.col])
        #Is it to ethe right and NOT a barrier
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        #Is it to the left and not a barrier
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col - 1])


    #If we compare two spot objects. The other spot is less than the current spot
    def __lt__(self,other):
        return False
#the H function, using Manhattan/L Distance How far two points are
def h(p1,p2):
    x1,y1 = p1 #point 1
    x2,y2 = p2 #point 2
    return abs(x1 - x2) + abs(y1 - y2) #returns absolute distance
#Returns the grid. 
#Will draw the optimal path from base to optimal path found
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
def algorithm(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start)) #same as Append. We add the start node to our queue
    #tracks where we came from
    came_from = {}
    #Orignal g and f scores are assumed to be infinity
    g_score = {spot:float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    #f score at start node. (So that when we reach end node we DONT assume its best path)
    f_score[start] = h(start.get_pos(),end.get_pos())
    #HASHU MAPU
    #Keeps track of the items in the Priority Queue HASHUUUU MAPUUUUU
    open_set_hash = {start}
    #Runs till open set is empty
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #a way to exit loop just in case
        current = open_set.get()[2] #indexing at 2. (Open stores f,count,node. We want node only)
        open_set_hash.remove(current)
        if current == end:
                #we are at the end
                reconstruct_path(came_from, end, draw)
                end.make_end()
                return True 
            #Our G score is +1 for every neighbor we traverse
        for neighbor in current.neighbors:
            #Our G score is +1 for every neighbor we traverse
            temp_g_score = g_score[current] + 1 #we assume all the weighted distance is one.
            #if we find a better method update and store it. (If lesser g)
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    #if it is not under consideration
                    #consider this new guy
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()#it is in the closed set. (already considered set)
        draw()
        if current != start:
            #if we are not the start node and we looked at it. Then itsn going to be added into closed set.
            current.make_closed()
    #we did not find a path
    return False
#makes a grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid
#Drawing Grid Lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
def draw(win,grid,rows,width):
#Fills the screen in one color in one frame with just one new thing
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()
    #It will draw whatever we want to draw onto the screen and will reset every frame
def get_clicked_pos(pos,rows,width):
    gap = width//rows
    y,x = pos 
    row = y//gap
    col = x//gap
    return row,col #Where we are and what we have clicked on
def main(win, width):
    ROWS = 50 # 50 rows
    grid = make_grid(ROWS, width) #makes a grid
    #does not start yet
    start = None
    end = None
    started = False
    run = True
    #while game is running
    while run:
        #draw the grid
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #if left mouse then start first, then end, then barriers
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()
            #removes if right mouse click.(2 is right mouse)
            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN: #if key is down
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            #everytime we press the activation key (and we have not started yet), neighbors are updated
                            spot.update_neighbors(grid)
                        #Lambda is an anonymous function
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)
                        #Simply it just equals any function. the draw function IS the arguement.
                        #The  lambda is the algorithm

#main function duh
main(WIN, WIDTH)