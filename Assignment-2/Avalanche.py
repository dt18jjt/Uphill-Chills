from settings import *
from sprites import *
import pygame as pg, sys
from pygame.locals import *
import random
import time
vec = pg.math.Vector2

# Class for the main game
class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Avalanche")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.all_sprites = pg.sprite.Group()
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


    def new(self):
        global vec
        self.player.pos = vec(0, HEIGHT - 100)
        self.pile.rect.center = vec(WIDTH / 2, HEIGHT + 350)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for snow in SNOW_LIST:
            s = Snow(*snow)
            self.all_sprites.add(s)
            self.snowPlatforms.add(s)
        for ice in ICE_LIST:
            i = Ice(*ice)
            self.all_sprites.add(i)
            self.icePlatforms.add(i)
        for exit in EXIT_LIST:
            e = Exit(*exit)
            self.all_sprites.add(e)
            self.exit.add(e)
        self.allPlatforms.add(self.platforms,self.snowPlatforms, self.icePlatforms,self.exit)
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
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = -0.12
        now = pg.time.get_ticks()
        snowhits = pg.sprite.spritecollide(self.player, self.snowPlatforms, False)
        for snow in self.snowPlatforms:
            if snowhits and snow.rect.y == self.player.pos.y:
                snow.kill()
        # player on ice platform
        icehits = pg.sprite.spritecollide(self.player, self.icePlatforms, False)
        if icehits:
            self.player.pos.y = icehits[0].rect.top
            self.player.vel.y = 0
        frozen = pg.sprite.collide_rect(self.player, self.freeze)
        if frozen:
            self.freeze.reset()
            pg.time.wait(200)
            self.player.frozentime = time.time()
            pass
        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.allPlatforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                   plat.kill()
        # Die
        if self.player.rect.bottom > HEIGHT/1.2:
            death = pg.sprite.collide_rect(self.player, self.pile)
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if death:
                    self.playing = False
                    sprite.kill()

        # Complete
        complete = pg.sprite.spritecollide(self.player, self.exit, False)
        if complete:
            LEVEL += 1
            self.completeScreen()




    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False



    def draw(self):
        self.screen.fill(CYAN)
        self.all_sprites.draw(self.screen)
        self.draw_text("DASH:"+str(self.player.dash), 22, WHITE, WIDTH / 2, 15)



    def startScreen(self):
        # game splash/start screen
        self.screen.fill(CYAN)
        self.draw_text("UPHILL CHILLS", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("L/R Arrows to move, UP to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Space to DASH",22, WHITE, WIDTH/2, HEIGHT * 5/8)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def overScreen(self):
        if not self.running:
            return
        self.screen.fill(BLUE)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def completeScreen(self):
        global LEVEL
        print(LEVEL)
        self.screen.fill(PURPLE)
        self.draw_text("LEVEL COMPlETE", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to next level", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()



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


