import random

from settings import *
from player import Player
from border import Block
from crate import Crate
from powerup import Powerup
from scoreboard import Scoreboard
from font import get_font
from mouse import Mouse


class Game:
    def __init__(self, overtime, timer, bullets, map_path):
        self.screen = pygame.display.get_surface()

        self.over_time_mode = True if overtime == OVERTIME_YES else False
        self.over_time = False
        self.timer = 0 if timer == INF else (int(timer) + 1) * 1_000
        self.player_bullets = bullets
        self.map_path = map_path

        self.obstacles = pygame.sprite.Group()
        self.crates = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mouses = pygame.sprite.Group()

        self.game_screen = pygame.Surface((1400, 700))
        self.game_screen.fill(GAME_SCREEN_BACKGROUND_COLOR)
        self.game_screen_rect = self.game_screen.get_rect(
            center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 10))

        self._generate_map()

        self.health_bar_player_1 = Scoreboard(self.player_1, HEALTH_BAR_1_POSITION)
        self.health_bar_player_2 = Scoreboard(self.player_2, HEALTH_BAR_2_POSITION)

        self.start_game_time = pygame.time.get_ticks()
        self.winner = None
        self.game_over = False
        self.over_time = False

    def _generate_map(self):
        x_start, y_start = self.game_screen_rect.topleft
        created_player_1 = -1, -1
        created_player_2 = -1, -1
        mouses_coords = []

        with open(self.map_path) as file:
            map_layout = file.readlines()

        for row_index, row in enumerate(map_layout):
            for col_index, col in enumerate(row):
                x = x_start + col_index * 50
                y = y_start + row_index * 50
                if col == WALL:
                    block = Block((x, y))
                    self.obstacles.add(block)
                if col == CRATE:
                    crate = Crate((x, y))
                    self.crates.add(crate)
                    self.obstacles.add(crate)
                if col == MOUSE:
                    mouses_coords.append((x, y))
                if col == PLAYER_1 and created_player_1 == (-1, -1):
                    created_player_1 = x + 50, y + 50
                if col == PLAYER_2 and created_player_2 == (-1, -1):
                    created_player_2 = x + 50, y + 50

        self.player_1 = Player(created_player_1, self.obstacles, self.game_screen_rect, PLAYER_1_CONTROLS,
                               PLAYER_1_NAME, self.player_bullets)
        self.player_1_sprite = pygame.sprite.GroupSingle(self.player_1)

        self.player_2 = Player(created_player_2, self.obstacles, self.game_screen_rect, PLAYER_2_CONTROLS,
                               PLAYER_2_NAME, self.player_bullets)
        self.player_2_sprite = pygame.sprite.GroupSingle(self.player_2)
        self._create_mouses(mouses_coords)

    def _create_mouses(self, coords):
        for pos in coords:
            mouse = Mouse(pos, self.obstacles)
            self.mouses.add(mouse)

    def _set_overtime(self):
        self.over_time = True
        self.player_1.infinity_bullets = True
        self.player_2.infinity_bullets = True
        self.mouses.empty()

    def _timer(self):
        game_time = pygame.time.get_ticks() - self.start_game_time
        if not self.over_time and game_time >= self.timer:
            winner = self._check_winner()
            if winner:
                self.game_over = True
                self.winner = winner
            elif self.over_time_mode:
                self._set_overtime()
            else:
                self.game_over = True

        remaining_time = int((self.timer - game_time) / 1000)

        if self.over_time:
            text = OVERTIME_TEXT
        else:
            text = TIMER_TEXT.format(remaining_time)

        font = get_font(50)
        timer_surf = font.render(text, True, 'white')
        timer_rect = timer_surf.get_rect(midbottom=self.game_screen_rect.midtop)

        self.screen.blit(timer_surf, timer_rect)

    def _check_draw(self):
        return self.player_1.bullet_amount == self.player_2.bullet_amount == 0

    def _check_winner(self):
        if self.player_1.target_health > self.player_2.target_health:
            return self.player_1
        elif self.player_1.target_health < self.player_2.target_health:
            return self.player_2

    def _bullet_collision(self, shooting_player, target_player):
        if shooting_player.sprite.bullets:
            for bullet in shooting_player.sprite.bullets:
                obstacles = pygame.sprite.spritecollide(bullet, self.obstacles, False, pygame.sprite.collide_mask)
                if obstacles:
                    bullet.kill()
                    for obstacle in obstacles:
                        if isinstance(obstacle, Crate):
                            position = obstacle.rect.center
                            if obstacle.attacked(shooting_player.sprite.gun_damage):
                                self._create_powerup(position)

                if pygame.sprite.collide_mask(bullet, target_player.sprite):
                    bullet.kill()
                    if not target_player.sprite.hit and target_player.sprite.get_damage(
                            shooting_player.sprite.gun_damage) or self.over_time:
                        self.game_over = True
                        self.winner = shooting_player.sprite

    def _player_mouse_collision(self):
        if self.mouses:
            for mouse in self.mouses:
                if pygame.sprite.collide_mask(mouse, self.player_1_sprite.sprite):
                    if not self.player_1.hit and self.player_1.get_damage(MOUSE_DAMAGE):
                        self.game_over = True
                        self.winner = self.player_2_sprite.sprite

                if pygame.sprite.collide_mask(mouse, self.player_2_sprite.sprite):
                    if not self.player_2.hit and self.player_2.get_damage(MOUSE_DAMAGE):
                        self.game_over = True
                        self.winner = self.player_1_sprite.sprite

    def _game_over_screen(self):
        font_winner = get_font(70)
        text = WINNER_MSG.format(self.winner.name) if self.winner is not None else DRAW_MSG

        winner_label_surf = font_winner.render(text, True, 'white')
        winner_label_rect = winner_label_surf.get_rect(center=self.game_screen_rect.center)

        font = get_font(15)
        restart_label_surf = font.render(RETURN_MSG, True, 'white')
        restart_label_rect = restart_label_surf.get_rect(midtop=winner_label_rect.midbottom)

        self.screen.blit(winner_label_surf, winner_label_rect)
        self.screen.blit(restart_label_surf, restart_label_rect)

    def _players_bullet_collision(self):
        self._bullet_collision(self.player_1_sprite, self.player_2_sprite)
        self._bullet_collision(self.player_2_sprite, self.player_1_sprite)

    def _create_powerup(self, position):
        powerups = list(POWERUPS_DROP_RATE.keys())
        powerup = random.choices(powerups, weights=POWERUPS_DROP_RATE.values())
        if powerup[0] != POWERUP_NOTHING:
            self.powerups.add(Powerup(position, powerup[0]))

    def _check_powerup_cooldown(self, player):
        current_time = pygame.time.get_ticks()
        if player.speed_powerup:
            if current_time - player.speed_powerup_time >= POWERUPS_COOLDOWN:
                player.speed_powerup = False
                player.movement_speed = PLAYER_SPEED
        if player.damage_powerup:
            if current_time - player.damage_powerup_time >= POWERUPS_COOLDOWN:
                player.damage_powerup = False
                player.gun_damage = PLAYER_GUN_DAMAGE

    def _check_powerups(self, player):
        if player.speed_powerup:
            player.movement_speed = PLAYER_SPEED + MOVEMENT_SPEED_BONUS
        if player.damage_powerup:
            player.gun_damage = PLAYER_GUN_DAMAGE * DAMAGE_MULTIPLIER

        self._check_powerup_cooldown(player)

    def _players_check_powerups(self):
        self._check_powerups(self.player_1)
        self._check_powerups(self.player_2)

    def _check_powerup_collision(self, player):
        if self.powerups:
            powerups = pygame.sprite.spritecollide(player, self.powerups, True, pygame.sprite.collide_mask)
            for powerup in powerups:
                powerup_name = powerup.name
                if powerup_name == POWERUP_HEALTH:
                    player.get_health(HEALTH_RESTORED)
                elif powerup_name == POWERUP_SHIELD:
                    player.shield = True
                elif powerup_name == POWERUP_BULLETS:
                    player.get_bullets(ADDED_BULLETS_AMOUNT)
                elif powerup_name == POWERUP_SPEED:
                    player.speed_powerup_time = pygame.time.get_ticks()
                    player.speed_powerup = True
                elif powerup_name == POWERUP_DAMAGE:
                    player.damage_powerup_time = pygame.time.get_ticks()
                    player.damage_powerup = True

    def _players_powerup_collision(self):
        self._check_powerup_collision(self.player_1)
        self._check_powerup_collision(self.player_2)

    def run(self):
        if not self.game_over:
            self.screen.blit(self.game_screen, self.game_screen_rect)
            self._players_bullet_collision()
            self._players_powerup_collision()
            self._player_mouse_collision()
            self._players_check_powerups()
            self.player_1.update()
            self.player_2.update()
            self.mouses.update()
            if self._check_draw():
                if self.over_time_mode and self.timer:
                    self._set_overtime()
                else:
                    self.game_over = True
            if not self.over_time:
                self.health_bar_player_1.update()
                self.health_bar_player_2.update()
            if self.timer:
                self._timer()

            self.obstacles.draw(self.screen)
            self.powerups.draw(self.screen)
            self.player_1_sprite.sprite.bullets.draw(self.screen)
            self.player_2_sprite.sprite.bullets.draw(self.screen)
            self.player_1_sprite.draw(self.screen)
            self.player_2_sprite.draw(self.screen)
            self.mouses.draw(self.screen)
        else:
            self._game_over_screen()
