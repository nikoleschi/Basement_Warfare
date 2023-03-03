import sys
from settings import *
from game import Game
from menu import Menu, Options
from others import get_current_directory


def play(overtime, timer, bullets, map_path):
    game = Game(overtime, timer, bullets, map_path)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE and game.game_over) or (
                        event.key == pygame.K_ESCAPE and not game.game_over):
                    return

        screen.blit(background, (0, 0))
        game.run()

        pygame.display.flip()
        clock.tick(FPS)


def options():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        option.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                option.menu_clicked = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                option.click_button(mouse_pos)

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        menu.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_button = menu.click_button(mouse_pos)
                if pressed_button == PLAY_BUTTON_TEXT:
                    play(*option.get_clicked())
                if pressed_button == OPTIONS_BUTTON_TEXT:
                    options()
                if pressed_button == QUIT_BUTTON_TEXT:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    clock = pygame.time.Clock()

    background = pygame.image.load(BACKGROUND)
    default_map_path = DEFAULT_MAP

    option = Options(screen, DEFAULT_OVERTIME, DEFAULT_TIMER, DEFAULT_BULLETS, default_map_path)
    menu = Menu(screen)
    main_menu()
