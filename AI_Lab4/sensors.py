from utils import *
from domain import *
import random

class Sensors:
    def __init__(self, map):
        self.sensorList = []
        self.surface = map
        self.sensor_position()
        self.distances_between_sensors = [[0 for i in range(SENSOR_COUNT)] for i in range(SENSOR_COUNT)]
        self.sensor_distance()

        for sensor in self.sensorList:
            sensor.find_max_energy()
            sensor.compute_max_energy()

    def valid_square(self, x, y):
        if x < 0 or y < 0 or x >= 20 or y >= 20:
            return False

        if self.surface.surface[x][y] == 1:
            return False
        return True

    def compute_sensor_distance(self, startX, startY, endX, endY):
        distance = {(startX, startY): 0}
        visited = [(startX, startY)]
        while visited:
            currentX, currentY = visited.pop(0)
            for d in dir:
                newX = currentX + d[0]
                newY = currentY + d[1]
                if self.valid_square(newX, newY) and (newX, newY) not in distance:
                    distance[(newX, newY)] = distance[(currentX, currentY)] + 1
                    visited.append((newX, newY))

                    if newX == endX and newY == endY:
                        return distance[(endX, endY)]
        return INFINITY

    def sensor_position(self):
        self.sensorList.clear()

        for s in range(SENSOR_COUNT):
            newX, newY = random.randint(0, MAP_HEIGHT-1), random.randint(0, MAP_WIDTH-1)
            while self.surface.surface[newX][newY] != 0:
                newX, newY = random.randint(0, MAP_HEIGHT-1), random.randint(0, MAP_WIDTH-1)
            self.surface.surface[newX][newY] = SENSOR_POSITION
            self.sensorList.append(Sensor(newX, newY, self.surface))

    def sensor_distance(self):
        for i in range(len(self.sensorList)):
            self.distances_between_sensors[i][i] = 0
            newX, newY = self.sensorList[i].getX(), self.sensorList[i].getY()
            for j in range(i + 1, len(self.sensorList)):
                dist = self.compute_sensor_distance(newX, newY, self.sensorList[j].getX(), self.sensorList[j].getY())
                self.distances_between_sensors[i][j] = self.distances_between_sensors[j][i] = dist

    def get_sensor_list(self):
        return self.sensorList

    def get_distance_between_sensors(self):
        return self.distances_between_sensors