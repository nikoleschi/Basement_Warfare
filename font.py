import pygame
from settings import DEFAULT_FONT


def get_font(size):
    return pygame.font.Font(DEFAULT_FONT, size)


def create_text(font, text, aa, color, position):
    new_font = font.render(text, aa, color)
    new_font_rect = new_font.get_rect(center=position)

    return new_font, new_font_rect
