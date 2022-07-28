import random

from repository import *


class controller():
    def __init__(self):
        self.repository = repository()


    def iteration(self, population):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        individuals = population.v
        firstIndividual = random.randint(0, len(individuals)-1)
        secondIndividual = random.randint(0,len(individuals)-1)
        firstParent = individuals[firstIndividual]
        secondParent = individuals[secondIndividual]
        firstOffspring, secondOffspring = secondParent.crossover(firstParent)
        firstOffspring.mutate()
        secondOffspring.mutate()
        if firstOffspring.getFitness() > secondOffspring.getFitness():
            population.v.append(firstOffspring)
        else:
            population.v.append(secondOffspring)


    def run(self, iterationCount, generationCount, individualSize, populationSize,seed):
        # args - list of parameters needed in order to run the algorithm
        
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics
        
        # return the results and the info for statistics

        random.seed(seed)
        population = Population(self.repository.drone,self.repository.cmap,populationSize,individualSize)
        self.repository.populations.append(population)

        for generation in range(generationCount):
            for iteration in range(iterationCount):
                self.iteration(population)
        population.v = population.selection(populationSize)
        allFitness = []
        for individual in population.v:
            allFitness.append(individual.getFitness())

        kingOfTheJungle =population.selection(1)[0]
        average = np.average(allFitness)

        return kingOfTheJungle,average
    
    
    def solver(self, iterationCount, generationCount,individualSize, populationSize):

        kingsOfTheJungle = []
        average = []

        for i in range(4):
            king,avg = self.run(iterationCount,generationCount,individualSize,populationSize,i)

            print("Trial: " + str(i) +" Average: " + str(avg) + " Best Fitness: " + str(king.getFitness()))

            kingsOfTheJungle.append(king)
            average.append(avg)
        return kingsOfTheJungle,average

       