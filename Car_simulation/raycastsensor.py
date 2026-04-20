import math

import pygame


class RaycastSensor:
    RANGE = 2000
    def __init__(self, angle):
        self.angle = angle

    def Get_colision_point(self, start_pos: tuple[float, float], base_angle: float, obsticles_group: pygame.sprite.Group) :
        angle = self.angle + base_angle
        start_x, start_y = start_pos
        angle_in_rad = math.radians(angle)
        end_x = start_x + self.RANGE * math.cos(angle_in_rad)
        end_y = start_y - self.RANGE * math.sin(angle_in_rad)

        shortest_dist = None
        closest_point = None

        for obsticle in obsticles_group:
            clipped = obsticle.rect.clipline(start_x, start_y, end_x, end_y)
            if not clipped:
                continue
            for point_x, point_y in clipped:
                dist_x = point_x - start_x
                dist_y = point_y - start_y
                dist_sq = dist_x * dist_x + dist_y * dist_y
                if shortest_dist is None or dist_sq < shortest_dist:
                    shortest_dist = dist_sq
                    closest_point = (float(point_x), float(point_y))

        return closest_point
