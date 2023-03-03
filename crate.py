import pygame
from settings import DEFAULT_CRATE_IMAGE, CRATE_HEALTH


class Crate(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(DEFAULT_CRATE_IMAGE).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect(topleft=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.health_points = CRATE_HEALTH

    def _check_destroyed(self):
        if self.health_points <= 0:
            self.kill()
            return True

        return False

    def attacked(self, damage_taken):
        self.health_points -= damage_taken
        return self._check_destroyed()
