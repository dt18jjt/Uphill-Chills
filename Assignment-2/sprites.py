from settings import *
import random
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
        self.rect.center = (0, HEIGHT - 100)
        self.pos = vec(0, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dash = 5
        self.cooldown = 0
        self.frozen = False

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
            if keys[pg.K_SPACE] and self.dash > 0 and self.cooldown == 0:
                self.cooldown = 1
                self.dash -= 1
                PLAYER_ACC = DASH_STR
                self.acc.x = -PLAYER_ACC
        # moves to the right
        if keys[pg.K_RIGHT]:
            PLAYER_ACC = 0.5
            self.acc.x = PLAYER_ACC
            if keys[pg.K_SPACE] and self.dash > 0:
                self.dash -= 1
                PLAYER_ACC = DASH_STR
                self.acc.x = PLAYER_ACC
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
        # wrap around the sides of the screen
        #if self.pos.x > WIDTH:
            #self.pos.x = 0
        #if self.pos.x < 0:
            #self.pos.x = WIDTH

    def dashing(self):
        # dash countdown
        while self.dash <= 0:
            self.cooldown += 0.01
            if self.cooldown >= 10:
                self.dash += 1
                self.cooldown = 0


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
        self.speed = random.randrange(5, 10)

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
        self.image = pg.Surface((WIDTH, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT + 100)
        self.pos = vec(0, HEIGHT + 100)

    def fill(self):
        self.height += 1
        pg.transform.scale(self.image, (WIDTH, self.height))



