from gui import *

def main():
    map = Map()
    drone = Drone(0,0)
    posX, posY = random.randint(0, MAP_HEIGHT), random.randint(0, MAP_WIDTH)
    while map.surface[posX][posY] == 1:
        posX, posY = random.randint(0, MAP_HEIGHT), random.randint(0, MAP_WIDTH)
    drone.setCoords(posX, posY)
    service = Controller(drone,map)
    ui = GUI(service)
    ui.start()


if __name__ == "__main__":
    main()
