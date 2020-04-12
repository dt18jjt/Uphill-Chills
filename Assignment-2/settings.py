import pygame as pg, sys
import random
PLAY = True

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 1
PLAYER_JSTR = -25
DASH_COUNT = 5
DASH_TIMER = 0
DASH_STR = 20
FONT_NAME = 'Impact'
WIDTH = 360
HEIGHT = 600
RED = (255, 0, 0)
PINK = (255, 0, 150)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

LEVEL = 1

PLATFORM_LIST = [(0, HEIGHT - 50, 150, 20), (200, HEIGHT - 50, 200, 20), (100, HEIGHT - 150, 100, 20),
                 (0, HEIGHT - 250, 100, 20),(300, HEIGHT - 250, 100, 20),(50, HEIGHT - 350, 100, 20),
                 (200, HEIGHT - 450, 100, 20),(100, HEIGHT - 550, 100, 20),(300, HEIGHT - 650, 100, 20),
                 (0, HEIGHT - 650, 150, 20), (150, HEIGHT - 750, 100, 20)]
SNOW_LIST = [(150, HEIGHT - 50, 50, 20), (100, HEIGHT - 250, 50, 20)]
ICE_LIST = [(200, HEIGHT - 150, 100, 20)]
EXIT_LIST = [(180, HEIGHT - 820)]
FLAKE_LIST = [(random.randrange(10, WIDTH - 10), 0)]