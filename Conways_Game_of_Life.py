import pygame
from pygame.locals import *
from random import random
import copy

columns = 60
rows = 60
cellSize = 10    #pixel width and height of each cell
cellGap = 0     #pixels be#Set a variable that allows a QUIT event to break the infinite loop
running = True

#Trackers to tell when evolution has stopped
parentGeneration = [[0] * columns] * rows
generation = 1
stagnant = 0

def InitialArray():
    global Game_Array, rows, columns
    Game_Array = []
    for y in range(rows):
        Game_Array.append([])
        for x in range(columns):
            Game_Array[y].append(0)
    #print "the initial array of zeros is:"
    #print Game_Array
    #print "The Game Array to be analysed:"
    #print Game_Array
    
def MouseInput():
    global Game_Array
    global nextGeneration

    running =1
    updateRect =[]

    while running:     
        event = pygame.event.poll()
        if (event.type == pygame.KEYDOWN): #and (event.key == pygame.K_KP_ENTER):
            running = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print "mouse at (%d, %d)" % event.pos
            Vector_Pos=event.pos

            #ROW
            x=Vector_Pos[1]
            i= x/cellSize
            cell_Row=int(i)

            #COLUMN 
            y=Vector_Pos[0]
            j= y/cellSize
            cell_Col=int(j)

            #print cell_Row , cell_Col
            if Game_Array[cell_Row][cell_Col]==0:
                Game_Array[cell_Row][cell_Col]=1
                updateRect.append(pygame.draw.rect(screen,(0, 255, 0) ,cells[cell_Row][cell_Col]))                    
                pygame.display.update(updateRect)
            elif Game_Array[cell_Row][cell_Col]==1:
                Game_Array[cell_Row][cell_Col]=0
                updateRect.append(pygame.draw.rect(screen,(0, 0, 0) ,cells[cell_Row][cell_Col]))                    
                pygame.display.update(updateRect)
                
            #print "The filled Game Array containing live and dead cells is:"
            #print Game_Array

        elif event.type ==pygame.QUIT:
            nextGeneration =0
            return nextGeneration

def Game_Quit():
    if nextGeneration ==0:
        pygame.event.clear()
        pygame.quit()
    
def displayArray():
    updateRect = []
    for i in range(rows):
        for j in range(columns):
            #only redraw cells that have changed.
            if (Game_Array[i][j] != parentGeneration[i][j]):
                if Game_Array[i][j]:
                    updateRect.append(pygame.draw.rect(screen, (0,255,0),cells[i][j]))
                else:
                    updateRect.append(pygame.draw.rect(screen, (0,0,0),cells[i][j]))
    pygame.display.update(updateRect)

def reproduce():
    #calculate who live and who dies
    global generation
    global parentGeneration
    global Game_Array
    
    duplicate = copy.deepcopy(Game_Array)
    for y in range(0,rows):
        for x in range(0,columns):
            neighbour_count = liveNeighbours(y,x) #should return count from the fn

            if Game_Array[y][x]==0 and neighbour_count ==3:
                duplicate[y][x]=1
            elif Game_Array[y][x]==1 and (neighbour_count<2 or neighbour_count>3):
                duplicate[y][x]=0

    Game_Array = duplicate
    #print "After reproduction:"
    #print Game_Array
    
def liveNeighbours(y, x):
    #Returns the number of live neighbours
    count = 0
    if y > 0:
        if Game_Array[y-1][x]:
            count = count + 1
        if x > 0:
            if Game_Array[y-1][x-1]:
                count = count + 1
        if columns > (x + 1):
            if Game_Array[y-1][x+1]:
                count = count + 1

    if x > 0:
        if Game_Array[y][x-1]:
            count = count + 1
    if columns > (x + 1):
        if Game_Array[y][x+1]:
            count = count + 1

    if rows > (y + 1):
        if Game_Array[y+1][x]:
            count = count + 1
        if x > 0:
            if Game_Array[y+1][x-1]:
                count = count + 1
        if columns > (x + 1):
            if Game_Array[y+1][x+1]:
                count = count + 1
    #print("row: ", y, "col: ", x,"has ", count, " neighbours") 
    return count
          
#main program

#setup screen
pygame.init()
screen = pygame.display.set_mode((columns*(cellSize+cellGap)-cellGap,rows*(cellSize+cellGap)-cellGap))
print screen
pygame.display.set_caption("Game of Life")
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
screen.blit(background,(0,0))

#Set a timer to initiate each geneartional event
#pygame.time.set_timer(nextGeneration, generationGap)

#Populate an array full of cells
Game_Array = []
cells = []
for i in range(rows):
    line = []
    for j in range(columns):
        line.append(pygame.Rect(((cellSize+cellGap)*j,(cellSize+cellGap)*i), (cellSize,cellSize)))
    cells.append(line)
#print "The cell format is as follows:"
#print cells

#generate universe
InitialArray() #creates the arrays of zeros and ones
global nextGeneration

nextGeneration=1
run=True

while run:
        #print nextGeneration
        MouseInput()
        #print "Before reproduction:"
        #print Game_Array
        #print nextGeneration
        if nextGeneration==0:
            run=False
            Game_Quit()            
        else:    
            reproduce()
            screen.fill((0,0,0))
            pygame.display.update()
            pygame.time.delay(5)
            displayArray()#displays the next generation
