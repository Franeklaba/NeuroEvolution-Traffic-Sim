import math
import itertools
import pygame
from .obsticle import Obsticle

class RaycastSensor:
    BASE_RANGE = 170
    def __init__(self, angle):
        self.angle = angle
    
    def get_sensor_data(self, start_pos, car_direction_vector, obsticles_group, cars_group, speed, my_car):
        abs_angle = abs(self.angle) % 360
        if abs_angle > 180:
            abs_angle = 360 - abs_angle
        
        range_multiplier = 1.0 - (abs_angle / 90.0) * 0.7
        raycas_range = (self.BASE_RANGE + speed * 35) * range_multiplier
        
        raycast_direction_vector = car_direction_vector.rotate(self.angle)
        end_point = start_pos + raycast_direction_vector * raycas_range
        
        shortest_wall_dist_sq = raycas_range * raycas_range
        shortest_car_dist_sq = shortest_wall_dist_sq
        
        wall_point = end_point
        car_point = end_point
        closest_car_object = None

        for obj in itertools.chain(obsticles_group, cars_group):
            if obj == my_car:
                continue

            clipped = obj.rect.clipline(start_pos, end_point)
            if not clipped:
                continue

            dist_sq = start_pos.distance_squared_to(clipped[0])

            if isinstance(obj, Obsticle):
                if dist_sq < shortest_wall_dist_sq:
                    shortest_wall_dist_sq = dist_sq
                    wall_point = clipped[0]
            else: 
                if dist_sq < shortest_car_dist_sq:
                    shortest_car_dist_sq = dist_sq
                    car_point = clipped[0]
                    closest_car_object = obj

        if shortest_wall_dist_sq < shortest_car_dist_sq:
            shortest_car_dist_sq = raycas_range * raycas_range 
            closest_car_object = None
             

        return math.sqrt(shortest_wall_dist_sq), math.sqrt(shortest_car_dist_sq), raycas_range, closest_car_object, wall_point, car_point

            
        
        
