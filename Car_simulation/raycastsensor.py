import math
import pygame


class RaycastSensor:
    BASE_RANGE = 170
    def __init__(self, angle):
        self.angle = angle

    def get_distance_and_colision_point_for_obsticles(self, start_pos: pygame.math.Vector2,
        car_direction_vector: pygame.math.Vector2,obsticles_group: pygame.sprite.Group, speed):
        
        raycas_range = self.BASE_RANGE + speed * 35
        
        raycast_direction_vector = car_direction_vector.rotate(self.angle)
        end_point = start_pos + raycast_direction_vector * raycas_range
        shortest_dist_sq = raycas_range * raycas_range
        point = end_point
        for obsticle in obsticles_group:
            clipped = obsticle.rect.clipline(start_pos, end_point)
            if not clipped:
                continue

            dist_sq = start_pos.distance_squared_to(clipped[0])
            if dist_sq < shortest_dist_sq:
                shortest_dist_sq = dist_sq
                point = clipped[0]
        
        distance = math.sqrt(shortest_dist_sq)

        standardized_data = 1 - ((distance - (6 + raycas_range * 0.11)) / raycas_range)
        if standardized_data > 1:
            standardized_data = 1
        standardized_data = standardized_data ** 1.7

        if distance >= raycas_range - 0.1:
            standardized_data = 0
        return standardized_data , point
    
    def get_distance_from_another_car(self, start_pos: pygame.math.Vector2,
        car_direction_vector: pygame.math.Vector2,obsticles_group: pygame.sprite.Group, speed):
        pass
        
