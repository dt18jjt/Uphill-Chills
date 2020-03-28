from settings import *
from sprites import *
import pygame as pg, sys
from pygame.locals import *
import random


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
        self.platforms = pg.sprite.Group()
        self.snowPlatforms = pg.sprite.Group()
        self.icePlatforms = pg.sprite.Group()
        self.allPlatforms = pg.sprite.Group()
        self.uiFont = pg.font.SysFont("impact", 16)
        self.dashText = "DASH:" + str(DASH_COUNT)

    def new(self):
        self.all_sprites.add(self.player)
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
        self.allPlatforms.add(self.platforms,self.snowPlatforms, self.icePlatforms)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            pg.display.update()
            self.clock.tick(60)
            self.Text()
            self.events()
            self.update()
            self.draw()
        while not self.playing:
            self.overScreen()

    def update(self):
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = -0.12
        snowhits = pg.sprite.spritecollide(self.player, self.snowPlatforms, False)
        if snowhits:
            self.player.pos.y = snowhits[0].rect.top
            self.player.vel.y = 0
        icehits = pg.sprite.spritecollide(self.player, self.icePlatforms, False)
        if icehits:
            self.player.pos.y = icehits[0].rect.top
            self.player.vel.y = 0


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                #sys.exit()

    def draw(self):
        self.screen.fill(CYAN)
        self.all_sprites.draw(self.screen)



    def startScreen(self):
        pass

    def overScreen(self):
        self.screen.fill(BLACK)

    def Text(self):
        self.screen.blit(self.uiFont.render(self.dashText, True, WHITE), (10, 10))







g = Game()

while g.running:
    g.new()

pg.quit()


