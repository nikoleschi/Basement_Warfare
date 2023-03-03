import pygame
import random
from settings import *


class Mouse(pygame.sprite.Sprite):
    def __init__(self, position, sprite_group):
        super().__init__()
        self.image = pygame.image.load(DEFAULT_MOUSE_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.speed = MOUSE_SPEED
        self.sprite_group = sprite_group

        self.current_direction_index = self._random_direction()
        self.current_direction = MOUSE_DIRECTIONS[self.current_direction_index]
        self.images = self._rotated_mouse_images()
        self.image = self.images[self.current_direction_index]
        self.masks = self._rotated_mouse_masks()
        self.mask = self.masks[self.current_direction_index]

    def _rotated_mouse_masks(self):
        return [pygame.mask.from_surface(image) for image in self.images]

    def _rotated_mouse_images(self):
        return [pygame.transform.rotate(self.image, 90 * angle) for angle in range(len(MOUSE_DIRECTIONS))]

    def _move(self):
        self.rect.x += self.current_direction[0] * self.speed
        self.rect.y += self.current_direction[1] * self.speed

    def update(self):
        if random.random() < CHANGE_DIRECTION_PROB:
            self._change_direction()

        self._move()
        self._obstacle_collision()

    def _obstacle_collision(self):
        for sprite in self.sprite_group:
            if pygame.sprite.collide_rect(self, sprite):
                if self.current_direction_index == 0:
                    self.rect.bottom = sprite.rect.top
                elif self.current_direction_index == 1:
                    self.rect.right = sprite.rect.left
                elif self.current_direction_index == 2:
                    self.rect.top = sprite.rect.bottom
                else:
                    self.rect.left = sprite.rect.right
                self._change_direction()

    def _change_direction(self):
        changed_direction = self._random_direction()
        while changed_direction == self.current_direction_index:
            changed_direction = self._random_direction()

        self.current_direction = MOUSE_DIRECTIONS[changed_direction]
        self.current_direction_index = changed_direction
        self.image = self.images[self.current_direction_index]
        self.mask = self.masks[self.current_direction_index]

    def _random_direction(self):
        return random.randint(0, 3)
