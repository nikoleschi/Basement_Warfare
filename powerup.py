import pygame
from settings import DEFAULT_POWERUP_DIRECTORY, PNG


class Powerup(pygame.sprite.Sprite):
    def __init__(self, position, name):
        super().__init__()
        file_path = DEFAULT_POWERUP_DIRECTORY + name + PNG
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name
