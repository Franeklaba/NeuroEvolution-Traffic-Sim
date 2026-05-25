import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
from .car import Car
from .obsticle import Obsticle
from .destinationpoint import DestinationPoint

from .simulationconfig import SIMULATION_CONFIG, SimulationConfig

from sys import exit

class CarSimulationMenager():
    def __init__(self, ml_input_type, is_trainig_mode: bool=False, config: SimulationConfig = SIMULATION_CONFIG):
        self.config = config 
        self.is_training_mode = is_trainig_mode
        self.ml_input_type = ml_input_type

        if self.is_training_mode:
            import os
            os.environ['SDL_VIDEODRIVER'] = 'dummy' 
            pygame.display.init() 
            self.screen = None
        else:
            pygame.init()
            self.screen = pygame.display.set_mode((self.config.window_width, self.config.window_height))
            self.clock = pygame.time.Clock()
        
        self.obsticles_group = pygame.sprite.Group()
        self.active_cars_group = pygame.sprite.Group()
        self.dest_points_group = pygame.sprite.Group()
        self.score = 0
        self.reset()
        
    def reset(self, map_type="slalom"):
        self.active_cars_group.empty()
        self.dest_points_group.empty()
        self.obsticles_group.empty()
        self.score = 0

        for obsticle in self.config.obsticles_pos(map_type):
            self.obsticles_group.add(Obsticle(*obsticle)) 

        dest_and_col = self.config.cars_destination_points_and_color(map_type)
        
        for i, car_pos_and_angle in enumerate(self.config.cars_position_and_angle(map_type)): 
            dest_pos, col = dest_and_col[i] 
            new_dest_point = DestinationPoint(dest_pos, col, self.config.car.dest_point_rect)
            self.dest_points_group.add(new_dest_point)
            self.active_cars_group.add(Car(car_pos_and_angle, new_dest_point, self.ml_input_type, self.config.car))

        for car in self.active_cars_group:
            car.take_observations(self.obsticles_group, self.active_cars_group)
        
        

    def colosion_menagment(self, frame): 
        active_cars = list(self.active_cars_group)
        
        for car in active_cars:
            if not car.alive():
                continue
            if pygame.sprite.spritecollideany(car, self.obsticles_group, pygame.sprite.collide_mask):
                self.score += car.car_score(colision=True)
                car.kill()
                continue  
            if pygame.sprite.collide_mask(car, car.dest_point):
                self.score += car.car_score(max_sim_time=self.config.simulation_time, time=frame, win=True)
                car.kill()
                continue 
            hit_cars = pygame.sprite.spritecollide(car, self.active_cars_group, False, pygame.sprite.collide_mask)
            
            if len(hit_cars) > 1:
                self.score += car.car_score(colision=True)
                car.kill()
                
                for other_car in hit_cars:
                    if other_car != car and other_car.alive():
                        self.score += other_car.car_score(colision=True)
                        other_car.kill()

    #TODO mozna pomyslec o dodaniu błędu gdy metoda ta zostanie wykonana przed koncem gry 
    def get_score(self):
        for car in self.active_cars_group:
            self.score += car.car_score()
        return self.score
    
    def get_ml_input(self):
        return [car.current_observation for car in self.active_cars_group]

    def step(self, frame, actions_matrix):
        #TODO przekminic wyswietlanie 
        if not self.is_training_mode:#nieprzewidzane zachowanie 
            self.__draw()       #nieprzewidzane zachowanie 
            for event in pygame.event.get():        #nieprzewidzane zachowanie 
                if event.type == pygame.QUIT:       #nieprzewidzane zachowanie 
                    pygame.quit()
                    exit()      #nieprzewidzane zachowanie 
            self.clock.tick(self.config.clock_tick)
        
        for i, car in enumerate(self.active_cars_group):
            car.update(self.obsticles_group, self.active_cars_group, actions_matrix[i], self.screen)
        self.colosion_menagment(frame)

    def __draw(self):
        self.dest_points_group.draw(self.screen)
        self.active_cars_group.draw(self.screen)
        self.obsticles_group.draw(self.screen)
        pygame.display.update()
        self.screen.fill(self.config.background_color)

    def is_active(self):
        return bool(self.active_cars_group)
        


    def quit(self):
        pygame.quit()
       