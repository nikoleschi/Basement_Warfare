import unittest
import pygame
from settings import DEFAULT_CRATE_IMAGE, CRATE_HEALTH
from crate import Crate


class TestCrate(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((640, 480))

    def test_crate_attacked(self):
        position = (0, 0)
        crate = Crate(position)
        self.assertEqual(crate.health_points, CRATE_HEALTH)
        crate.attacked(10)
        self.assertEqual(crate.health_points, CRATE_HEALTH - 10)

    def test_crate_destroyed(self):
        position = (0, 0)
        crate = Crate(position)
        crate.attacked(CRATE_HEALTH)
        self.assertTrue(crate._check_destroyed())

    def test_crate_not_destroyed(self):
        position = (0, 0)
        crate = Crate(position)
        crate.attacked(CRATE_HEALTH - 10)
        self.assertFalse(crate._check_destroyed())

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
