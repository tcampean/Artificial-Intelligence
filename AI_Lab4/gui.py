import pygame
from controller import *
from utils import *
from pygame.constants import KEYDOWN


class GUI:
    def __init__(self, service):
        self.initPygame()
        self.screen = pygame.display.set_mode((400, 400))
        self.screen.fill(WHITE)
        self.service = service

    def getMapSurface(self):
        return self.service.getMapSurface()

    def initPygame(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("ACO")

    def get_image(self, colour = BLUE, background = WHITE):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        sensor = pygame.Surface((20, 20))
        brick.fill(colour)
        image.fill(background)
        sensor.fill(GREEN)

        surface = self.service.getMapSurface()
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if surface[i][j] == 1:
                    image.blit(brick, (j * 20, i * 20))
                elif surface[i][j] == SENSOR_POSITION:
                    image.blit(sensor, (j * 20, i * 20))

        return image

    def print_image(self):
        drone_image = pygame.image.load("drone.png")
        path_image = self.get_image()
        path_image.blit(drone_image, (self.service.getDroneYCoord() * 20, self.service.getDroneXCoord() * 20))
        self.screen.blit(path_image, (0, 0))
        pygame.display.update()
        return drone_image, path_image

    def start(self):
        self.service.run()
        self.print_image()
        pygame.time.wait(100000)
