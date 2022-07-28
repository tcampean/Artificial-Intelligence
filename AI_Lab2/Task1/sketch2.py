

# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np

import View.View
from Model.Drone import Drone
from Model.Environment import Map
from Controller.Controller import Controller

'''
#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations 
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))

        return imagine
        

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y-1]==0:
                self.y = self.y - 1
        if self.y < 19:        
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                 self.y = self.y + 1
                  
    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        
        return mapImage


def valid_square(detectedMap, x, y):
        if x < 0 or y < 0 or x >= 20 or y >= 20:
            return False

        if detectedMap.surface[x][y] == -1 or detectedMap.surface[x][y] == 1:
            return False
        return True

def heuristic(currentX, currentY, finalX, finalY):
    return (currentX - finalX) ** 2 + (currentY - finalY) ** 2

def searchAStar(mapM, droneD, initialX, initialY, finalX, finalY):

    # node data format [x,y,parentx,parenty,distance,heuristic,totalcost]
    open_list = []
    closed_list = []

    start_node = [initialX,initialY,-1,-1,0,0,0]
    end_node = [finalX,finalY,None,None,0,0,0]

    open_list.append(start_node)

    while open_list:
        current_node = open_list[0]

        position = 0
        min_position = 0

        for node in open_list:
            if node[6] < current_node[6]:
                current_node = node
                min_position = position
            position += 1

        open_list.pop(min_position)
        closed_list.append(current_node)

        if current_node[0] == end_node[0] and current_node[1] == end_node[1]:
            path = []
            path_node = current_node
            while path_node[2] != -1:
                path.append([path_node[0],path_node[1]])
                for element in closed_list:
                    if element[0] == path_node[2] and element[1] == path_node[3]:
                        path_node = element
            path = path[::-1]
            return path

        children = []

        if valid_square(mapM,current_node[0], current_node[1] +1):
            children .append([current_node[0], current_node[1]+1, current_node[0],current_node[1],0,0,0])
        if valid_square(mapM,current_node[0], current_node[1] -1):
            children .append([current_node[0], current_node[1]-1, current_node[0],current_node[1],0,0,0])
        if valid_square(mapM,current_node[0]+1, current_node[1]):
            children .append([current_node[0]+1, current_node[1], current_node[0],current_node[1],0,0,0])
        if valid_square(mapM,current_node[0] -1, current_node[1]):
            children .append([current_node[0] -1, current_node[1], current_node[0],current_node[1],0,0,0])

        for child in children:
            for child2 in closed_list:
                if child[0] == child2[0] and child[1] == child2[1]:
                    continue

            child[4] = current_node[4] + 1
            child[5] = heuristic(child[0],child[1], end_node[0], end_node[1])
            child[6] = child[4] + child[5]


            for child3 in open_list:
                if child[0] == child3[0] and child[1] == child3 and child[4] <   child3[4]:
                    continue

            open_list.append(child)

def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY):
    # TO DO 
    # implement the search function and put it in controller
    # returns a list of moves as a list of pairs [x,y]
    pass

def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
    
def displayWithPath(image, path):
    mark = pygame.Surface((20,20))
    mark.fill(GREEN)
    for move in path:
        image.blit(mark, (move[1] *20, move[0] * 20))
        
    return image

                  
# define a main function
def main():
    
    # we create the map
    m = Map() 
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")
    
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")
        
    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)
    
    #create drona
    d = Drone(5, 7)
    
    
    
    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)
    
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        path = searchAStar(m, None, d.x, d.y, 7, 11)
        screen.blit(displayWithPath(m.image(), path), (0, 0))

        drona = pygame.image.load("drona.png")
        screen.blit(drona,(d.y*20, d.x*20))
        final = pygame.Surface((20,20))
        final.fill(RED)
        screen.blit(final, (11 * 20,7 * 20))
        pygame.display.flip()
       

    pygame.quit()
    '''
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    map = Map()
    map.loadMap('test1.map')
    x = randint(0, 19)
    y = randint(0, 19)
    map.surface[x][y] = 0
    d = Drone(x,y)
    x = randint(0, 19)
    y = randint(0, 19)
    map.surface[x][y] = 0
    c = Controller(map,d)
    view = View.View.View(c)
    view.run(17,17)
