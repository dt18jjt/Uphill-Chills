import pygame as pg, sys
import random
PLAY = True

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 1
PLAYER_JSTR = 25
DASH_COUNT = 5
DASH_TIMER = 0
DASH_STR = 20
FONT_NAME = 'Impact'
# size of window
WIDTH = 360
HEIGHT = 600
# Spritesheet
SPRITESHEET = "PengSheet.png"
# Colours
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
# Level
LEVEL = 1
# highscore file
HS_FILE = "highscore"


