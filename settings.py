import pygame
import os

# others
TXT_TYPE = 'text/plain'
PNG = '.png'
INF = 'INF'
BORDER_RECT_SIZE = 4
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
SHOOT = 'shoot'
LOCK = 'lock'
DIRECTION_TO_INDEX = {
    (1, 0): 0,
    (1, -1): 1,
    (0, -1): 2,
    (-1, -1): 3,
    (-1, 0): 4,
    (-1, 1): 5,
    (0, 1): 6,
    (1, 1): 7
}
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# main.py
GAME_NAME = 'Basement Warfare'
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 820
DEFAULT_MAP = os.path.join(ROOT_DIR, 'maps', 'basement_warfare_classic.txt')
BACKGROUND = os.path.join(ROOT_DIR, 'graphics', 'background.jpg')
DEFAULT_OVERTIME = 'YES'
DEFAULT_TIMER = '180'
DEFAULT_BULLETS = '30'
FPS = 60
PLAY_BUTTON_TEXT = 'PLAY'
OPTIONS_BUTTON_TEXT = 'OPTIONS'
QUIT_BUTTON_TEXT = 'QUIT'

# game
OVERTIME_YES = 'YES'
OVERTIME_TEXT = 'OVERTIME - GOLDEN SHOOT'
TIMER_TEXT = 'TIMER: {0}'
WINNER_MSG = 'THE WINNER IS {0}'
DRAW_MSG = 'THE GAME ENDED IN A DRAW'
RETURN_MSG = 'Press Space to return to Main Menu'

# powerups
DEFAULT_POWERUP_DIRECTORY = os.path.join(ROOT_DIR, 'graphics', 'powerups\\')

POWERUP_BULLETS = 'bullets'
POWERUP_SHIELD = 'shield'
POWERUP_HEALTH = 'health'
POWERUP_SPEED = 'speed'
POWERUP_DAMAGE = 'damage'
POWERUP_NOTHING = 'nothing'
POWERUPS_DROP_RATE = {
    POWERUP_NOTHING: 10,
    POWERUP_SHIELD: 15,
    POWERUP_DAMAGE: 5,
    POWERUP_HEALTH: 15,
    POWERUP_SPEED: 15,
    POWERUP_BULLETS: 40
}
ADDED_BULLETS_AMOUNT = 20
HEALTH_RESTORED = 25
DAMAGE_MULTIPLIER = 2
MOVEMENT_SPEED_BONUS = 1
POWERUPS_COOLDOWN = 10_000

# colors
ORANGE = '#b68f40'
HOVER_COLOR = '#d7fcd4'
VALID_COLOR = '#23dc3d'
INVALID_COLOR = 'red'
HEALTH_BAR_COLOR = 'red'
HEALTH_BAR_COLOR_SHIELDED = '#ffff00'
HEALTH_BAR_LENGTH = 310
HEALTH_BAR_CHANGE_SPEED = 2

GAME_SCREEN_BACKGROUND_COLOR = '#4f4f57'

# menu
BUTTON_IMAGE = pygame.image.load(os.path.join(ROOT_DIR, 'graphics', 'button.png'))
OVERTIME_BUTTONS_TEXT = ['YES', 'NO']
TIMER_BUTTONS_TEXT = ['30', '60', '120', '180', '300', 'INF']
BULLET_BUTTONS_TEXT = ['30', '50', '99', 'INF']
SUCCESSFUL_LOAD_MSG = 'The map was loaded successfully!'

# font
DEFAULT_FONT = 'font/font.ttf'

# players
DEFAULT_PLAYER_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'player', 'player_idle.png')
PLAYER_HEALTH = 100
PLAYER_MAX_HEALTH = 100
GUN_COOLDOWN = 400
PLAYER_GUN_DAMAGE = 30
MAX_BULLETS = 99
PLAYER_SPEED = 3
HIT_COOLDOWN = 1_000

PLAYER_1_NAME = 'P1'
PLAYER_2_NAME = 'P2'

PLAYER_1_CONTROLS = {
    UP: pygame.K_w,
    DOWN: pygame.K_s,
    LEFT: pygame.K_a,
    RIGHT: pygame.K_d,
    SHOOT: pygame.K_SPACE,
    LOCK: pygame.K_q
}

PLAYER_2_CONTROLS = {
    UP: pygame.K_UP,
    DOWN: pygame.K_DOWN,
    LEFT: pygame.K_LEFT,
    RIGHT: pygame.K_RIGHT,
    SHOOT: pygame.K_RETURN,
    LOCK: pygame.K_BACKSLASH
}

# bullets
DEFAULT_BULLET_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'bullet', 'bullet.png')
BULLET_SPEED = 35

BULLET_OFFSET = {
    (1, 0): (15, 8),
    (1, -1): (15, 15),
    (0, -1): (8, -15),
    (-1, -1): (5, -5),
    (-1, 0): (-15, -9),
    (-1, 1): (5, 0),
    (0, 1): (-9, 15),
    (1, 1): (0, 12)
}

# border
DEFAULT_BORDER_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'border', 'border.png')

# crate
DEFAULT_CRATE_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'crate', 'crate.png')
CRATE_HEALTH = 60

# mouse
DEFAULT_MOUSE_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'mouse', 'mouse.png')
MOUSE_DAMAGE = 15
MOUSE_SPEED = 2
CHANGE_DIRECTION_PROB = 0.005
MOUSE_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Map variables
COL_SIZE = 28
ROW_SIZE = 14
HORIZONTAL_BORDER = 0, 13
VERTICAL_BORDER = 0, 27
WALL = '#'
CRATE = 'c'
MOUSE = 'm'
PLAYER_1 = '1'
PLAYER_2 = '2'
BLANK_SPACE = ' '
ALL_SYMBOLS = WALL, CRATE, MOUSE, PLAYER_1, PLAYER_2, BLANK_SPACE
PLAYER_SYMBOLS = PLAYER_1, PLAYER_2

# Scoreboard
DEFAULT_BAR_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'scoreboard', 'bar.png')
DEFAULT_HEART_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'scoreboard', 'heart.png')
DEFAULT_SHIELD_IMAGE = os.path.join(ROOT_DIR, 'graphics', 'scoreboard', 'shield.png')

HEALTH_BAR_1_POSITION = 50, 755
HEALTH_BAR_2_POSITION = 750, 755
