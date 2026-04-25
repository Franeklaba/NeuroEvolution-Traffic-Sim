import pygame
class DestinationPoint(pygame.sprite.Sprite):

    def __init__(self, pos, color, rect):
        super().__init__()
        self.color = color
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.Surface(rect, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center = self.pos)    
        self.mask = pygame.mask.from_surface(self.image) 

