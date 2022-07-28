# -*- coding: utf-8 -*-


# imports
import time

from gui import *
from controller import *
from repository import *
from domain import *
import matplotlib.pyplot as pyplot


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

class UI:
    def __init__(self):
        self.controller = controller()
        self.bestIndividuals = []
        self.populationSize = 50
        self.individualSize = 30
        self.generationCount = 20
        self.iterationCount = 100

    def menu_options(self):
        print("1: Evolution Algorithm Options")
        print("2: Map Options")

    def print_map_options(self):
        print("1: Create a new map")
        print("2: Load Map")
        print("3: Save Map")
        print("4: Visualize Map")

    def print_evolution_algorithm_options(self):
        print("1: Parameter")
        print("2: Solve")
        print("3: Drone Visualization")

    def dataFile(self, average, iterationCount = 100 , generationCount = 20, individualSize = 30, populationSize = 50,seed = 30):

        file = open("statistics.txt","a")
        file.write("Seed: 1-" + str(seed) )
        file.write("Population Size: " + str(populationSize)+ " Individual Size: " + str(individualSize) + " Generation count: " + str(generationCount) + " Iterations: " + str(iterationCount))
        file.write("Average: " + str(np.average(average)))
        file.write("Standard Deviation: " + str(np.std(average)))
        file.write("\n")
        file.close()



    def runUI(self):
        while True:
            self.menu_options()
            command = int(input("Enter your command"))

            if command == 2:
                self.mapUI()
            else:
                self.eaUI()

    def graph(self,average):
        pyplot.plot(average)
        pyplot.savefig("graph.png")





    def mapUI(self):
        map = Map()
        onGoing = True
        while onGoing:
            self.print_map_options()
            command = int(input("Enter command: "))

            if command == 1:
                map.randomMap()
            elif command == 4:
                print(map)
            else:
                onGoing = False

        self.controller.repository.cmap = map

    def eaUI(self):
        onGoing = True
        while onGoing:
            self.print_evolution_algorithm_options()
            command = int(input("Enter command: "))

            if command == 1:
                self.populationSize = int(input("Population size: "))
                self.individualSize = int(input("Number of individuals: "))
                self.generationCount = int(input("Number of generations: "))
                self.iterationCount = int(input("Number of iterations: "))

            elif command == 2:
                start = time.time()
                kings, averages = self.controller.solver(self.iterationCount, self.generationCount, self.individualSize,self.populationSize)
                end = time.time()
                kings.sort(key=lambda e: e.getFitness(), reverse=True)
                self.bestIndividuals = kings[:3]
                self.graph(averages)
                self.dataFile(averages)
                print("Execution time: ", end - start)

            elif command == 3:
                screen = initPyGame((400, 400))
                movingDrone(screen, self.controller, self.bestIndividuals)
                closePyGame()
            elif command == 0:
                onGoing = False
            else:
                print("Invalid command.\n")








if __name__ == "__main__":
    ui = UI()
    ui.runUI()

