import unittest
from unittest.mock import Mock, patch
import pygame
from mouse import Mouse
from settings import MOUSE_SPEED


class TestMouse(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((640, 480))
        self.mock_group = Mock()
        self.position = (0, 0)

    def test_init(self):
        mouse = Mouse(self.position, self.mock_group)
        self.assertEqual(mouse.rect.topleft, self.position)
        self.assertEqual(mouse.speed, MOUSE_SPEED)
        self.assertIsNotNone(mouse.image)
        self.assertIsNotNone(mouse.mask)

    def test_change_direction(self):
        mouse = Mouse(self.position, self.mock_group)
        original_direction = mouse.current_direction_index
        mouse._change_direction()
        self.assertNotEqual(mouse.current_direction_index, original_direction)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
