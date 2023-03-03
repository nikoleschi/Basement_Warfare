from abc import ABC, abstractmethod

from font import create_text, get_font
from button import Button, create_buttons
from settings import *
from map_validator import MapValidator
from others import prompt_file, get_file_name, get_dirname


class BaseMenu(ABC):
    def __init__(self, screen):
        self.screen = screen
        self.center_x, self.center_y = screen.get_rect().center

        self.texts = self._create_texts()
        self.buttons = self._create_buttons()
        self.menu_clicked = False

    @abstractmethod
    def _create_texts(self):
        pass

    @abstractmethod
    def _create_buttons(self):
        pass

    def _display_texts(self):
        for text in self.texts:
            self.screen.blit(*text)

    def _check_hover(self, mouse_pos):
        for button in self.buttons:
            button.change_color(mouse_pos)
            button.update(self.screen)

    def click_button(self, mouse_pos):
        for button in self.buttons:
            if button.check_input(mouse_pos):
                return button.text_input

    def update(self, mouse_pos):
        self._display_texts()
        self._check_hover(mouse_pos)


class Menu(BaseMenu):
    def __int__(self, screen):
        super().__init__(screen)

    # Override
    def _create_texts(self):
        menu_text = create_text(get_font(90), GAME_NAME, True, ORANGE, (self.center_x, self.center_y - 280))
        return [menu_text]

    # Override
    def _create_buttons(self):
        button_font = get_font(75)

        play_button = create_buttons(center_start_x=self.center_x, center_start_y=self.center_y - 100,
                                     offset=0,
                                     button_texts=[PLAY_BUTTON_TEXT],
                                     image=pygame.transform.scale(BUTTON_IMAGE, (370, 110)),
                                     font=button_font,
                                     base_color='white', hovering_color=HOVER_COLOR)
        options_button = create_buttons(center_start_x=self.center_x, center_start_y=self.center_y + 50,
                                        offset=0,
                                        button_texts=[OPTIONS_BUTTON_TEXT],
                                        image=pygame.transform.scale(BUTTON_IMAGE, (580, 110)),
                                        font=button_font,
                                        base_color='white', hovering_color=HOVER_COLOR)
        quit_button = create_buttons(center_start_x=self.center_x, center_start_y=self.center_y + 200,
                                     offset=0,
                                     button_texts=[QUIT_BUTTON_TEXT],
                                     image=pygame.transform.scale(BUTTON_IMAGE, (370, 110)),
                                     font=button_font,
                                     base_color='white', hovering_color=HOVER_COLOR)

        return [*play_button, *options_button, *quit_button]


class Options(BaseMenu):
    def __init__(self, screen, overtime, timer, bullets, map_path):
        self.image = pygame.transform.scale(BUTTON_IMAGE, (150, 60))
        self.overtime = overtime
        self.timer = timer
        self.bullets = bullets
        self.map_path = map_path

        super().__init__(screen)

        self._clicked_button(self.overtime_buttons, overtime)
        self._clicked_button(self.timer_buttons, timer)
        self._clicked_button(self.bullet_buttons, bullets)

    def _create_texts(self):
        self.text_font = get_font(70)

        overtime_text = create_text(font=self.text_font, text='OVERTIME', aa=True, color=ORANGE,
                                    position=(self.center_x, self.center_y - 350))

        timer_text = create_text(font=self.text_font, text='TIMER (in seconds)', aa=True, color=ORANGE,
                                 position=(self.center_x, self.center_y - 170))

        bullets_text = create_text(font=self.text_font, text='BULLETS', aa=True, color=ORANGE,
                                   position=(self.center_x, self.center_y + 10))

        map_text = create_text(font=self.text_font, text='CURRENT MAP', aa=True, color=ORANGE,
                               position=(self.center_x, self.center_y + 190))

        return_text = create_text(font=get_font(20), text='Press any key to return to Main Menu', aa=True,
                                  color=ORANGE,
                                  position=(self.center_x, self.center_y + 400))

        return [overtime_text, timer_text, bullets_text, map_text, return_text]

    def _create_buttons(self):
        self.button_font = get_font(40)

        self.overtime_buttons = create_buttons(center_start_x=self.center_x - 100, center_start_y=self.center_y - 280,
                                               offset=200,
                                               button_texts=OVERTIME_BUTTONS_TEXT, image=self.image,
                                               font=self.button_font,
                                               base_color='white', hovering_color=HOVER_COLOR)

        self.timer_buttons = create_buttons(center_start_x=self.center_x - 500, center_start_y=self.center_y - 100,
                                            offset=200,
                                            button_texts=TIMER_BUTTONS_TEXT, image=self.image,
                                            font=self.button_font, base_color='white', hovering_color=HOVER_COLOR)

        self.bullet_buttons = create_buttons(center_start_x=self.center_x - 300, center_start_y=self.center_y + 80,
                                             offset=200,
                                             button_texts=BULLET_BUTTONS_TEXT, image=self.image,
                                             font=self.button_font, base_color='white', hovering_color=HOVER_COLOR)

        self.map_button = Button(image=pygame.transform.scale(BUTTON_IMAGE, (800, 60)),
                                 pos=(self.center_x, self.center_y + 260), text_input=get_file_name(self.map_path),
                                 font=self.button_font, base_color='white', hovering_color=HOVER_COLOR)

        return [*self.overtime_buttons, *self.timer_buttons, *self.bullet_buttons, self.map_button]

    def get_clicked(self):
        return self.overtime, self.timer, self.bullets, self.map_path

    def _clicked_button(self, buttons, button_text):
        for button in buttons:
            if button.text_input == button_text:
                button.clicked = True
                break

    def _click_button_group(self, button_group, mouse_pos):
        for button in button_group:
            if button.check_input(mouse_pos):
                button.clicked = True
                for btn in button_group:
                    if btn != button:
                        btn.clicked = False
                return button.text_input

    def _click_map_button(self, mouse_pos):
        if self.map_button.check_input(mouse_pos):
            self.menu_clicked = True
            map_validator = MapValidator(prompt_file(get_dirname(self.map_path)))
            if not map_validator.valid:
                self.message = map_validator.error_message
                self.color_message = INVALID_COLOR
            else:
                self.message = SUCCESSFUL_LOAD_MSG
                self.color_message = VALID_COLOR
                self.map_path = map_validator.path
                self.map_button.change_text(get_file_name(map_validator.path))

    def _display_change_map_status(self, message, color):
        map_status_text = create_text(get_font(20), message, True, color, (self.center_x, self.center_y + 300))
        self.screen.blit(*map_status_text)

    def update(self, mouse_pos):
        self._display_texts()
        self._check_hover(mouse_pos)
        if self.menu_clicked:
            self._display_change_map_status(self.message, self.color_message)

    def click_button(self, mouse_pos):
        self._click_map_button(mouse_pos)

        overtime = self._click_button_group(self.overtime_buttons, mouse_pos)
        if overtime:
            self.overtime = overtime

        timer = self._click_button_group(self.timer_buttons, mouse_pos)
        if timer:
            self.timer = timer

        bullets = self._click_button_group(self.bullet_buttons, mouse_pos)
        if bullets:
            self.bullets = bullets
