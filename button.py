import pygame


def create_buttons(center_start_x, center_start_y, offset, button_texts, image, font, base_color, hovering_color):
    return [Button(image=image,
                   pos=(center_start_x + button_num * offset, center_start_y),
                   text_input=button_texts[button_num],
                   font=font,
                   base_color=base_color, hovering_color=hovering_color) for button_num in
            range(len(button_texts))]


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.center_pos = pos
        self.rect = self.image.get_rect(center=pos)

        self.border = pygame.Rect(self.rect.topleft, self.rect.size)
        self.clicked = False

        self.text_input = text_input
        self.font = font
        self.text = self.font.render(self.text_input, True, base_color)
        self.text_rect = self.text.get_rect(center=pos)

        self.base_color, self.hovering_color = base_color, hovering_color

    def change_text(self, new_text):
        self.text_input = new_text
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.center_pos)

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        if self.clicked:
            pygame.draw.rect(screen, 'white', self.border, 4)

    def _check_range(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom)

    def check_input(self, position):
        return self._check_range(position)

    def change_color(self, position):
        if self._check_range(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
