import math
import pygame
from .simulationconfig import CAR_CONFIG, CarConfig
from .raycastsensor import RaycastSensor
from .destinationpoint import DestinationPoint


class Car(pygame.sprite.Sprite):
    def __init__(self, position_and_angle: tuple[int, int], dest_point: DestinationPoint, car_config: CarConfig = CAR_CONFIG):
        super().__init__()
        position, angle = position_and_angle
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
        self.angle = angle
        self.direction_vector.from_polar((1, 0 - self.angle))



        self.sensors = [RaycastSensor(angle, car_config.sensor) for angle in self.car_config.sensors_angle]

        self._start_dist_to_dest_point = self.dist_to_dest_point

    @property
    def dist_to_dest_point(self):
        return  self.pos.distance_to(self.dest_point.pos)
    @property 
    def angle_to_dest_point(self):
        target_vector = self.dest_point.pos - self.pos
        if target_vector.length() > 0:
            return self.direction_vector.angle_to(target_vector)
        return 0.0
        

    def _update_pos(self, actions): #
        cfg = self.car_config
        if actions[1] and self.speed < cfg.max_speed:  # kod do pozniejszego usunięcia
            self.speed += cfg.acceleration  # kod do pozniejszego usunięcia
        else:  
            if self.speed > 0:
                self.speed -= cfg.acceleration * 2
            
            if self.speed < 0:
                self.speed = 0

        self.angle += actions[0] * cfg.angle_change
        self.direction_vector.from_polar((1, 0 - self.angle))
        self.pos += self.direction_vector * self.speed
        self.rect.center = self.pos

    def _update_sprite(self):
        self.image = pygame.transform.rotate(self._base_sprite, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    def _draw_sensors(self, distacnce_to_obsticle, obsticle_col_point, car_col_point, screen, is_car):
        current_color = 'Green'   
        if distacnce_to_obsticle > 0:
            pygame.draw.circle(screen, current_color, obsticle_col_point, 3)
        if is_car:
            pygame.draw.line(screen, "White", self.pos, car_col_point, 4)
        pygame.draw.line(screen, current_color, self.pos, obsticle_col_point, 1)
    
        if distacnce_to_obsticle > 0:
            pygame.draw.circle(screen, current_color, obsticle_col_point, 3)


    def _get_ml_sensor_input(self, measur):
        norm_cfg = self.car_config.ml_input_norm
        ml_sensor_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj in measur:
            dead_zone = norm_cfg.dead_zone_base + (abs(self.speed) * norm_cfg.dead_zone_speed_weight) + (sensor_range * norm_cfg.dead_zone_range_weight)

            if dead_zone >= sensor_range:
                dead_zone = sensor_range - norm_cfg.dead_zone_margin

            standardized_data = (sensor_range - distance_to_obsticle) / (sensor_range - dead_zone)
            standardized_data = max(0.0, min(1.0, standardized_data))
            standardized_data = standardized_data ** norm_cfg.sensor_data_exponent
            ml_sensor_input.append(standardized_data)

        return ml_sensor_input
    def _get_ml_nav_input(self):
        norm_cfg = self.car_config.ml_input_norm
        norm_distance = min(1.0, self.dist_to_dest_point / norm_cfg.max_nav_distance)
        norm_angle = self.angle_to_dest_point / norm_cfg.max_nav_angle
        return [norm_distance, norm_angle]
        
    def _get_ml_input(self, measur): # aktualnie funckcja ta przetwarza jedynie wejście z czujnika ścian zakładamy ze na planszy jest tylko jeden samochod 
        sensor_data = self._get_ml_sensor_input(measur)
        navigation_data = self._get_ml_nav_input()

        ml_input = sensor_data + navigation_data        
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
        

    def update(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, actions, screen):
        if screen is not None:
            self._update_sprite()
        self._update_pos(actions)
        self.take_observations(obsticles_group, cars_group, screen)

    #TODO funckja wymaga dopracowania przedstawiono dopiero szkielet 
    def car_score(self, time=0, colision=False, win=False):
        score_cfg = self.car_config.score
        result = 0
        if(not colision):
            result = score_cfg.no_collision_reward
        dist_diff = self._start_dist_to_dest_point - self.dist_to_dest_point
        result = max(score_cfg.min_distance_score, result + dist_diff)

        if win:
            result += max(score_cfg.win_base_reward, score_cfg.win_distance_multiplier * self._start_dist_to_dest_point - (time**1.1))

        return result
    
    def take_observations(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, screen = None):
        sesor_mesur = self._sensors_managment(obsticles_group, cars_group, screen)
        self.current_observation = self._get_ml_input(sesor_mesur)
