from settings import *
from font import get_font, create_text


class Scoreboard:
    def __init__(self, player, position):
        super().__init__()

        self.bar_image = pygame.image.load(DEFAULT_BAR_IMAGE).convert_alpha()
        self.bar = self.bar_image.get_rect(topleft=position)

        self.player_name_position = self.bar.topleft[0] + 20, self.bar.topleft[1] + 3
        self.bullet_position = self.bar.topleft[0] + 160, self.bar.topleft[1] + 13
        self.health_position = self.bar.topleft[0] + 310, self.bar.topleft[1] + 10

        self.player = player

        self.screen = pygame.display.get_surface()
        self.image_heart = pygame.image.load(DEFAULT_HEART_IMAGE).convert_alpha()
        self.image_heart = pygame.transform.rotozoom(self.image_heart, 0, 1.4)
        self.rect_heart = self.image_heart.get_rect()

        self.image_bullet = pygame.image.load(DEFAULT_BULLET_IMAGE).convert_alpha()
        self.image_bullet = pygame.transform.rotozoom(self.image_bullet, 90, 0.35)
        self.rect_bullet = self.image_bullet.get_rect(topleft=self.bullet_position)

        self.image_shield = pygame.image.load(DEFAULT_SHIELD_IMAGE).convert_alpha()
        self.image_shield = pygame.transform.rotozoom(self.image_shield, 0, 1.5)
        self.rect_shield = self.image_shield.get_rect()

        self.health_bar_color = HEALTH_BAR_COLOR

        self.health_bar_length = HEALTH_BAR_LENGTH
        self.health_ratio = self.player.max_health / self.health_bar_length
        self.health_change_speed = HEALTH_BAR_CHANGE_SPEED

        self.health_bar_border_rect = pygame.Rect(*self.health_position, self.health_bar_length, 40)

        self.player_label_surf = get_font(60).render(f'{self.player.name}', True, 'white')
        self.player_label_rect = self.player_label_surf.get_rect(topleft=self.player_name_position)

    def update(self):
        health_bar = self._health_calc()
        self.screen.blit(self.bar_image, self.bar)
        self.screen.blit(self.player_label_surf, self.player_label_rect)

        self._display_health_bar(health_bar)
        self._display_bullets()

    def _health_calc(self):
        if self.player.current_health < self.player.target_health:
            self.player.current_health += self.health_change_speed

        if self.player.current_health > self.player.target_health:
            self.player.current_health -= self.health_change_speed

        health_bar_width = min(int(self.player.max_health / self.health_ratio),
                               int(self.player.current_health / self.health_ratio))
        return pygame.Rect(*self.health_position, health_bar_width, 40)

    def _display_bullets(self):
        font = get_font(40)
        self.screen.blit(self.image_bullet, self.rect_bullet)

        self.bullet_count_surf = font.render(f'{self.player.bullet_amount}', True, 'white')
        self.bullet_count_rect = self.bullet_count_surf.get_rect(
            midleft=(self.rect_bullet.midright[0] + 5, self.rect_bullet.midright[1]))
        self.screen.blit(self.bullet_count_surf, self.bullet_count_rect)

    def _display_health_bar(self, health_bar_rect):
        font = get_font(40)

        # Health bar
        pygame.draw.rect(self.screen, self.health_bar_color, health_bar_rect)
        pygame.draw.rect(self.screen, 'white', self.health_bar_border_rect, BORDER_RECT_SIZE)

        # Shield / Heart
        if self.player.shield:
            self.health_bar_color = HEALTH_BAR_COLOR_SHIELDED
            self.rect_shield.midright = (health_bar_rect.midleft[0] - 5, health_bar_rect.midleft[1])
            self.screen.blit(self.image_shield, self.rect_shield)
        else:
            self.health_bar_color = HEALTH_BAR_COLOR
            self.rect_heart.midright = (health_bar_rect.midleft[0], health_bar_rect.midleft[1])
            self.screen.blit(self.image_heart, self.rect_heart)

            health_score = create_text(font, f'{self.player.target_health}', True, 'white',
                                       self.health_bar_border_rect.center)

            self.screen.blit(*health_score)
