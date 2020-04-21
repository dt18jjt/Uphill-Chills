# All art is created by myself
# Base platformer template from http://kidscancode.org
from settings import *
from sprites import *
from levels import *
import pygame as pg, sys
from pygame.locals import *
from os import path
import time
vec = pg.math.Vector2
titleImage = pg.image.load("Uphill title.png")
background = pg.image.load("BKG.png")

# Class for the main game
class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Uphill Chills")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.all_sprites = pg.sprite.Group()
        self.dir = path.dirname(__file__)
        self.spritesheet = Spritesheet(path.join(self.dir, SPRITESHEET))
        self.player = Player(self)
        self.freeze = Freeze()
        self.pile = Pile()
        self.exit = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.snowPlatforms = pg.sprite.Group()
        self.icePlatforms = pg.sprite.Group()
        self.allPlatforms = pg.sprite.Group()
        self.snowflakes = pg.sprite.Group()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.stars = pg.sprite.Group()
        self.starcount = 3
        self.startotal = 0
        self.highscore = 0
        self.load_data()

    def load_data(self):
        # load high score
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image

    def new(self):
        global vec
        self.player.pos = vec(0, HEIGHT - 220)
        self.player.frozentime = 0
        self.player.dash = 5
        self.pile.rect.center = vec(WIDTH / 2, HEIGHT + 300)
        self.createLevel()
        self.allPlatforms.add(self.platforms,self.snowPlatforms, self.icePlatforms, self.exit, self.stars)
        self.all_sprites.add(self.player, self.freeze, self.pile)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            pg.display.update()
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def update(self):
        global vec
        global LEVEL
        self.all_sprites.update()
        self.freeze.fall()
        # platforms moving down
        for plat in self.allPlatforms:
            plat.rect.y += 1
        # player on normal platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
        now = pg.time.get_ticks()
        # player on snow platform
        snowhits = pg.sprite.spritecollide(self.player, self.snowPlatforms, False)
        for snow in self.snowPlatforms:
            if snowhits and snow.rect.y == self.player.pos.y:
                snow.kill()
        # player on ice platform
        icehits = pg.sprite.spritecollide(self.player, self.icePlatforms, False)
        if icehits:
            lowest = icehits[0]
            for icehit in icehits:
                if icehit.rect.bottom > lowest.rect.bottom:
                    lowest = icehit
            if self.player.pos.y < lowest.rect.bottom:
                self.player.pos.y = lowest.rect.top
                self.player.vel.y = 0
                self.player.jumping = False
        frozen = pg.sprite.collide_rect(self.player, self.freeze)
        if frozen:
            self.freeze.reset()
            pg.time.wait(200)
            self.player.frozentime = time.time()
        starhits = pg.sprite.spritecollide(self.player, self.stars, False)
        if starhits:
            star = starhits[0]
            star.kill()
            self.starcount -= 1
            self.startotal += 1
        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.allPlatforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.y >= HEIGHT:
                    plat.kill()
        # Die
        if self.player.rect.bottom > HEIGHT/1.2:
            death = pg.sprite.collide_rect(self.player, self.pile)
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if death or self.player.pos.y > HEIGHT + 30:
                    self.playing = False
                    sprite.kill()

        # Complete
        complete = pg.sprite.spritecollide(self.player, self.exit, False)
        if complete:
            for sprite in self.all_sprites:
                sprite.kill()
            LEVEL += 1
            self.completeScreen()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False


    def draw(self):
        self.screen.blit(background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text("DASHES LEFT:"+str(self.player.dash), 22, BLUE, WIDTH / 1.3, 15)
        self.draw_text("STARS LEFT:"+str(self.starcount), 22, YELLOW, WIDTH / 5, 15)


    def createLevel(self):
        global LEVEL
        if LEVEL == 1:
            self.starcount = 3
            for plat in PLATFORM_LIST1:
                p = Platform(*plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            for snow in SNOW_LIST1:
                s = Snow(*snow)
                self.all_sprites.add(s)
                self.snowPlatforms.add(s)
            for ice in ICE_LIST1:
                i = Ice(*ice)
                self.all_sprites.add(i)
                self.icePlatforms.add(i)
            for exit in EXIT_LIST1:
                e = Exit(*exit)
                self.all_sprites.add(e)
                self.exit.add(e)
            for star in STAR_LIST1:
                s = Star(*star)
                self.all_sprites.add(s)
                self.stars.add(s)
        elif LEVEL == 2:
            self.starcount = 4
            for plat in PLATFORM_LIST2:
                p = Platform(*plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            for snow in SNOW_LIST2:
                s = Snow(*snow)
                self.all_sprites.add(s)
                self.snowPlatforms.add(s)
            for ice in ICE_LIST2:
                i = Ice(*ice)
                self.all_sprites.add(i)
                self.icePlatforms.add(i)
            for exit in EXIT_LIST2:
                e = Exit(*exit)
                self.all_sprites.add(e)
                self.exit.add(e)
            for star in STAR_LIST2:
                s = Star(*star)
                self.all_sprites.add(s)
                self.stars.add(s)

    def startScreen(self):
        # game splash/start screen
        self.screen.fill(CYAN)
        self.screen.blit(titleImage, (0, HEIGHT / 8))
        self.draw_text("L/R Arrows to move, UP to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Space to DASH",22, WHITE, WIDTH/2, HEIGHT * 5/8)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT * 5 / 6)
        pg.display.flip()
        self.wait_for_key()

    def overScreen(self):
        if not self.running:
            return
        self.screen.fill(BLUE)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.startotal > self.highscore:
            self.highscore = self.startotal
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT * 5 / 6)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.startotal))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT * 5 / 6)
        pg.display.flip()
        self.startotal = 0
        self.wait_for_key()

    def completeScreen(self):
        #if not self.running:
            #return
        global LEVEL
        print(LEVEL)
        self.screen.fill(PURPLE)
        self.draw_text("LEVEL COMPlETE", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("STARS COLLECTED:" + str(self.startotal), 22, YELLOW, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to next level", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        self.new()



    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)







g = Game()
g.startScreen()
while g.running:
    g.new()
    g.overScreen()
pg.quit()


