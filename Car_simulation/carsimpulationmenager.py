import pygame
from .car import Car
from .obsticle import Obsticle
from .config import SIMULATION_CONFIG, SimulationConfig

from sys import exit

class CarSimulationMenager():
    def __init__(self, config: SimulationConfig = SIMULATION_CONFIG):
        self.config = config
    
        if self.config.learning_mode:
            import os
            os.environ['SDL_VIDEODRIVER'] = 'dummy' 
            pygame.display.init() 
            self.screen = pygame.display.set_mode((self.config.window_width, self.config.window_height))
        else:
            pygame.init()
            self.screen = pygame.display.set_mode((self.config.window_width, self.config.window_height))
            self.clock = pygame.time.Clock()

        self.cars_group = pygame.sprite.Group()
        for car_pos in self.config.cars_position:
            self.cars_group.add(Car(car_pos, self.config.car))

        self.obsticles_group = pygame.sprite.Group()
        for obsticle in self.config.obsticles_pos:
            self.obsticles_group.add(Obsticle(*obsticle)) 
    
    def run(self):
        while 1:
            for event in pygame.event.get():        #kod do pozniejszego usuniecia 
                if event.type == pygame.QUIT:       #kod do pozniejszego usuniecia 
                    pygame.quit()       #kod do pozniejszego usuniecia 
                    exit()                              #kod do pozniejszego usuniecia         
            if not self.config.learning_mode:
                self.__draw()
                #self.clock.tick(CLOCK_TICK)

            self.cars_group.update(self.obsticles_group)

    def __draw(self):
        self.screen.fill(self.config.background_color)
        self.cars_group.draw(self.screen)
        self.obsticles_group.draw(self.screen)
        pygame.display.update()

       