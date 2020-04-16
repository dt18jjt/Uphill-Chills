from settings import *
import pygame as pg, sys
import random
import time
vec = pg.math.Vector2


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
        #self.standing_frame = self.game.spritesheet.get_image(250, 0, 49, 49)
        self.standing_frame_l = self.game.spritesheet.get_image(386, 0, 38, 41)
        self.standing_frame_r = self.game.spritesheet.get_image(462, 0, 38, 41)
        self.walk_frames_r = [self.game.spritesheet.get_image(424, 0, 38, 41),
                              self.game.spritesheet.get_image(462, 0, 38, 41)]
        self.walk_frames_l = [self.game.spritesheet.get_image(348, 0, 38, 41),
                              self.game.spritesheet.get_image(386, 0, 38, 41)]
        #self.jump_frames = [self.game.spritesheet.get_image(250, 0, 49, 49),
                            #self.game.spritesheet.get_image(299, 0, 49, 49)]
        # Frozen animations
        #self.fstanding_frame = self.game.spritesheet.get_image(0, 0, 49, 49)
        self.fstanding_frame_l = self.game.spritesheet.get_image(136, 0, 38, 41)
        self.fstanding_frame_r = self.game.spritesheet.get_image(212, 0, 38, 41)
        self.fwalk_frames_r = [self.game.spritesheet.get_image(174, 0, 38, 41),
                               self.game.spritesheet.get_image(212, 0, 38, 41)]
        self.fwalk_frames_l = [self.game.spritesheet.get_image(98, 0, 38, 41),
                               self.game.spritesheet.get_image(136, 0, 38, 41)]
        #self.fjump_frames = [self.game.spritesheet.get_image(0, 0, 49, 49),
                             #self.game.spritesheet.get_image(49, 0, 49, 49)]
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
        self.dash = 5
        self.frozen = False
        self.frozentime = 0
        self.frozencooldown = 1000
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
        #for frame in self.jump_frames:
            #frame.set_colorkey(BLACK)
        # frozen
        self.fstanding_frame_l.set_colorkey(BLACK)
        self.fstanding_frame_r.set_colorkey(BLACK)
        for frame in self.fwalk_frames_r:
            frame.set_colorkey(BLACK)
        for frame in self.fwalk_frames_l:
            frame.set_colorkey(BLACK)
        #for frame in self.fjump_frames:
            #frame.set_colorkey(BLACK)


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
        self.animate()
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
            self.jumping = True
            self.jump()
        if not keys[pg.K_UP]:
            self.jumping = False
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
            #self.image.fill(RED)
            self.frozen = False
            PLAYER_ACC = 0.5
            PLAYER_JSTR = -25
        else:
            #self.image.fill(BLUE)
            self.frozen = True
            PLAYER_ACC = 0.2
            PLAYER_JSTR = -15

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
        # show jump animation
        #if self.jumping and not self.walking and not self.frozen:
            #if now - self.last_update > 350:
                #self.last_update = now
                #self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
                #bottom = self.rect.bottom
                #self.image = self.jump_frames[self.current_frame]
                #self.rect = self.image.get_rect()
                #self.rect.bottom = bottom
        # show frozen jump animation
        #elif self.jumping and not self.walking and self.frozen:
            #if now - self.last_update > 350:
                #self.last_update = now
                #self.current_frame = (self.current_frame + 1) % len(self.fjump_frames)
                #bottom = self.rect.bottom
                #self.image = self.fjump_frames[self.current_frame]
                #self.rect = self.image.get_rect()
                #self.rect.bottom = bottom
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


