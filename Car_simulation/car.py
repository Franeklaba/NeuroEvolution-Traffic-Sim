import math

import pygame

from .config import CAR_CONFIG, CarConfig
from .raycastsensor import RaycastSensor


class Car(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], car_config: CarConfig = CAR_CONFIG):
        super().__init__()
        self.car_config = car_config

        self._base_sprite = pygame.Surface((40, 20), pygame.SRCALPHA)
        self._base_sprite.fill("Red")
        self.image = self._base_sprite

        self.pos_x, self.pos_y = position  # kod do zmiany wprzyszłosci nalezy urzyć Vector2
        self.pos = pygame.math.Vector2(position)
        self.direction_vector = pygame.math.Vector2((1, 0))

        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 0.0
        self.angle = 0.0

        self.sensors = [RaycastSensor(angle) for angle in self.car_config.sensors_angle]

    def __update_pos(self):  # kod do pozniejszego usunięcia
        keys = pygame.key.get_pressed()  # kod do pozniejszego usunięcia
        cfg = self.car_config
        if keys[pygame.K_w] and self.speed < cfg.max_speed:  # kod do pozniejszego usunięcia
            self.speed += cfg.acceleration  # kod do pozniejszego usunięcia
        elif keys[pygame.K_s] and self.speed > -cfg.max_speed:  # kod do pozniejszego usunięcia
            self.speed -= cfg.acceleration  # kod do pozniejszego usunięcia
        else:  # kod do pozniejszego usunięcia
            if self.speed > 0:  # kod do pozniejszego usunięcia
                self.speed -= cfg.acceleration / 2  # kod do pozniejszego usunięcia
            elif self.speed < 0:  # kod do pozniejszego usunięcia
                self.speed += cfg.acceleration / 2  # kod do pozniejszego usunięcia
        if keys[pygame.K_d]:  # kod do pozniejszego usunięcia
            self.angle -= cfg.angle_change  # kod do pozniejszego usunięcia
        elif keys[pygame.K_a]:  # kod do pozniejszego usunięcia
            self.angle += cfg.angle_change  # kod do pozniejszego usunięcia
        # kod do pozniejszego usunięcia
        self.pos_y += self.speed * math.sin(math.radians(self.angle))  # kod do pozniejszego usunięcia
        self.pos_x -= self.speed * math.cos(math.radians(self.angle))  # kod do pozniejszego usunięcia
        self.rect.centery = self.pos_y  # kod do pozniejszego usunięcia
        self.rect.centerx = self.pos_x  # kod do pozniejszego usunięcia

    def __update_sprite(self):
        self.image = pygame.transform.rotate(self._base_sprite, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def __sensors_managment(self, obsticles_group: pygame.sprite.Group):
        for i in range(self.car_config.num_of_sensors):
            point_pos = self.sensors[i].Get_colision_point(
                (self.pos_x, self.pos_y), self.angle, obsticles_group
            )
            # if point_pos:
            #     pygame.draw.line(screen, 'Green',(self.pos_x, self.pos_y) ,point_pos, 1)

    def update(self, obsticles_group: pygame.sprite.Group):
        self.__update_pos()
        self.__update_sprite()
        self.__sensors_managment(obsticles_group)
