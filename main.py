import pygame
import math

from sys import exit
pygame.init()

class Raycast_sensor():
    STEP_SIZE = 3
    MAX_DISTANCE = 1800
    def __init__(self, angle):
        self.angle = angle
    def Get_colision_point(self, start_pos, base_angle, obsticles_group: pygame.sprite.Group):
        angle = self.angle + base_angle
        base_x, base_y = start_pos
        for distance in range(0, self.MAX_DISTANCE, self.STEP_SIZE):
            curr_x = base_x - distance * math.sin(math.radians(angle))
            curr_y = base_y - distance * math.cos(math.radians(angle))

            for obstacle in obsticles_group:
                if obstacle.rect.collidepoint(curr_x, curr_y):
                    return (curr_x, curr_y)
        return None           



class Car(pygame.sprite.Sprite):
    ANGLE_CHANGE = 2
    MAX_SPEED = 8
    ACCELERATION = 0.05
    SPRITE = pygame.Surface((20, 40), pygame.SRCALPHA)
    SPRITE.fill('Red')
    SENSORS_ANGLE = [0, 20, 45, 90, 155, 180, 205, 270, 315 ,340]
    NUM_OF_SENSORS = len(SENSORS_ANGLE)
    def __init__(self, position):
        super().__init__()
        self.image = self.SPRITE

        self.pos_x, self.pos_y = position
        self.rect = self.image.get_rect(center = position)

        self.mask = pygame.mask.from_surface(self.image) 

        self.speed = 0.0
        self.angle = 30.0
        

        self.sensors = []
        for angle in self.SENSORS_ANGLE:
            self.sensors.append(Raycast_sensor(angle))

    def __update_pos(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.speed < self.MAX_SPEED:
            self.speed += self.ACCELERATION
        elif keys[pygame.K_s] and self.speed > - self.MAX_SPEED:
            self.speed -= self.ACCELERATION
        else:
            if self.speed > 0:
                self.speed -= self.ACCELERATION / 2
            elif self.speed < 0:
                self.speed += self.ACCELERATION / 2
        if keys[pygame.K_d]:
            self.angle -= self.ANGLE_CHANGE
        elif keys[pygame.K_a]:
            self.angle += self.ANGLE_CHANGE
        
        self.pos_y -= self.speed * math.cos(math.radians(self.angle))
        self.pos_x -= self.speed * math.sin(math.radians(self.angle))
        self.rect.centery = self.pos_y
        self.rect.centerx = self.pos_x

    def __update_sprite(self):
        self.image = pygame.transform.rotate(self.SPRITE, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image) 

    def __sensors_managment(self, obsticles_group: pygame.sprite.Group):
        for i in range(self.NUM_OF_SENSORS):
            point_pos = self.sensors[i].Get_colision_point((self.pos_x, self.pos_y), self.angle, obsticles_group)
            if point_pos:    
                pygame.draw.line(screen, 'Green',(self.pos_x, self.pos_y) ,point_pos, 1)

    
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



class Game():
    WINDOW_WIDTH = 1600
    WINDOW_HEIFHT = 1000
    CARS_POSITION = [()]
    NUM_OF_CARS = 8

    pass

screen = pygame.display.set_mode((1600,1000))
background_color = (30, 30, 30) 
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()




car = pygame.sprite.GroupSingle()
car.add(Car((200,200)))

obsticles = pygame.sprite.Group()
obsticles.add(Obsticle(0, 0, 1600, 20))    
obsticles.add(Obsticle(0, 980, 1600, 20))  
obsticles.add(Obsticle(0, 0, 20, 1000))    
obsticles.add(Obsticle(1580, 0, 20, 1000)) 

obsticles.add(Obsticle(400, 300, 200, 50)) 
obsticles.add(Obsticle(1000, 500, 50, 300))
obsticles.add(Obsticle(750, 700, 100, 100))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill(background_color)
    car.draw(screen)
    car.update(obsticles)
    if pygame.sprite.spritecollide(car.sprite, obsticles, False, pygame.sprite.collide_mask):
        car.sprite.speed = 0  
        print("Kolizja!")
    obsticles.draw(screen)

    pygame.display.update()
    clock.tick(30)