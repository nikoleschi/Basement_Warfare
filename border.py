import pygame
from settings import DEFAULT_BORDER_IMAGE


class Block(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(DEFAULT_BORDER_IMAGE).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1.25)
        self.rect = self.image.get_rect(topleft=position)
        self.mask = pygame.mask.from_surface(self.image)
