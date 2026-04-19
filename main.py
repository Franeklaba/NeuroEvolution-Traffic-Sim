import pygame
import math

from sys import exit

class RaycastSensor():
    STEP_SIZE = 3
    RANGE = 1800
    def __init__(self, angle):
        self.angle = angle

    def _get_distance(point_a, point_b):
        a_x, a_y = point_a
        b_x, b_y = point_b
        # return math.sqrt(pow(a_x - b_x, 2) + pow(b_x - b_y, 2))
    
    def Get_colision_point(self, start_pos, base_angle, obsticles_group: pygame.sprite.Group):
        angle = self.angle + base_angle
        base_x, base_y = start_pos
        end_x = base_x - self.RANGE * math.sin(math.radians(angle))
        end_y = base_y - self.RANGE * math.cos(math.radians(angle))

        # for obstacle in obsticles_group:
        #         if obstacle.rect.collidepoint(curr_x, curr_y):
        #             return (curr_x, curr_y)
        return None           



class Car(pygame.sprite.Sprite):
    ANGLE_CHANGE = 2
    MAX_SPEED = 8
    ACCELERATION = 0.05
    SPRITE = pygame.Surface((40, 20), pygame.SRCALPHA)
    SPRITE.fill('Red')
    SENSORS_ANGLE = [0, 20, 45, 90, 155, 180, 205, 270, 315 ,340]
    NUM_OF_SENSORS = len(SENSORS_ANGLE)
    def __init__(self, position):
        super().__init__()
        self.image = self.SPRITE

        self.pos_x, self.pos_y = position #kod do zmiany wprzyszłosci nalezy urzyć Vector2
        self.pos = pygame.math.Vector2(position)
        self.direction_vector = pygame.math.Vector2((1,0))

        self.rect = self.image.get_rect(center = position)
        self.mask = pygame.mask.from_surface(self.image) 

        self.speed = 0.0
        self.angle = 0.0
        

        self.sensors = []
        for angle in self.SENSORS_ANGLE:
            self.sensors.append(RaycastSensor(angle))

    def __update_pos(self):                                                        #kod do pozniejszego usunięcia
        keys = pygame.key.get_pressed()                                                                #kod do pozniejszego usunięcia
        if keys[pygame.K_w] and self.speed < self.MAX_SPEED:                               #kod do pozniejszego usunięcia
            self.speed += self.ACCELERATION                            #kod do pozniejszego usunięcia
        elif keys[pygame.K_s] and self.speed > - self.MAX_SPEED:                               #kod do pozniejszego usunięcia
            self.speed -= self.ACCELERATION                            #kod do pozniejszego usunięcia
        else:                              #kod do pozniejszego usunięcia
            if self.speed > 0:                             #kod do pozniejszego usunięcia
                self.speed -= self.ACCELERATION / 2                            #kod do pozniejszego usunięcia
            elif self.speed < 0:                               #kod do pozniejszego usunięcia
                self.speed += self.ACCELERATION / 2                            #kod do pozniejszego usunięcia
        if keys[pygame.K_d]:                               #kod do pozniejszego usunięcia
            self.angle -= self.ANGLE_CHANGE                            #kod do pozniejszego usunięcia
        elif keys[pygame.K_a]:                             #kod do pozniejszego usunięcia
            self.angle += self.ANGLE_CHANGE                            #kod do pozniejszego usunięcia
                                    #kod do pozniejszego usunięcia
        self.pos_y += self.speed * math.sin(math.radians(self.angle))                              #kod do pozniejszego usunięcia
        self.pos_x -= self.speed * math.cos(math.radians(self.angle))                              #kod do pozniejszego usunięcia
        self.rect.centery = self.pos_y                             #kod do pozniejszego usunięcia
        self.rect.centerx = self.pos_x                             #kod do pozniejszego usunięcia

    def __update_sprite(self):
        self.image = pygame.transform.rotate(self.SPRITE, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image) 

    def __sensors_managment(self, obsticles_group: pygame.sprite.Group):
        for i in range(self.NUM_OF_SENSORS):
            point_pos = self.sensors[i].Get_colision_point((self.pos_x, self.pos_y), self.angle, obsticles_group)
            # if point_pos:    
            #     pygame.draw.line(screen, 'Green',(self.pos_x, self.pos_y) ,point_pos, 1)

    
    def update(self, obsticles_group: pygame.sprite.Group):
        self.__update_pos()
        self.__update_sprite()
        self.__sensors_managment(obsticles_group)


class Obsticle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill('White')
        self.rect = self.image.get_rect(topleft = (x, y))    
        self.mask = pygame.mask.from_surface(self.image) 



WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000
NUM_OF_CARS = 14
BACKGROUND_COLOR = (30, 30, 30) 
CLOCK_TICK = 30
LEARNING_MODE = False

class CarSimulationMenager():
    CARS_POSITION = [(WINDOW_WIDTH - 70, WINDOW_HEIGHT - 80 - i * 60) for i in range(NUM_OF_CARS)]
    OBSTICLES_POS = [(0, 0, 1600, 20), (0, 980, 1600, 20), (0, 0, 20, 1000), (1580, 0, 20, 1000), 
                (400, 300, 200, 50), (1000, 500, 50, 300), (750, 700, 100, 100)]
    
    def __init__(self):
        if(LEARNING_MODE):
            import os
            os.environ['SDL_VIDEODRIVER'] = 'dummy' 
            pygame.display.init() 
            self.screen = pygame.display.set_mode((1600,1000))
        else:
            pygame.init()
            self.screen = pygame.display.set_mode((1600,1000))
            self.clock = pygame.time.Clock()

        self.cars_group = pygame.sprite.Group()
        for car_pos in self.CARS_POSITION:
            self.cars_group.add(Car(car_pos)) 

        self.obsticles_group = pygame.sprite.Group()
        for obsticle in self.OBSTICLES_POS:
            self.obsticles_group.add(Obsticle(*obsticle)) 
    
    def run(self):
        while 1:
            for event in pygame.event.get():        #kod do pozniejszego usuniecia 
                if event.type == pygame.QUIT:       #kod do pozniejszego usuniecia 
                    pygame.quit()       #kod do pozniejszego usuniecia 
                    exit()                              #kod do pozniejszego usuniecia         
            if(not LEARNING_MODE):
                self.__draw()
                #self.clock.tick(CLOCK_TICK)

            self.cars_group.update(self.obsticles_group)

    def __draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.cars_group.draw(self.screen)
        self.obsticles_group.draw(self.screen)
        pygame.display.update()

        

        
game = CarSimulationMenager()
game.run()