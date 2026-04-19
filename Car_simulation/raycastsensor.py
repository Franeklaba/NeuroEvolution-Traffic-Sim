import math
import pygame 
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
