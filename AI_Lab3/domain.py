

import random
from utils import *
import numpy as np
from copy import deepcopy,copy

# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

class gene:
    def __init__(self):
        # random initialise the gene according to the representation
        pass


class Drone:
    def __init__(self, x, y, energy=10):
        self.x = x
        self.y = y
        self.energy = energy


class Individual:
    def __init__(self, drona, map, size=0):
        self.size = size
        self.x = [random.randint(0, 3) for i in range(self.size)]
        self.f = None
        self.discovered = []
        self.drone = drona
        self.surface = map

    def readUDMSensors(self, x, y,surface):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (surface[xf][y] == 0)):
            if [xf,y] not in self.discovered:
                readings[UP] = readings[UP] + 1
                self.discovered.append([xf,y])
            xf = xf - 1
        # DOWN
        xf = x + 1
        while ((xf < self.surface.n) and (surface[xf][y] == 0)):
            if [xf,y] not in self.discovered:
                readings[DOWN] = readings[DOWN] + 1
                self.discovered.append([xf,y])
            xf = xf + 1
        # LEFT
        yf = y + 1
        while ((yf < self.surface.m) and (surface[x][yf] == 0)):
            if [x,yf] not in self.discovered:
                readings[LEFT] = readings[LEFT] + 1
                self.discovered.append([x,yf])
            yf = yf + 1

        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (surface[x][yf] == 0)):
            if [x,yf] not in self.discovered:
                readings[RIGHT] = readings[RIGHT] + 1
                self.discovered.append([x,yf])
            yf = yf - 1

        return readings

    def valid_square(self, x, y):
        if x < 0 or y < 0 or x >= 20 or y >= 20:
            return False

        if self.surface.surface[x][y] == 1:
            return False
        return True


    def fitness(self):
        # compute the fitness for the indivisual
        # and save it in self.__f
        self.discovered = []
        copyMap = copy(self.surface.surface)
        readings= self.readUDMSensors(self.drone.x, self.drone.y,copyMap)
        fitness = readings[0] + readings[1] + readings[2] + readings[3]
        current_position = [self.drone.x, self.drone.y]
        moves = 0

        for i in self.x:
            direction = v[i]
            new_x = current_position[0] + direction[0]
            new_y = current_position[1] + direction[1]
            if self.valid_square(new_x,new_y):
                readings= self.readUDMSensors(new_x, new_y,copyMap)

                obtained_fitness = readings[0] + readings[1] + readings[2] + readings[3]
                fitness += obtained_fitness
            else:
                fitness -= 1000
            current_position = [new_x,new_y]
            moves = moves + 1
            if moves == self.drone.energy:
                break

        self.f = fitness

    def getFitness(self):
        self.fitness()
        return self.f
    
    def mutate(self, mutateProbability = 0.04):
        # perform a mutation with respect to the representation
        if random.random() < mutateProbability:
            self.x[random.randint(0,self.size-1)] = random.randint(0,3)

        
    
    def crossover(self, otherParent, crossoverProbability = 0.8):
        offspring1, offspring2 = Individual(self.drone,self.surface,self.size), Individual(self.drone,self.surface,self.size)
        if random.random() < crossoverProbability:
            offspring_breakpoint = random.randint(0,self.size)
            offspring1.x = self.x[offspring_breakpoint:] + otherParent.x[:offspring_breakpoint]
            offspring2.x = self.x[:offspring_breakpoint] + otherParent.x[offspring_breakpoint:]
            # perform the crossover between the self and the otherParent
        
        return offspring1, offspring2
    
class Population():
    def __init__(self,drone,surface, populationSize = 5, individualSize = 10):
        self.populationSize = populationSize
        self.v = [Individual(drone,surface,individualSize) for x in range(populationSize)]
        
    def evaluate(self):
        # evaluates the population
        for x in self.v:
            x.fitness()
            
            
    def selection(self, k = 3):
        # perform a selection of k individuals from the population
        # and returns that selection

        return sorted(self.v,key= lambda x: x.getFitness(), reverse=True)[:k]



    
class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random.random() <= fill :
                    self.surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

