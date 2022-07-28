import time

import pygame
from random import random,randint
from Model.Environment import Map

#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class View:
    def __init__(self, controller):
        self.controller = controller

    def searchAStarVisualization(self,initialX, initialY, finalX, finalY,screen, iteration):

        visited = []
        unvisited = []

        start_node = [initialX, initialY, -1, -1, 0, 0, 0]
        unvisited.append(start_node)

        while len(unvisited) > 0:
            current_node = unvisited.pop(0)
            visited.append(current_node)
            self.controller.map.surface[current_node[0]][current_node[1]] = -1
            time.sleep(0.09)
            screen.blit(
                self.controller.map.image(self.controller.drone.x, self.controller.drone.y, finalX, finalY, iteration),
                (400 * (iteration - 1), 0))
            pygame.display.flip()

            if current_node[0] == finalX and current_node[1] == finalY:
                path = []
                path_node = current_node
                while path_node[2] != -1:
                    path.append([path_node[0], path_node[1]])
                    for element in visited:
                        if element[0] == path_node[2] and element[1] == path_node[3]:
                            path_node = element
                path = path[::-1]
                return path

            children = []

            if self.controller.valid_square(self.controller.map, current_node[0], current_node[1] + 1):
                children.append(
                    [current_node[0], current_node[1] + 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0], current_node[1] + 1, finalX, finalY),
                     current_node[4] + 1 + self.controller.manhattan(current_node[0], current_node[1] + 1, finalX,
                                                                     finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0], current_node[1] - 1):
                children.append(
                    [current_node[0], current_node[1] - 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0], current_node[1] - 1, finalX, finalY),
                     current_node[4] + 1 + self.controller.manhattan(current_node[0], current_node[1] - 1, finalX,
                                                                     finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0] + 1, current_node[1]):
                children.append(
                    [current_node[0] + 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0] + 1, current_node[1], finalX, finalY),
                     current_node[4] + 1 + self.controller.manhattan(current_node[0] + 1, current_node[1], finalX,
                                                                     finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0] - 1, current_node[1]):
                children.append(
                    [current_node[0] - 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0] - 1, current_node[1], finalX, finalY),
                     current_node[4] + 1 + self.controller.manhattan(current_node[0] - 1, current_node[1], finalX,
                                                                     finalY)])

            for child in children:
                if child not in visited:
                    if child in unvisited:
                        for unvisited_child in unvisited:
                            if child[0] == unvisited_child[0] and child[1] == unvisited_child[1]:
                                if child[6] < unvisited_child[6]:
                                    unvisited.pop(unvisited.index(unvisited_child))
                                    unvisited.append(child)
                    else:
                        unvisited.append(child)



            unvisited.sort(key=lambda x: x[6])

    def searchGreedyVisualization(self, initialX, initialY, finalX, finalY, screen,iteration):
        open_list = []
        closed_list = []

        start_node = [initialX, initialY, -1, -1, 0, 0]
        end_node = [finalX, finalY, None, None, 9999, 0]

        open_list.append(start_node)

        while open_list:
            open_list.sort(key=lambda x: x[5])
            current_node = open_list[0]
            open_list.pop(0)
            closed_list.append(current_node)
            time.sleep(0.4)
            self.controller.map.surface[current_node[0]][current_node[1]] = -1
            screen.blit(self.controller.map.image(self.controller.drone.x, self.controller.drone.y, finalX, finalY,iteration),
                        (400*(iteration-1), 0))
            pygame.display.flip()

            if current_node[0] == end_node[0] and current_node[1] == end_node[1]:
                path = []
                path_node = current_node
                while path_node[2] != -1:
                    path.append([path_node[0], path_node[1]])
                    for element in closed_list:
                        if element[0] == path_node[2] and element[1] == path_node[3]:
                            path_node = element
                path = path[::-1]
                return path

            children = []

            if self.controller.valid_square(self.controller.map, current_node[0], current_node[1] + 1):
                children.append(
                    [current_node[0], current_node[1] + 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0], current_node[1] + 1, finalX, finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0], current_node[1] - 1):
                children.append(
                    [current_node[0], current_node[1] - 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0], current_node[1] - 1, finalX, finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0] + 1, current_node[1]):
                children.append(
                    [current_node[0] + 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0] + 1, current_node[1], finalX, finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0] - 1, current_node[1]):
                children.append(
                    [current_node[0] - 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0] - 1, current_node[1], finalX, finalY)])

            for child in children:
                if child in closed_list:
                    continue
                if child not in open_list:
                    open_list.append(child)

    def searchGreedyVisualization2(self, initialX, initialY, finalX, finalY, screen,iteration):
        open_list = []
        closed_list = []

        start_node = [initialX, initialY, -1, -1, 0, 0]
        end_node = [finalX, finalY, None, None, 9999, 0]

        open_list.append(start_node)

        while open_list:
            open_list.sort(key=lambda x: x[5])
            print(open_list)
            current_node = open_list[0]
            open_list.pop(0)
            closed_list.append(current_node)
            self.controller.map.surface[current_node[0]][current_node[1]] = -1
            if current_node[0] == end_node[0] and current_node[1] == end_node[1]:
                path = []
                path_node = current_node
                while path_node[2] != -1:
                    path.append([path_node[0], path_node[1]])
                    for element in closed_list:
                        if element[0] == path_node[2] and element[1] == path_node[3]:
                            path_node = element
                path = path[::-1]
                return path

            children = []

            if self.controller.valid_square(self.controller.map, current_node[0], current_node[1] + 1):
                children.append(
                    [current_node[0], current_node[1] + 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0], current_node[1] + 1, finalX, finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0], current_node[1] - 1):
                children.append(
                    [current_node[0], current_node[1] - 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0], current_node[1] - 1, finalX, finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0] + 1, current_node[1]):
                children.append(
                    [current_node[0] + 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0] + 1, current_node[1], finalX, finalY)])
            if self.controller.valid_square(self.controller.map, current_node[0] - 1, current_node[1]):
                children.append(
                    [current_node[0] - 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.controller.manhattan(current_node[0] - 1, current_node[1], finalX, finalY)])

            for child in children:
                if child in closed_list:
                    continue
                if child not in open_list:
                    open_list.append(child)

    def displayWithPath(self,image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image



    def run(self,finalx,finaly):
        pygame.init()
        # load and set the logo
        initialX = self.controller.drone.x
        initialY = self.controller.drone.y
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)

        # define a variable to control the main loop
        running = True
        iteration = 1
        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            map = Map()
            map.loadMap('test1.map')
            map.surface[finalx][finaly] = 0
            map.surface[initialX][initialY] = 0
            self.controller.map = map
            self.controller.map.surface[initialX, initialY] = 0
            self.controller.map.surface[finalx, finaly] = 0
            self.controller.drone.x = initialX
            self.controller.drone.y = initialY
            start = time.time()
            path = self.controller.searchAStar(initialX, initialY,finalx,finaly)
            stop = time.time()
            print("A* : " ,stop - start,"length", len(path))

            map = Map()
            map.loadMap('test1.map')
            map.surface[finalx][finaly] = 0
            map.surface[initialX][initialY] = 0
            self.controller.map = map
            self.controller.map.surface[initialX, initialY] = 0
            self.controller.map.surface[finalx, finaly] = 0
            self.controller.drone.x = initialX
            self.controller.drone.y = initialY

            start = time.time()
            path = self.controller.searchGreedy(self.controller.drone.x,self.controller.drone.y,finalx,finaly)
            stop = time.time()
            print("Greedy: ", stop - start, "Length", len(path))

            map = Map()
            map.loadMap('test1.map')
            map.surface[finalx][finaly] = 0
            map.surface[initialX][initialY] = 0
            self.controller.map = map
            self.controller.map.surface[initialX, initialY] = 0
            self.controller.map.surface[finalx, finaly] = 0
            self.controller.drone.x = initialX
            self.controller.drone.y = initialY

            path = self.searchAStarVisualization(self.controller.drone.x, self.controller.drone.y, finalx, finaly,
                                                 screen, iteration)
            iteration = 1
            for elem in path:
                self.controller.drone.x = elem[0]
                self.controller.drone.y = elem[1]
                screen.blit(self.controller.map.image(self.controller.drone.x,self.controller.drone.y,finalx,finaly,iteration,path),(400*(iteration-1),0))
                pygame.display.flip()
                time.sleep(0.4)
            drona = pygame.image.load("drona.png")
            screen.blit(drona, (self.controller.drone.y * 20, self.controller.drone.x * 20))
            iteration +=1
            map = Map()
            map.loadMap('test1.map')
            map.surface[finalx][finaly] = 0
            map.surface[initialX][initialY] = 0
            self.controller.map = map
            self.controller.map.surface[initialX, initialY] = 0
            self.controller.map.surface[finalx, finaly] = 0
            self.controller.drone.x = initialX
            self.controller.drone.y = initialY
            path = self.searchGreedyVisualization(self.controller.drone.x, self.controller.drone.y, finalx, finaly,
                                                  screen, iteration)
            for elem in path:
                self.controller.drone.x = elem[0]
                self.controller.drone.y = elem[1]
                screen.blit(self.controller.map.image(self.controller.drone.x,self.controller.drone.y,finalx,finaly,iteration,path),(400*(iteration-1),0))
                pygame.display.flip()
                time.sleep(0.4)
            drona = pygame.image.load("drona.png")
            screen.blit(drona, (self.controller.drone.y * 20, self.controller.drone.x * 20))
            running = False

        pygame.quit()
