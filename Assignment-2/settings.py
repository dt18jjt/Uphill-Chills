import pygame as pg, sys
import random
PLAY = True
# player values
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 1
PLAYER_JSTR = 25
DASH_COUNT = 5
DASH_TIMER = 0
DASH_STR = 20
# font
FONT_NAME = 'Impact'
# size of window
WIDTH = 360
HEIGHT = 600
# Spritesheet
SPRITESHEET = "SpriteSheet.png"
# Colours
RED = (255, 0, 0)
PINK = (255, 0, 150)
PURPLE = (255, 0, 255)
YELLOW = (255, 180, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 230, 0)
# Level
LEVEL = 1
# highscore file (to reset change text file to 0)
HS_FILE = "highscore"


