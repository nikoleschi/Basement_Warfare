import unittest
import pygame
from player import Player
from bullet import Bullet
from settings import INF


class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.obstacles = pygame.sprite.Group()
        self.game_screen = pygame.display.set_mode((800, 600))
        self.controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT, pygame.K_SPACE]
        self.bullets = '10'
        self.player = Player((400, 300), self.obstacles, self.game_screen, self.controls, "Player1", self.bullets)

    def tearDown(self):
        pygame.quit()

    def test_bullet_amount(self):
        bullets = INF
        self.player_1 = Player((400, 300), self.obstacles, self.game_screen, self.controls, "Player1", bullets)
        self.assertTrue(self.player_1.infinity_bullets)
        self.assertEqual(self.player_1.bullet_amount, INF)

        self.assertFalse(self.player.infinity_bullets)
        self.assertEqual(self.player.bullet_amount, 10)

    def test_get_damage(self):
        self.player.current_health = 100
        self.player.target_health = 100
        self.player.shield = False

        self.assertFalse(self.player.get_damage(20))
        self.assertEqual(self.player.target_health, 80)

        self.player.shield = True
        self.assertFalse(self.player.get_damage(20))
        self.assertFalse(self.player.shield)
        self.assertEqual(self.player.target_health, 80)

        self.assertTrue(self.player.get_damage(100))
        self.assertEqual(self.player.target_health, 0)

    def test_get_health(self):
        self.player.current_health = 50
        self.player.target_health = 50
        self.player.max_health = 100

        self.player.get_health(20)
        self.assertEqual(self.player.target_health, 70)

        self.player.get_health(50)
        self.assertEqual(self.player.target_health, 120)

    def test_get_bullets(self):
        self.player.bullet_amount = 5
        self.player.max_bullets = 10

        self.player.get_bullets(5)
        self.assertEqual(self.player.bullet_amount, 10)

        self.player.get_bullets(10)
        self.assertEqual(self.player.bullet_amount, 10)

        self.player.infinity_bullets = True
        self.player.get_bullets(5)
        self.assertTrue(self.player.infinity_bullets)
        self.assertEqual(self.player.bullet_amount, self.player.max_bullets)

    def test_shoot(self):
        initial_bullet_amount = self.player.bullet_amount
        initial_time = pygame.time.get_ticks()

        self.player._shoot()
        bullet_created = False
        for sprite in self.player.bullets:
            if isinstance(sprite, Bullet):
                bullet_created = True
                break

        self.assertTrue(bullet_created)
        self.assertFalse(self.player.ready)
        self.assertLessEqual(self.player.gun_time - initial_time, self.player.gun_time)

        if not self.player.infinity_bullets:
            self.assertEqual(self.player.bullet_amount, initial_bullet_amount - 1)

    def test_reload(self):
        self.player.ready = False
        self.player.gun_time = pygame.time.get_ticks() - self.player.gun_cooldown
        self.player._reload()

        self.assertTrue(self.player.ready)


if __name__ == '__main__':
    unittest.main()
