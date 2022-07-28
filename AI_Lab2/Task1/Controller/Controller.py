

class Controller:
    def __init__(self, map, drone):
        self.map = map
        self.map1 = map
        self.drone = drone

    def valid_square(self,detectedMap, x, y):
        if x < 0 or y < 0 or x >= 20 or y >= 20:
            return False

        if detectedMap.surface[x][y] == -1 or detectedMap.surface[x][y] == 1:
            return False
        return True

    def heuristic(self,currentX, currentY, finalX, finalY):
        return (currentX - finalX) ** 2 + (currentY - finalY) ** 2

    def manhattan(self, currentX, currentY, finalX, finalY):
        return abs(currentX - finalX) + abs(currentY - finalY)

    def searchGreedy(self,initialX, initialY, finalX, finalY):

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
            self.map.surface[current_node[0]][current_node[1]] = -1

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

            if self.valid_square(self.map, current_node[0], current_node[1] + 1):
                children.append(
                    [current_node[0], current_node[1] + 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0], current_node[1] + 1, finalX, finalY)])
            if self.valid_square(self.map, current_node[0], current_node[1] - 1):
                children.append(
                    [current_node[0], current_node[1] - 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0], current_node[1] - 1, finalX, finalY)])
            if self.valid_square(self.map, current_node[0] + 1, current_node[1]):
                children.append(
                    [current_node[0] + 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0] + 1, current_node[1], finalX, finalY)])
            if self.valid_square(self.map, current_node[0] - 1, current_node[1]):
                children.append(
                    [current_node[0] - 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0] - 1, current_node[1], finalX, finalY)])

            for child in children:
                if child in closed_list:
                    continue
                if child not in open_list:
                    open_list.append(child)


    def searchAStar(self,initialX, initialY, finalX, finalY):

        visited = []
        unvisited = []

        start_node = [initialX, initialY, -1, -1, 0, 0, 0]
        unvisited.append(start_node)

        while len(unvisited) > 0:
            current_node = unvisited.pop(0)
            visited.append(current_node)
            self.map.surface[current_node[0]][current_node[1]] = -1

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

            if self.valid_square(self.map, current_node[0], current_node[1] + 1):
                children.append(
                    [current_node[0], current_node[1] + 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0], current_node[1] + 1, finalX, finalY),
                     current_node[4] + 1 + self.manhattan(current_node[0], current_node[1] + 1, finalX,
                                                                     finalY)])
            if self.valid_square(self.map, current_node[0], current_node[1] - 1):
                children.append(
                    [current_node[0], current_node[1] - 1, current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0], current_node[1] - 1, finalX, finalY),
                     current_node[4] + 1 + self.manhattan(current_node[0], current_node[1] - 1, finalX,
                                                                     finalY)])
            if self.valid_square(self.map, current_node[0] + 1, current_node[1]):
                children.append(
                    [current_node[0] + 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0] + 1, current_node[1], finalX, finalY),
                     current_node[4] + 1 + self.manhattan(current_node[0] + 1, current_node[1], finalX,
                                                                     finalY)])
            if self.valid_square(self.map, current_node[0] - 1, current_node[1]):
                children.append(
                    [current_node[0] - 1, current_node[1], current_node[0], current_node[1], current_node[4] + 1,
                     self.manhattan(current_node[0] - 1, current_node[1], finalX, finalY),
                     current_node[4] + 1 + self.manhattan(current_node[0] - 1, current_node[1], finalX,
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


    def dummysearch(self):
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]