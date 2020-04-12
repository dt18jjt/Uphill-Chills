from settings import *
import pygame as pg, sys
import random
import time
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self,  game):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (0, HEIGHT - 100)
        self.pos = vec(0, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dash = 5
        self.frozen = False
        self.frozentime = 0
        self.frozencooldown = 1000
        self.dashlast = pg.time.get_ticks()
        self.dashcooldown = 1000

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.allPlatforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = PLAYER_JSTR

    def update(self):
        global PLAY
        global vec, PLAYER_FRICTION
        global DASH_TIMER
        global DASH_STR
        global PLAYER_ACC
        global PLAYER_JSTR
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        slide = pg.sprite.spritecollide(self, self.game.icePlatforms, False)
        now = pg.time.get_ticks()
        # if the player is on a ice platform the friction is reduced making it slide
        if slide:
            PLAYER_FRICTION = 0
        else:
            PLAYER_FRICTION = -0.12
        # moves to the left
        if keys[pg.K_LEFT]:
            PLAYER_ACC = 0.5
            self.acc.x = -PLAYER_ACC
            if keys[pg.K_SPACE] and self.dash > 0 and now - self.dashlast >= self.dashcooldown:
                self.dash -= 1
                PLAYER_ACC = DASH_STR
                self.acc.x = -PLAYER_ACC
                self.dashlast = now
        # moves to the right
        if keys[pg.K_RIGHT]:
            PLAYER_ACC = 0.5
            self.acc.x = PLAYER_ACC
            if keys[pg.K_SPACE] and self.dash > 0 and now - self.dashlast >= self.dashcooldown:
                self.dash -= 1
                PLAYER_ACC = DASH_STR
                self.acc.x = PLAYER_ACC
                self.dashlast = now
        if keys[pg.K_UP]:
            self.jump()
        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        # stops at edge
        if self.pos.x >= WIDTH - 15:
            self.pos.x = WIDTH - 15
        if self.pos.x <= 15:
            self.pos.x = 15
        if self.pos.y <= 0:
            self.game.playing = False
        # when frozen
        if time.time() - self.frozentime > 2:
            self.image.fill(RED)
            PLAYER_ACC = 0.5
            PLAYER_JSTR = -25
        else:
            self.image.fill(BLUE)
            PLAYER_ACC = 0.2
            PLAYER_JSTR = -15
            # wrap around the sides of the screen
        #if self.pos.x > WIDTH:
            #self.pos.x = 0
        #if self.pos.x < 0:
            #self.pos.x = WIDTH


# Class for normal platforms
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Class for snow platforms
class Snow(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fall = False

    def destroy(self):
        self.fall = True


class Ice(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Freeze(pg.sprite.Sprite):

    def __init__(self,):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(10, WIDTH - 10), 0)
        self.pos = vec(random.randrange(10, WIDTH - 10), 10)
        self.speed = 5

    def fall(self):
        self.rect.center = self.pos
        self.pos.y += self.speed
        if self.pos.y > HEIGHT:
            self.reset()

    def reset(self):
        global vec
        self.pos = vec(random.randrange(10, WIDTH - 10), 10)

class Pile(pg.sprite.Sprite):

    def __init__(self):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.height = 150
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT + 300)
        self.rect.center = (WIDTH / 2, HEIGHT + 350)

    def fill(self):
        self.rect.center = self.pos
        self.pos.y -= 1


class Exit(pg.sprite.Sprite):

    def __init__(self,x, y):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 70))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


