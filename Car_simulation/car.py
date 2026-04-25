import math
import pygame
from .config import CAR_CONFIG, CarConfig
from .raycastsensor import RaycastSensor
from .destinationpoint import DestinationPoint


class Car(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], dest_point: DestinationPoint, car_config: CarConfig = CAR_CONFIG):
        super().__init__()
        self.car_config = car_config
        self.dest_point:DestinationPoint = dest_point
        
        self._base_sprite = pygame.Surface((25, 20), pygame.SRCALPHA)
        self._base_sprite.fill(dest_point.color)
        self.image = self._base_sprite

        self.current_observation = list()

        self.pos = pygame.math.Vector2(position)
        self.direction_vector = pygame.math.Vector2((1, 0))

        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 0.0
        self.angle = 0.0

        self.sensors = [RaycastSensor(angle) for angle in self.car_config.sensors_angle]

        self.counter = 0 # KOD TYMCZASOWY DO TESTOWANIA funkcji _get_ml_input
    @property
    def dist_to_dest_point(self):
        return  self.pos.distance_to(self.dest_point.pos)
    @property 
    def angle_to_dest_point(self):
        target_vector = self.dest_point.pos - self.pos
        if target_vector.length() > 0:
            return self.direction_vector.angle_to(target_vector)
        return 0.0
        

    def _update_pos(self):  
        keys = pygame.key.get_pressed()  # kod do pozniejszego usunięcia
        cfg = self.car_config
        if keys[pygame.K_w] and self.speed < cfg.max_speed:  # kod do pozniejszego usunięcia
            self.speed += cfg.acceleration  # kod do pozniejszego usunięcia
        else:  # kod do pozniejszego usunięcia
            if self.speed > 0:  # kod do pozniejszego usunięcia
                self.speed -= cfg.acceleration  # kod do pozniejszego usunięcia
            else:
                self.speed = 0
        if keys[pygame.K_d]:  # kod do pozniejszego usunięcia
            self.angle -= cfg.angle_change  # kod do pozniejszego usunięcia
        elif keys[pygame.K_a]:  # kod do pozniejszego usunięcia
            self.angle += cfg.angle_change  # kod do pozniejszego usunięcia


        self.direction_vector.from_polar((1, 0 - self.angle))
        self.pos += self.direction_vector * self.speed
        self.rect.center = self.pos

    def _update_sprite(self):
        self.image = pygame.transform.rotate(self._base_sprite, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    def _draw_sensors(self, distacnce_to_obsticle, obsticle_col_point, car_col_point, screen, is_car):
        current_color = 'Green'      # Krytycznie blisko - kolizja jest niemal pewna
        
        if distacnce_to_obsticle > 0:
            pygame.draw.circle(screen, current_color, obsticle_col_point, 3)

        
        if is_car:
            pygame.draw.line(screen, "White", self.pos, car_col_point, 4)
        pygame.draw.line(screen, current_color, self.pos, obsticle_col_point, 1)
        

        
        if distacnce_to_obsticle > 0:
            pygame.draw.circle(screen, current_color, obsticle_col_point, 3)


    def _get_ml_sensor_input(self, measur):
        ml_sensor_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj in measur:
            dead_zone = 15 + (abs(self.speed) * 2.0) + (sensor_range * 0.1)

            if dead_zone >= sensor_range:
                dead_zone = sensor_range - 1.0

            standardized_data = (sensor_range - distance_to_obsticle) / (sensor_range - dead_zone)
            standardized_data = max(0.0, min(1.0, standardized_data))
            standardized_data = standardized_data ** 1.5
            ml_sensor_input.append(standardized_data)

        return ml_sensor_input
    def _get_ml_nav_input(self):
        MAX_DIST = 2000.0 
        norm_distance = min(1.0, self.dist_to_dest_point / MAX_DIST)
        norm_angle = self.angle_to_dest_point / 180
        return [norm_distance, norm_angle]
        
    def _get_ml_input(self, measur): # aktualnie funckcja ta przetwarza jedynie wejście z czujnika ścian zakładamy ze na planszy jest tylko jeden samochod 
        sensor_data = self._get_ml_sensor_input(measur)
        navigation_data = self._get_ml_nav_input()

        ml_input = sensor_data + navigation_data

        # if self.counter % 50 == 0: #kod do debugowania 
        #     print(f"Dist: {self.dist_to_dest_point} | Norm_dist: {navigation_data[0]:.2f} | Angle: {self.angle_to_dest_point:.1f} | Norm_angle: {navigation_data[1]:.2f}")
        self.counter += 1

        return ml_input


    def _sensors_managment(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, screen = None):
        measurement = list()
        for i in range(self.car_config.num_of_sensors):
            distance_to_obsticle, distance_to_another_car, sensor_range, car_obj, obsticle_col_point, car_col_point = \
            self.sensors[i].get_sensor_data(self.pos, self.direction_vector, obsticles_group, cars_group, self.speed, self)

            if screen: 
                self._draw_sensors(distance_to_obsticle, obsticle_col_point, car_col_point, screen, not(car_obj == None))

            measurement.append((distance_to_obsticle, distance_to_another_car, sensor_range, car_obj))
        return measurement                
        
    #TODO napisać obsluge kolizji  dla klasy CAR 
    def colision_menagment(self):
        pass
        

    def update(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, screen):
        if screen is not None:
            self._update_pos()

        self._update_sprite()
        sesor_mesur = self._sensors_managment(obsticles_group, cars_group, screen)
        self.current_observation = self._get_ml_input(sesor_mesur)
        self.colision_menagment()



    #TODO napisać funckje fittingu dla klasy CAR w danym stacie 
    def fitting(self):
        pass