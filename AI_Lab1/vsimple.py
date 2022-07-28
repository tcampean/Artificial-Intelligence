# import the pygame module, so you can use it
import pickle, pygame, sys
import time

from pygame.locals import *
from random import random, randint
import numpy as np

# Creating some colors
BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

# define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Environment():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))

    def randomMap(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        # UP 
        xf = x - 1
        while ((xf >= 0) and (self.__surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.__n) and (self.__surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.__m) and (self.__surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.__surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine


class DMap():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1

    def markDetectedWalls(self, e, x, y):
        #   To DO
        # mark on this map the walls that you detect
        walls = e.readUDMSensors(x, y)
        i = x - 1
        if walls[UP] > 0:
            while ((i >= 0) and (i >= x - walls[UP])):
                self.surface[i][y] = 0
                i = i - 1
        if (i >= 0):
            self.surface[i][y] = 1

        i = x + 1
        if walls[DOWN] > 0:
            while ((i < self.__n) and (i <= x + walls[DOWN])):
                self.surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.surface[i][y] = 1

        j = y + 1
        if walls[LEFT] > 0:
            while ((j < self.__m) and (j <= y + walls[LEFT])):
                self.surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.surface[x][j] = 1

        j = y - 1
        if walls[RIGHT] > 0:
            while ((j >= 0) and (j >= y - walls[RIGHT])):
                self.surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.surface[x][j] = 1

        return None

    def image(self, x, y):

        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(GRAYBLUE)

        for i in range(self.__n):
            for j in range(self.__m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                elif (self.surface[i][j] == 0):
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine


class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def valid_square(self, visited,detectedMap, x, y):
        if x < 0 or y < 0 or x >= 20 or y >= 20:
            return False

        if detectedMap.surface[x][y] == -1 or detectedMap.surface[x][y] == 1 or [x,y] in visited:
            return False
        return True


    def neighbour_square(self,x,y,nx,ny):
        if nx < 0 or ny < 0 or nx >= 20 or ny >= 20:
            return False
        if nx == x + 1 and ny == y:
            return True
        if nx == x -1 and ny == y:
            return True
        if nx == x and ny == y+1:
            return True
        if nx == x and ny == y - 1:
            return True
        if nx == x and ny == y:
            return True
        return False

    def get_parent(self,parent,x,y):
        for node in parent:
            if node[0] == x and node[1] == y:
                return [node[2],node[3]]

    def get_path(self,parent,path,x,y):
        done = False
        while not done:
            node = self.get_parent(parent,x,y)
            if node[0] == -1:
                return path
            else:
                path.append([node[0],node[1]])
                x = node[0]
                y = node[1]



    def short_path(self,detectedMap,x,y,nx,ny):
        stack = []
        stack.append([x,y])
        parent = []
        parent.append([x,y,-1,-1])
        visited = []
        visited.append([x,y])

        while stack:
            current_square = stack[0]
            stack.pop(0)

            if current_square[0] == nx and current_square[1] == ny:
                path = []
                self.get_path(parent,path,nx,ny)
                return path

            if self.valid_square(visited,detectedMap,current_square[0]-1, current_square[1]):
                stack.append([current_square[0]- 1,current_square[1]])
                parent.append([current_square[0]- 1,current_square[1],current_square[0],current_square[1]])
                visited.append([current_square[0]-1, current_square[1]])
            if self.valid_square(visited, detectedMap, current_square[0] + 1, current_square[1]):
                stack.append([current_square[0] + 1, current_square[1]])
                parent.append([current_square[0] + 1, current_square[1], current_square[0], current_square[1]])
                visited.append([current_square[0]+1, current_square[1]])
            if self.valid_square(visited, detectedMap, current_square[0], current_square[1] + 1):
                stack.append([current_square[0], current_square[1] + 1])
                parent.append([current_square[0], current_square[1]+1, current_square[0], current_square[1]])
                visited.append([current_square[0],current_square[1]+1])
            if self.valid_square(visited, detectedMap, current_square[0], current_square[1]-1):
                stack.append([current_square[0] , current_square[1]-1])
                parent.append([current_square[0], current_square[1]-1, current_square[0], current_square[1]])
                visited.append([current_square[0],current_square[1]-1])
        return



    def moveDSF(self, detectedMap):
        stack = []
        stack.append([self.x,self.y])
        visited = []
        detectedMap.surface[self.x, self.y] = 0

        while len(stack) != 0:
            current_square = stack[len(stack) - 1]
            if not self.neighbour_square(self.x,self.y,current_square[0],current_square[1]):
                path = self.short_path(detectedMap,self.x,self.y,current_square[0],current_square[1])
                print(path)
                path.reverse()
                for node in path:
                    self.x = node[0]
                    self.y = node[1]
                    time.sleep(0.2)
                    detectedMap.markDetectedWalls(e, self.x, self.y)
                    screen.blit(detectedMap.image(self.x, self.y), (400, 0))
                    pygame.display.flip()
                    detectedMap.surface[current_square[0], [current_square[1]]] = 0


            stack.pop(len(stack)- 1)
            visited.append(current_square)

            self.x = current_square[0]
            self.y = current_square[1]
            time.sleep(0.2)
            detectedMap.markDetectedWalls(e, self.x, self.y)
            screen.blit(detectedMap.image(self.x, self.y), (400, 0))
            pygame.display.flip()

            detectedMap.surface[current_square[0],[current_square[1]]] = 0

            if self.valid_square(visited,detectedMap,current_square[0]-1, current_square[1]):
                stack.append([current_square[0]- 1,current_square[1]])
            if self.valid_square(visited, detectedMap, current_square[0] + 1, current_square[1]):
                stack.append([current_square[0] + 1, current_square[1]])
            if self.valid_square(visited, detectedMap, current_square[0], current_square[1] + 1):
                stack.append([current_square[0], current_square[1] + 1])
            if self.valid_square(visited, detectedMap, current_square[0], current_square[1]-1):
                stack.append([current_square[0] , current_square[1]-1])



# define a main function
def main():
    # we create the environment
    global screen, e
    e = Environment()
    e.loadEnvironment("test2.map")
    # print(str(e))

    # we create the map
    m = DMap()

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # cream drona
    d = Drone(x, y)

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800, 400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0, 0))

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

        d.moveDSF(m)
        running = False
        m.markDetectedWalls(e, d.x, d.y)
        screen.blit(m.image(d.x, d.y), (400, 0))
        pygame.display.flip()



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
