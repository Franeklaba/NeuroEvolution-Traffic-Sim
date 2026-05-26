import math
import pygame
from .simulationconfig import CAR_CONFIG, CarConfig
from .raycastsensor import RaycastSensor
from .destinationpoint import DestinationPoint


class Car(pygame.sprite.Sprite):
    def __init__(self, position_and_angle: tuple[int, int], dest_point: DestinationPoint, ml_input_type, car_config: CarConfig = CAR_CONFIG):
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
        self._min_dist_to_dest_point = self.dist_to_dest_point
        self.ml_input_type = ml_input_type

        self.last_progress_timer = 0


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
        self.speed += cfg.acceleration * actions[1]
        self.speed = min(self.speed, cfg.max_speed)
        self.speed = max(self.speed, 0)

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

    def _get_ml_sensor_input_1(self, measur):
        ml_sensor_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj,obsticle_col_point in measur:
            standardized_data = 1.0 - (min(distance_to_obsticle, distance_to_another_car) / sensor_range)
            standardized_data = max(0.0, min(1.0, standardized_data))
            ml_sensor_input.append(standardized_data)
        return ml_sensor_input
    
    def _get_ml_sensor_input_2(self, measur):
        ml_sensor_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj,obsticle_col_point in measur:
            wall_sensor_data = 1.0 - (distance_to_obsticle / sensor_range)
            wall_sensor_data = max(0.0, min(1.0, wall_sensor_data))
            car_sensor_data = 1.0 - (distance_to_another_car / sensor_range)
            car_sensor_data = max(0.0, min(1.0, car_sensor_data))
            ml_sensor_input.append(wall_sensor_data)
            ml_sensor_input.append(car_sensor_data)
        return ml_sensor_input

    def _get_closure_rate(self, other_car: 'Car' = None, wall: bool = False, wall_pos: tuple[float, float] = (0, 0)) -> float:
        v_self = self.direction_vector * self.speed
        if wall:
            v_other = pygame.math.Vector2(0, 0) 
            target_pos = pygame.math.Vector2(wall_pos)
        else:
            if other_car is None:
                return 0.0 
            v_other = other_car.direction_vector * other_car.speed
            target_pos = other_car.pos
        v_rel = v_self - v_other
    
        pos_diff = target_pos - self.pos
        if pos_diff.length_squared() == 0:
            return 0.0 
        dir_to_target = pos_diff.normalize()
        closure_rate = v_rel.dot(dir_to_target)
        max_possible_rate = 1.8 * self.car_config.max_speed
        normalized_rate = closure_rate / max_possible_rate
        return max(-1.0, min(1.0, normalized_rate))
    
    def _get_ml_sensor_input_3(self, measur):
        ml_sensor_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj,obsticle_col_point in measur:
            wall_sensor_data = 1.0 - (distance_to_obsticle / sensor_range)
            wall_sensor_data = max(0.0, min(1.0, wall_sensor_data))
            car_sensor_data = 1.0 - (distance_to_another_car / sensor_range)
            car_sensor_data = max(0.0, min(1.0, car_sensor_data))
            closure_rate = self._get_closure_rate(other_car=car_obj)
            ml_sensor_input.append(wall_sensor_data)
            ml_sensor_input.append(car_sensor_data)
            ml_sensor_input.append(closure_rate)
        return ml_sensor_input

    def _get_ml_sensor_input_4(self, measur):
        ml_sensor_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj, obsticle_col_point in measur:
            wall_sensor_data = 1.0 - (distance_to_obsticle / sensor_range)
            wall_sensor_data = max(0.0, min(1.0, wall_sensor_data))
            car_sensor_dist = 1.0 - (distance_to_another_car / sensor_range)
            car_sensor_dist = max(0.0, min(1.0, car_sensor_dist))
            if car_obj is not None:
                v_self = self.direction_vector * self.speed
                v_other = car_obj.direction_vector * car_obj.speed
                v_rel_global = v_self - v_other
    
                v_rel_local = v_rel_global.rotate(self.angle)
                max_vel = 1.8 * self.car_config.max_speed
        
                rel_vx = max(-1.0, min(1.0, v_rel_local.x / max_vel))
                rel_vy = max(-1.0, min(1.0, v_rel_local.y / max_vel))
            else:
                rel_vx = 0.0
                rel_vy = 0.0
            
            ml_sensor_input.extend([wall_sensor_data, car_sensor_dist, rel_vx, rel_vy])
        return ml_sensor_input
    
    def _get_ml_sensor_input_5(self, measur):
        ml_sensor_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj,obsticle_col_point in measur:
            
            nearest_dist = min(distance_to_obsticle, distance_to_another_car)
            sensor_data = 1.0 - (nearest_dist / sensor_range)
            sensor_data = max(0.0, min(1.0, sensor_data))
            
            if distance_to_another_car < distance_to_obsticle and car_obj is not None:
                closure_rate = self._get_closure_rate(other_car=car_obj)
            else:
                closure_rate = self._get_closure_rate(wall=True, wall_pos=obsticle_col_point)

            ml_sensor_input.extend([sensor_data, closure_rate])   
        return ml_sensor_input
    
    def _get_ml_nav_input(self):
        norm_cfg = self.car_config.ml_input_norm
        norm_distance = min(1.0, self.dist_to_dest_point / norm_cfg.max_nav_distance)
        norm_distance = norm_distance ** norm_cfg.nav_distance_exponent

        angle_rad = math.radians(self.angle_to_dest_point)
        
        sin_angle = math.sin(angle_rad)
        cos_angle = math.cos(angle_rad)
        return [norm_distance, sin_angle, cos_angle]
    def _get_ml_input(self, measur): 
        if self.ml_input_type == 1:
            sensor_data = self._get_ml_sensor_input_1(measur)
        elif self.ml_input_type == 2:
            sensor_data = self._get_ml_sensor_input_2(measur)
        elif self.ml_input_type == 3:
            sensor_data = self._get_ml_sensor_input_3(measur)
        elif self.ml_input_type ==  4:
            sensor_data = self._get_ml_sensor_input_4(measur)
        elif self.ml_input_type ==  5:
            sensor_data = self._get_ml_sensor_input_5(measur)
        else:
            raise ValueError(f"Invalid ml_input_type value: {self.ml_input_type}. Values 1 to 5 expected.")
        navigation_data = self._get_ml_nav_input()
        norm_speed = max(0.0, min(1.0, self.speed / self.car_config.max_speed))
        
        ml_input = sensor_data + navigation_data + [norm_speed]       
        return ml_input


    def _sensors_managment(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, screen = None):
        measurement = list()
        for i in range(self.car_config.num_of_sensors):
            distance_to_obsticle, distance_to_another_car, sensor_range, car_obj, obsticle_col_point, car_col_point = \
            self.sensors[i].get_sensor_data(self.pos, self.direction_vector, obsticles_group, cars_group, self)
            if screen: 
                self._draw_sensors(distance_to_obsticle, obsticle_col_point, car_col_point, screen, not(car_obj == None))

            measurement.append((distance_to_obsticle, distance_to_another_car, sensor_range, car_obj, obsticle_col_point))
        return measurement                
        

    def update(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, actions, screen):
        if screen is not None:
            self._update_sprite()
        self._update_pos(actions)
        self.take_observations(obsticles_group, cars_group, screen)
        if self.dist_to_dest_point + 20 < self._min_dist_to_dest_point:
            self._start_dist_to_dest_point = self._min_dist_to_dest_point
            self.last_progress_timer = 0
        else :
            self.last_progress_timer += 1


    def car_score(self, max_sim_time=1500, time=0, colision=False, win=False):
        cfg = self.car_config.score
        
        start_dist = max(cfg.min_score, self._start_dist_to_dest_point) 
        progress = max(0.0, (start_dist - self._min_dist_to_dest_point) / start_dist)
        base_score = (progress ** 2) * 50.0
        
        if win:
            win_base = 25.0
            time_efficiency = max(0.0, (max_sim_time - time) / max_sim_time)
            time_bonus = (time_efficiency ** cfg.time_efficiency_exponent) * 25.0
            base_score += (win_base + time_bonus)
        elif colision:        
            base_score *= cfg.collision_multiplier
        else:
            base_score *= cfg.timeout_multiplier
            
        return max(cfg.min_score, base_score)
    def take_observations(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, screen = None):
        sesor_mesur = self._sensors_managment(obsticles_group, cars_group, screen)
        self.current_observation = self._get_ml_input(sesor_mesur)
