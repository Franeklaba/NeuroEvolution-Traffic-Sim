import pygame
class Obsticle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill('White')
        self.rect = self.image.get_rect(topleft = (x, y))    
        self.mask = pygame.mask.from_surface(self.image) 

