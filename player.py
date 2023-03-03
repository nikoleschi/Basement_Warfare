import math

import pygame.math

from settings import *
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, position, obstacles, game_screen, controls, name, bullets):
        super().__init__()
        self.game_screen = game_screen
        self.start_position = position
        self.controls = controls
        self.name = name

        self.image = pygame.image.load(DEFAULT_PLAYER_IMAGE).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.18)
        self.rect = self.image.get_rect(center=self.start_position)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(1, 0)
        self.last_movement = pygame.math.Vector2(1, 0)
        self.images = self._rotated_player_images()
        self.masks = self._rotated_player_masks()

        self.movement_speed = PLAYER_SPEED
        self.previous_positions = [(self.rect.center, 0)]
        self.current_health = PLAYER_HEALTH
        self.target_health = PLAYER_HEALTH
        self.max_health = PLAYER_MAX_HEALTH

        self.shield = False
        self.speed_powerup_time = 0
        self.speed_powerup = False
        self.damage_powerup_time = 0
        self.damage_powerup = False

        self.lock_rotation = False
        self.lock_key_pressed = False

        self.ready = True
        self.gun_damage = PLAYER_GUN_DAMAGE
        self.gun_time = 0
        self.gun_cooldown = GUN_COOLDOWN
        self.gun_key_pressed = False
        if bullets == INF:
            self.infinity_bullets = True
            self.bullet_amount = bullets
        else:
            self.infinity_bullets = False
            self.bullet_amount = int(bullets)

        self.max_bullets = MAX_BULLETS

        self.bullets = pygame.sprite.Group()

        self.obstacle_sprites = obstacles
        self.current_index = 0

        self.hit = False
        self.hit_cooldown = 0

    def get_damage(self, amount):
        self.hit = True
        self.hit_cooldown = pygame.time.get_ticks()

        if self.shield:
            self.shield = False
        else:
            if self.target_health > 0:
                self.target_health -= amount
            if self.target_health <= 0:
                self.target_health = 0
                return True
            return False

    def get_health(self, amount):
        self.target_health += amount

    def get_bullets(self, amount):
        if not self.infinity_bullets:
            self.bullet_amount = min(self.max_bullets, self.bullet_amount + amount)

    def _rotated_player_images(self):
        return [pygame.transform.rotate(self.image, 45 * angle) for angle in range(len(DIRECTION_TO_INDEX))]

    def _rotated_player_masks(self):
        return [pygame.mask.from_surface(image) for image in self.images]

    def _rotate_player(self, direction, current_direction):
        if self.lock_rotation:
            return
        self.image = self.images[direction]
        self.mask = self.masks[direction]
        self.current_index = direction
        self._rotation_collision()
        if self.direction != (0, 0):
            self.last_movement = current_direction.copy()

    def _get_input(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls[UP]]:
            self.direction.y = -1
        elif keys[self.controls[DOWN]]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[self.controls[LEFT]]:
            self.direction.x = -1
        elif keys[self.controls[RIGHT]]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[self.controls[LOCK]]:
            if not self.lock_key_pressed:
                self.lock_rotation = not self.lock_rotation
                self.lock_key_pressed = True
        else:
            self.lock_key_pressed = False

        if keys[self.controls[SHOOT]]:
            if not self.gun_key_pressed and self.ready:
                self._shoot()
                self.gun_key_pressed = True
        else:
            self.gun_key_pressed = False

    def _move(self):
        current_position = self.rect.center
        current_index = self.current_index
        last_direction = self.last_movement.copy()
        current_direction = self.direction
        if self.direction != (0, 0):
            index_to_move = DIRECTION_TO_INDEX[tuple(self.direction)]

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() * math.sqrt(2)
        self.rect.center += self.direction * self.movement_speed

        if self.direction != (0, 0):
            self._rotate_player(index_to_move, current_direction)

        if self._movement_collision():
            self.rect.center = current_position
            self._rotate_player(index_to_move, current_direction)
            if self._movement_collision():
                self.rect.center = current_position
                self._rotate_player(current_index, last_direction)

    def _reload(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.gun_time >= self.gun_cooldown:
                self.ready = True

    def _shoot(self):
        if self.infinity_bullets or self.bullet_amount > 0:
            if self.last_movement != (0, 0):
                if not self.infinity_bullets:
                    self.bullet_amount -= 1
                self.ready = False
                self.gun_time = pygame.time.get_ticks()
                tuple_direction = tuple(self.last_movement)
                self.bullets.add(Bullet(self.last_movement, (self.rect.centerx + BULLET_OFFSET[tuple_direction][0],
                                                             self.rect.centery + BULLET_OFFSET[tuple_direction][1])))

    def _rotation_collision(self):
        for sprite in self.obstacle_sprites:
            if pygame.sprite.collide_mask(sprite, self):
                if self.direction.y < 0:
                    if abs(self.rect.bottom - sprite.rect.top) < abs(self.rect.top - sprite.rect.top):
                        self.rect.bottom = sprite.rect.top - 10
                if self.direction.y > 0:
                    if abs(self.rect.top - sprite.rect.bottom) < abs(self.rect.bottom - sprite.rect.bottom):
                        self.rect.top = sprite.rect.bottom + 10
                if self.direction.x > 0:
                    if abs(self.rect.left - sprite.rect.right) < abs(self.rect.right - sprite.rect.right):
                        self.rect.left = sprite.rect.right + 10
                if self.direction.x < 0:
                    if abs(self.rect.right - sprite.rect.left) < abs(self.rect.left - sprite.rect.left):
                        self.rect.right = sprite.rect.left - 10

    def _movement_collision(self):
        for sprite in self.obstacle_sprites:
            if pygame.sprite.collide_mask(sprite, self):
                return True
        return False

    def _movement_constraint(self):
        if self.rect.left <= self.game_screen.left or self.rect.right >= self.game_screen.right \
                or self.rect.top <= self.game_screen.top or self.rect.bottom >= self.game_screen.bottom:
            self._reset_position()

    def _reset_position(self):
        self.rect.center = self.start_position

    def _hit_reset(self):
        if self.hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_cooldown >= HIT_COOLDOWN:
                self.hit = False

    def update(self):
        self._get_input()
        self._move()
        self._movement_constraint()
        self._reload()
        self._hit_reset()
        self.bullets.update()
