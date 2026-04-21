import pygame
from .car import Car
from .obsticle import Obsticle
from .config import SIMULATION_CONFIG, SimulationConfig

from sys import exit

class CarSimulationMenager():
    def __init__(self, is_trainig_mode :bool, config: SimulationConfig = SIMULATION_CONFIG):
        self.config = config
        self.is_training_mode = is_trainig_mode

        if self.is_training_mode:
            import os
            os.environ['SDL_VIDEODRIVER'] = 'dummy' 
            pygame.display.init() 
            self.screen = None
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
        for _ in range(self.config.simulation_time):
            if not self.is_training_mode:
                self.__draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                self.clock.tick(self.config.clock_tick)

            self.cars_group.update(self.obsticles_group, self.cars_group, self.screen)
        

        pygame.quit()
        exit()

    def __draw(self):
        self.cars_group.draw(self.screen)
        self.obsticles_group.draw(self.screen)
        pygame.display.update()
        self.screen.fill(self.config.background_color)


       