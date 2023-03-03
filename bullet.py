import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, moving_direction, player_position):
        super().__init__()
        self.moving_direction = moving_direction

        if self.moving_direction.magnitude() != 0:
            self.moving_direction = self.moving_direction.normalize()

        self.image = pygame.image.load(DEFAULT_BULLET_IMAGE).convert_alpha()

        self.image = pygame.transform.rotozoom(self.image, DIRECTION_TO_INDEX[tuple(moving_direction)] * 45, 0.2)
        self.rect = self.image.get_rect(center=player_position)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = BULLET_SPEED

    def _move(self):
        self.rect.center += self.moving_direction * self.speed

    def update(self):
        self._move()
