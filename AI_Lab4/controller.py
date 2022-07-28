from sensors import *
from domain import *

class Controller:
    def __init__(self,drone,map):
        self.surface = map
        self.drone = drone
        self.sensors = Sensors(self.surface)
        self.pheromones = [[1.0 for i in range(SENSOR_COUNT)] for i in range(SENSOR_COUNT)]
        self.distances = self.sensors.get_distance_between_sensors()

    def move_ants(self, ants, alpha, beta, q0):
        ant_lives = [True for _ in ants]
        for i in range(len(ants)):
            ant = ants[i]
            for step in range(SENSOR_COUNT-1):
                found = ant.next_move(self.distances, self.pheromones, q0, alpha, beta)
                if not found:
                    ant_lives[i] = False
                    break

        alive_ants=[]
        for i in range(len(ants)):
            if ant_lives[i]:
                ants[i].compute_fitness(self.distances)
                alive_ants.append(ants[i])
        return alive_ants

    def get_best_ant(self, ants):
        best_ant = None
        best_fitness = INFINITY

        for ant in ants:
            if best_fitness > ant.get_fitness():
                best_fitness = ant.get_fitness()
                best_ant = ant
        return best_ant

    def sim_epoch(self, nrAnts, alpha, beta, q0, rho):
        ants = [Ant() for i in range(nrAnts)]

        ants = self.move_ants(ants, alpha, beta, q0)

        for i in range(SENSOR_COUNT):
            for j in range(SENSOR_COUNT):
                self.pheromones[i][j] = (1 - rho) * self.pheromones[i][j]

        if not ants:
            return None

        new_pheromones = [1.0 / ant.get_fitness() for ant in ants]
        for i in range(len(ants)):
            current = ants[i].get_path()
            for j in range(len(current)-1):
                current_sensor = current[j]
                next_sensor = current[j+1]
                self.pheromones[current_sensor][next_sensor] += new_pheromones[i]

        return self.get_best_ant(ants)

    def charge_sensor(self, remaining_battery, accessible_sensors):
        sensors = []
        for i in range(len(self.sensors.get_sensor_list())):
            if i in accessible_sensors:
                sensors.append(self.sensors.get_sensor_list()[i])

        energy_levels = [0 for i in sensors]
        if remaining_battery <= 0:
            return energy_levels

        sensors.sort(key=lambda s: (s.get_positions()[-1] / s.get_max_energy()))
        i = 0
        while i < len(sensors) and remaining_battery > 0:
            current_sensor_max_energy = sensors[i].get_max_energy()
            if remaining_battery > current_sensor_max_energy:
                remaining_battery -= current_sensor_max_energy
                energy_levels[i] = current_sensor_max_energy
            else:
                energy_levels[i] = remaining_battery
                remaining_battery = 0
            i += 1
        return energy_levels

    def update_best_solution(self, best_solution):
        curr_solution = self.sim_epoch(ANT_COUNT, ALPHA, BETA, Q0, RHO)
        if curr_solution is None:
            return best_solution

        current_solution_lenght = len(curr_solution.get_path())
        if best_solution is None or current_solution_lenght > len(best_solution.get_path()) \
                or (current_solution_lenght == len(best_solution.get_path()) and curr_solution.get_fitness() < best_solution.get_fitness()):
            return curr_solution
        return best_solution

    def run(self):
        best_solution = None

        for epoch in range(EPOCH_COUNT):
            best_solution = self.update_best_solution(best_solution)

        energyLevels = self.charge_sensor(BATTERY - best_solution.get_fitness(), best_solution.get_path())
        print("Sensor order: ")
        for indices in best_solution.get_path():
            print(self.sensors.get_sensor_list()[indices].get_coordinates(), end=" ")
        print("\nEnergy in each sensor: ", energyLevels)

    def getMap(self):
        return self.surface

    def setMap(self, dmap):
        self.surface = dmap

    def getMapSurface(self):
        return self.surface.surface

    def getDroneXCoord(self):
        return self.drone.getX()

    def getDroneYCoord(self):
        return self.drone.getY()