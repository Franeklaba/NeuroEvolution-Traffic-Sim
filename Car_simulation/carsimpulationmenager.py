import pygame
import random
from .car import Car
from .obsticle import Obsticle
from .destinationpoint import DestinationPoint

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
        
        self.active_cars_group = pygame.sprite.Group()
        self.dest_points_group = pygame.sprite.Group()


        self.score = 0

        dest_and_col = self.config.cars_destination_points_and_color
        random.shuffle(dest_and_col) #-> !!!! IMPORTANT IF we want to dest points be random for cars or not 
        
        
        #TODO zaimplementować wyjątek polegającym na tym ze jest zbyt mało miejsc docelowych by rozdysponować je samochodom 
        
        for car_pos in self.config.cars_position: 
            dest_pos, col = dest_and_col.pop() 
            new_dest_point = DestinationPoint(dest_pos, col, self.config.car.dest_point_rect)
            self.dest_points_group.add(new_dest_point)
            self.active_cars_group.add(Car(car_pos, new_dest_point, self.config.car))

        self.obsticles_group = pygame.sprite.Group()
        for obsticle in self.config.obsticles_pos:
            self.obsticles_group.add(Obsticle(*obsticle)) 
    



    def reset(self):
        self.active_cars_group.empty()
        self.dest_points_group.empty()

        self.score = 0

        dest_and_col = self.config.cars_destination_points_and_color
        random.shuffle(dest_and_col) #-> !!!! IMPORTANT IF we want to dest points be random for cars or not 
        
        for car_pos in self.config.cars_position: 
            dest_pos, col = dest_and_col.pop() 
            new_dest_point = DestinationPoint(dest_pos, col, self.config.car.dest_point_rect)
            self.dest_points_group.add(new_dest_point)
            self.active_cars_group.add(Car(car_pos, new_dest_point, self.config.car))

    def colosion_menagment(self, frame_counter): #funkcja na razie zakłada ze na mapie znajduje sie jeden samochod wiec kolizja miedzy pojazdami nie wystepuje 
        
        #TODO miejsce na zrealizowanie kolizji między samochodkami które powinny być sprawdzo przed kolizjiami samochodow ze scianami 
        
        for car in self.active_cars_group:
            if pygame.sprite.spritecollide(car, self.obsticles_group, False, pygame.sprite.collide_mask):
                self.score += car.car_score(colision=True)
                car.kill()
            elif pygame.sprite.collide_mask(car, car.dest_point):
                self.score += car.car_score(time=frame_counter,win=True)
                car.kill()
        

    

    def run(self):
        for frame_counter in range(self.config.simulation_time):
            if not self.is_training_mode:
                self.__draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                self.clock.tick(self.config.clock_tick)

            self.active_cars_group.update(self.obsticles_group, self.active_cars_group, self.screen)
            self.colosion_menagment(frame_counter)

            if not self.active_cars_group:
                break
        

    def __draw(self):
        self.dest_points_group.draw(self.screen)
        self.active_cars_group.draw(self.screen)
        self.obsticles_group.draw(self.screen)
        pygame.display.update()
        self.screen.fill(self.config.background_color)




    def quit(self):
        pygame.quit()
       