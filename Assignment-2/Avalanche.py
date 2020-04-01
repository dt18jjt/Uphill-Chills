from settings import *
from sprites import *
import pygame as pg, sys
from pygame.locals import *
import random
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
        self.platforms = pg.sprite.Group()
        self.snowPlatforms = pg.sprite.Group()
        self.icePlatforms = pg.sprite.Group()
        self.allPlatforms = pg.sprite.Group()
        self.snowflakes = pg.sprite.Group()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.dash = DASH_COUNT

    def new(self):
        global vec
        self.all_sprites.add(self.player, self.freeze, self.pile)
        self.player.pos = vec(0, HEIGHT - 100)
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
            self.events()
            self.update()
            self.draw()
        #while not self.playing:
            #self.overScreen()

    def update(self):
        self.all_sprites.update()
        self.freeze.fall()
        self.pile.fill()
        # player on normal platform
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = -0.12
        # player on snow platform
        snowhits = pg.sprite.spritecollide(self.player, self.snowPlatforms, False)
        for snow in self.snowPlatforms:
            if snowhits and snow.rect.y == self.player.pos.y:
                self.player.pos.y = snowhits[0].rect.top
                self.player.vel.y = 0
                snow.kill()
        # player on ice platform
        icehits = pg.sprite.spritecollide(self.player, self.icePlatforms, False)
        if icehits:
            self.player.pos.y = icehits[0].rect.top
            self.player.vel.y = 0
        frozen = pg.sprite.collide_rect(self.player, self.freeze)
        if frozen:
            self.freeze.reset()

            pass
        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 6:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.allPlatforms:
                plat.rect.y += abs(self.player.vel.y)
                #if plat.rect.top >= HEIGHT:
                   # plat.kill()

        # Die!
        #death = pg.sprite.collide_rect(self.player, self.pile)
        #if death:
            #self.pile.kill()
            #self.player.kill()
            #self.playing = False

        if self.player.rect.bottom > HEIGHT / 1.2:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < -1000:
                    sprite.kill()


        # spawn new platforms to keep same average number
        #while len(self.platforms) < 6:
            #width = random.randrange(50, 100)
           # p = Platform(random.randrange(0, WIDTH - width),
                         #random.randrange(-60, -30),
                         #width, 20)
            #self.platforms.add(p)
            #self.allPlatforms.add(p)
            #self.all_sprites.add(p)





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
        pass

    def overScreen(self):
        self.screen.fill(BLACK)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)







g = Game()

while g.running:
    g.new()
pg.quit()


