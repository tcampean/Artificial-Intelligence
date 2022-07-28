import random
from utils import *

import numpy as np

class Drone:
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setCoords(self, x, y):
        self.x = x
        self.y = y


class Map:
    def __init__(self):
        self.surface = np.zeros((MAP_HEIGHT, MAP_WIDTH))
        self.randomMap()

    def randomMap(self, fill=0.2):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if random.random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string




class Sensor:
    def __init__(self, x, y, map):
        self.x = x
        self.y = y
        self.positions = [0 for i in range(6)]
        self.surface = map
        self.max_energy = 0

    def valid_square(self, x, y):
        if x < 0 or y < 0 or x >= 20 or y >= 20:
            return False

        if self.surface.surface[x][y] == 1:
            return False
        return True

    def find_max_energy(self):
        blocked = [False for i in range(4)]
        for i in range(1, 6):
            self.positions[i] = self.positions[i - 1]
            for d in range(4):
                if not blocked[d]:
                    newX = self.x + dir[d][0] * i
                    newY = self.y + dir[d][1] * i
                    if self.valid_square(newX, newY):
                        self.positions[i] += 1
                    else:
                        blocked[d] = True

    def compute_max_energy(self):
        for energy in range(5):
            if self.positions[energy] == self.positions[energy + 1]:
                self.max_energy = energy
                return
        self.max_energy = 5

    def get_max_energy(self):
        return self.max_energy

    def get_positions(self):
        return self.positions

    def get_coordinates(self):
        coord = (self.x, self.y)
        return coord

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class Ant:
    def __init__(self):
        self.size = SENSOR_COUNT
        self.path = [random.randint(0, SENSOR_COUNT - 1)]
        self.fitness = 0
        self.battery = BATTERY


    def get_possible_moves(self, distances):
        moves = []
        current_sensor = self.path[-1]

        for next_sensor in range(SENSOR_COUNT):
            if next_sensor != current_sensor and distances[current_sensor][next_sensor] != INFINITY and next_sensor not in self.path and self.battery >= distances[current_sensor][next_sensor]:
                moves.append(next_sensor)
        return moves

    def probability_of_path(self, moves, alpha, beta, distances, pheromones):
        current_sensor = self.path[-1]
        next_sensor_probability = [0 for i in range(SENSOR_COUNT)]

        for i in moves:
            distance_next_sensor = distances[current_sensor][i]
            pheromone_next_sensor = pheromones[current_sensor][i]

            prob = (distance_next_sensor ** beta) * (pheromone_next_sensor ** alpha)
            next_sensor_probability[i] = prob

        return next_sensor_probability

    def next_move(self, distances, pheromones, q0, alpha, beta):
        moves = self.get_possible_moves(distances)
        if not moves:
            return False

        next_node_prob = self.probability_of_path(moves, alpha, beta, distances, pheromones)
        if random.random() < q0:
            best_probability = max(next_node_prob)
            selectedNode = next_node_prob.index(best_probability)
        else:
            selectedNode = self.randomize(next_node_prob)

        self.battery -= distances[self.path[-1]][selectedNode]
        self.path.append(selectedNode)

        return True

    def randomize(self, next_node_probability):
        sum_probability = sum(next_node_probability)

        if sum_probability == 0:
            return random.randint(0, len(next_node_probability) - 1)

        prob_sum = [next_node_probability[0] / sum_probability]
        for i in range(1, len(next_node_probability)):
            prob_sum.append(prob_sum[i - 1] + next_node_probability[i] / sum_probability)

        r = random.random()
        position = 0
        while r > prob_sum[position]:
            position += 1
        return position

    def compute_fitness(self, distances):
        length = 0
        for i in range(1, len(self.path)):
            length += distances[self.path[i - 1]][self.path[i]]

        self.fitness = length

    def get_fitness(self):
        return self.fitness

    def get_path(self):
        return self.path

    def get_battery(self):
        return self.battery