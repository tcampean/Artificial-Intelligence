import pickle, numpy as np
from random import random, randint
import pygame

BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Map():
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, dronex,droney,finalx,finaly,it,path = [],colour=BLUE, background=WHITE):

        imagine = pygame.Surface((int(400*it), 400))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        iteration = pygame.Surface((20,20))
        iteration.fill(GRAYBLUE)
        final = pygame.Surface((20,20))
        final.fill(RED)
        pygame.display.flip()
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                if self.surface[i][j] == -1:
                    imagine.blit(iteration,(j*20,i*20))
                if [i,j] in path:
                    imagine.blit(mark,(j*20,i*20))
                if i == finalx and j == finaly:
                    imagine.blit(final,(j*20,i*20))
        drone = pygame.image.load("drona.png")
        imagine.blit(drone,(droney*20,dronex*20))
        return imagine