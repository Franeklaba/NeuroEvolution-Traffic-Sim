import pygame
class DestinationPoint(pygame.sprite.Sprite):

    def __init__(self, pos, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((40,40), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)    
        self.mask = pygame.mask.from_surface(self.image) 

