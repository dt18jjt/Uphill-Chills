from settings import *
import pygame as pg, sys
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self,  game):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(0, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

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
        global DASH_COUNT
        global DASH_TIMER
        global DASH_STR
        global PLAYER_ACC
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        slide = pg.sprite.spritecollide(self, self.game.icePlatforms, False)
        # if the player is on a ice platform the friction is reduced making it slide
        if slide:
            PLAYER_FRICTION = 0
        else:
            PLAYER_FRICTION = -0.12
        # moves to the left
        if keys[pg.K_LEFT]:
            PLAYER_ACC = 0.5
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_LEFT]:
            PLAYER_ACC = 0.5
            self.acc.x = -PLAYER_ACC
        # dashes to the left
        if keys[pg.K_LEFT] and keys[pg.K_SPACE] and DASH_COUNT > 0:
            DASH_COUNT -= 1
            PLAYER_ACC = DASH_STR
            self.acc.x = -PLAYER_ACC
        # moves to the right
        if keys[pg.K_RIGHT]:
            PLAYER_ACC = 0.5
            self.acc.x = PLAYER_ACC
        # dashes to the right
        if keys[pg.K_RIGHT] and keys[pg.K_SPACE] and DASH_COUNT > 0:
            DASH_COUNT -= 1
            PLAYER_ACC = DASH_STR
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP]:
            self.jump()
        # dash countdown
        while DASH_COUNT <= 0:
            DASH_TIMER += 0.01
            if DASH_TIMER >= 3:
                DASH_COUNT += 1
                DASH_TIMER = 0

        # apply friction
        #if self.vel.y <= 0:
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
        # wrap around the sides of the screen
        #if self.pos.x > WIDTH:
            #self.pos.x = 0
        #if self.pos.x < 0:
            #self.pos.x = WIDTH




class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Snow(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, d):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.destroy = d


class Ice(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



