from settings import *
import pygame as pg, sys
import random
import time
vec = pg.math.Vector2
platform_image = pg.image.load("Sprites/Platform.png")
pile_image = pg.image.load("Pile.png")


# Class for spritesheet
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        #image = pg.transform.scale(image, (width / 2, height / 2))
        return image

# Class for player
class Player(pg.sprite.Sprite):

    def __init__(self,  game):
        global vec
        pg.sprite.Sprite.__init__(self)
        # Game class
        self.game = game
        # Normal animations
        self.standing_frame_l = self.game.spritesheet.get_image(38, 112, 38, 41)
        self.standing_frame_r = self.game.spritesheet.get_image(76, 112, 38, 41)
        self.walk_frames_r = [self.game.spritesheet.get_image(0, 153, 38, 41),
                              self.game.spritesheet.get_image(76, 112, 38, 41)]
        self.walk_frames_l = [self.game.spritesheet.get_image(0, 112, 38, 41),
                              self.game.spritesheet.get_image(38, 112, 38, 41)]
        # Frozen animations
        self.fstanding_frame_l = self.game.spritesheet.get_image(0, 71, 38, 41)
        self.fstanding_frame_r = self.game.spritesheet.get_image(76, 71, 38, 41)
        self.fwalk_frames_r = [self.game.spritesheet.get_image(38, 71, 38, 41),
                               self.game.spritesheet.get_image(76, 71, 38, 41)]
        self.fwalk_frames_l = [self.game.spritesheet.get_image(60, 30, 38, 41),
                               self.game.spritesheet.get_image(0, 71, 38, 41)]
        self.walking = False
        self.jumping = False
        self.direction = 0
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frame_l
        self.image.set_colorkey(BLACK)
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (0, HEIGHT - 100)
        self.pos = vec(0, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dash = 3
        self.frozen = False
        self.frozentime = 0
        self.dashlast = pg.time.get_ticks()
        self.dashcooldown = 1000


    def load_images(self):
        # normal
        self.standing_frame_l.set_colorkey(BLACK)
        self.standing_frame_r.set_colorkey(BLACK)
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
        # frozen
        self.fstanding_frame_l.set_colorkey(BLACK)
        self.fstanding_frame_r.set_colorkey(BLACK)
        for frame in self.fwalk_frames_r:
            frame.set_colorkey(BLACK)
        for frame in self.fwalk_frames_l:
            frame.set_colorkey(BLACK)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.allPlatforms, False)
        self.rect.x -= 1
        if hits and not self.jumping:
            self.vel.y = PLAYER_JSTR
            self.jumping = True

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        global PLAY
        global vec, PLAYER_FRICTION
        global DASH_TIMER
        global DASH_STR
        global PLAYER_ACC
        global PLAYER_JSTR
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        slide = pg.sprite.spritecollide(self, self.game.icePlatforms, False)
        now = pg.time.get_ticks()
        # if the player is on a ice platform the acceleration is increased making it slide
        if slide:
            if self.direction == 0:
                self.acc.x = -1
            elif self.direction == 1:
                self.acc.x = 1
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
            if not keys[pg.K_UP]:
                self.jump_cut()
        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
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
            self.frozen = False
            PLAYER_ACC = 0.5
            PLAYER_JSTR = -25
        else:
            self.frozen = True
            PLAYER_ACC = 0.1
            PLAYER_JSTR = -20

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking and not self.frozen and not self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                    self.direction = 1
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    self.direction = 0
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show frozen walk animation
        elif self.walking and self.frozen and not self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.fwalk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.fwalk_frames_r[self.current_frame]
                    self.direction = 1
                else:
                    self.image = self.fwalk_frames_l[self.current_frame]
                    self.direction = 0
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking and not self.frozen:
            if now - self.last_update > 350:
                self.last_update = now
                #self.current_frame = (self.current_frame + 1) % len(self.standing_frame)
                bottom = self.rect.bottom
                if self.direction == 0:
                    self.image = self.standing_frame_l
                elif self.direction == 1:
                    self.image = self.standing_frame_r
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show frozen idle animation
        if not self.jumping and not self.walking and self.frozen:
            if now - self.last_update > 350:
                self.last_update = now
                #self.current_frame = (self.current_frame + 1) % len(self.fstanding_frame)
                bottom = self.rect.bottom
                if self.direction == 0:
                    self.image = self.fstanding_frame_l
                elif self.direction == 1:
                    self.image = self.fstanding_frame_r
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


# Class for normal platforms
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        global platform_image
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.fill = self.game.spritesheet.get_image(60, 0, 60, 30)
        self.image = pg.transform.scale(self.fill, (w, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Class for snow platforms
class Snow(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.fill = self.game.spritesheet.get_image(0, 30, 60, 30)
        self.image = pg.transform.scale(self.fill, (w, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fall = False

    def destroy(self):
        self.fall = True


class Ice(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.fill = self.game.spritesheet.get_image(0, 0, 60, 30)
        self.image = pg.transform.scale(self.fill, (w, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Freeze(pg.sprite.Sprite):

    def __init__(self, game):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.fill = [self.game.spritesheet.get_image(49, 251, 50, 50),
                     self.game.spritesheet.get_image(0, 301, 50, 50)]
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(49, 251, 50, 50)
        self.image = pg.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(10, WIDTH - 10), 0)
        self.pos = vec(random.randrange(10, WIDTH - 10), 10)
        self.speed = 5

    def load_images(self):
        # on each frame
        for frame in self.fill:
            frame.set_colorkey(BLACK)

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.fill)
            self.image = self.fill[self.current_frame]
            self.image = pg.transform.scale(self.image, (30, 30))

    def fall(self):
        self.animate()
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
        self.image = pile_image
        #self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT + 300)
        self.rect.center = (WIDTH / 2, HEIGHT + 350)


class Exit(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image(50, 351, 70, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Star(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        global vec
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.fill = [self.game.spritesheet.get_image(50, 301, 50, 50),
                      self.game.spritesheet.get_image(0, 351, 50, 50)]
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(50, 301, 50, 50)
        self.image = pg.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        # on each frame
        for frame in self.fill:
            frame.set_colorkey(BLACK)

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.fill)
            self.image = self.fill[self.current_frame]
            self.image = pg.transform.scale(self.image, (30, 30))

    def update(self):
        self.animate()


