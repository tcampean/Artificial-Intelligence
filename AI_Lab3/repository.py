# -*- coding: utf-8 -*-

import pickle
from domain import *


class repository():
    def __init__(self):
         
        self.populations = []
        self.cmap = Map()
        self.drone = Drone(random.randint(0,19), random.randint(0,19))

    def get_population(self):
        return self.populations

    def get_map(self):
        return self.cmap

    def get_drone(self):
        return self.drone

    def random_map(self):
        self.cmap.randomMap()
        
    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args    
        self.populations.append(Population(self.drone,self.cmap))
        
    # TO DO : add the other components for the repository: 
    #    load and save from file, etc

    def load_random(self):
        self.cmap.randomMap()