# All art is created by myself
# Music: [Ice-Shine-Bells by hc https://opengameart.org/content/ice-shine-bells
# Ice Village by KarateStudios https://opengameart.org/content/ice-village
# Time by diana23570  https://opengameart.org/content/time-1
# Win Sound by Listener  https://opengameart.org/content/win-sound-effect
# LedasLuzta by IgnasD https://opengameart.org/content/ice-breakingshattering
# Picked Coin Echo by NenadSimic https://opengameart.org/content/picked-coin-echo
# SnowWalk by IgnasD https://opengameart.org/content/walking-on-snow-sound
# porta by  https://opengameart.org/content/portal-sound
# penguin_RIP 03 by Ouren https://opengameart.org/content/penguin-sfx ]
# Base platformer template from http://kidscancode.org


from settings import *
from sprites import *
from levels import *
import pygame as pg, sys
from pygame.locals import *
from os import path
import time
vec = pg.math.Vector2


# Class for the main game
class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Uphill Chills")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.complete = False
        # Audio
        self.titleImage = pg.image.load("Uphill title.png")
        self.background = pg.image.load("BKG.png")
        self.title_music = pg.mixer.Sound('Audio/Ice-Shine-Bells.ogg')
        self.level_music = pg.mixer.Sound('Audio/Ice Village.wav.ogg')
        self.complete_music = pg.mixer.Sound('Audio/Win sound.ogg')
        self.over_music = pg.mixer.Sound('Audio/Time.ogg')
        self.freeze_sound = pg.mixer.Sound('Audio/LedasLuzta.ogg')
        self.snow_sound = pg.mixer.Sound('Audio/SnowWalk.ogg')
        self.exit_sound = pg.mixer.Sound('Audio/porta.ogg')
        self.star_sound = pg.mixer.Sound('Audio/Picked Coin Echo.ogg')
        self.death_sound = pg.mixer.Sound('Audio/penguin_RIP 03.ogg')
        # All sprite in one group
        self.all_sprites = pg.sprite.Group()
        # Directory
        self.dir = path.dirname(__file__)
        # Spritesheet
        self.spritesheet = Spritesheet(path.join(self.dir, SPRITESHEET))
        # Player class
        self.player = Player(self)
        # Freeze class
        self.freeze = Freeze(self)
        # Pile class
        self.pile = Pile()
        # Sprite groups for classes
        self.exit = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.snowPlatforms = pg.sprite.Group()
        self.icePlatforms = pg.sprite.Group()
        self.allPlatforms = pg.sprite.Group()
        self.snowflakes = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        # name of font
        self.font_name = pg.font.match_font(FONT_NAME)
        # score values
        self.starleft = 3
        self.starcount = 0
        self.startotal = 0
        self.highscore = 0
        # fade sprite
        self.fade = pg.Surface((WIDTH, HEIGHT))
        # loads highscore from text file
        self.load_data()

    def load_data(self):
        # load high score
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        global vec
        self.complete = False
        # Music plays on loop
        self.level_music.play(-1)
        # starting postion for player
        self.player.pos = vec(0, HEIGHT - 220)
        self.player.frozentime = 0
        self.starcount = 0
        self.player.dash = 3
        # starting postion for pile
        self.pile.rect.center = vec(WIDTH / 2, HEIGHT + 300)
        # creates the levels platforms and items
        self.createLevel()
        # adds all platforms and others to it own group
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
        # Updates all sprites in level
        self.all_sprites.update()
        # Snowflake falls downwards
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
        # player on snow platform
        snowhits = pg.sprite.spritecollide(self.player, self.snowPlatforms, False)
        if snowhits:
            self.snow_sound.play()
            snow = snowhits[0]
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
        # player frozen by a snowflake
        frozen = pg.sprite.collide_rect(self.player, self.freeze)
        if frozen:
            self.freeze.reset()
            self.freeze_sound.play()
            pg.time.wait(200)
            self.player.frozentime = time.time()
        # player collecting star
        starhits = pg.sprite.spritecollide(self.player, self.stars, False)
        if starhits:
            self.star_sound.play()
            star = starhits[0]
            star.kill()
            self.starleft -= 1
            self.starcount += 1
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
                    self.level_music.stop()
                    self.playing = False
                    sprite.kill()
        # Complete
        complete = pg.sprite.spritecollide(self.player, self.exit, False)
        if complete:
            self.exit_sound.play()
            self.level_music.stop()
            for sprite in self.all_sprites:
                sprite.kill()
            LEVEL += 1
            self.startotal += self.starcount
            if LEVEL < 5:
                self.fadein(PURPLE)
                self.playing = False
                self.complete = True
            else:
                self.fadein(GREEN)
                self.playing = False
                self.complete = True

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.fadein(BLACK)
                self.running = False

    def draw(self):
        # creates background
        self.screen.blit(self.background, (0, 0))
        # creates sprites in level
        self.all_sprites.draw(self.screen)
        # how many dashes the player has left
        self.draw_text("DASHES LEFT:"+str(self.player.dash), 22, BLUE, WIDTH / 1.3, 15)
        # how many stars are left in the level
        self.draw_text("STARS LEFT:"+str(self.starleft), 22, YELLOW, WIDTH / 5, 15)

    def createLevel(self):
        global LEVEL
        # level 1
        if LEVEL == 1:
            # the stars left equal the amount of stars in the list
            self.starleft = len(STAR_LIST1)
            # creates the amount of platforms there are in the list
            for plat in PLATFORM_LIST1:
                p = Platform(self, *plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            # creates the amount of snow platforms there are in the list
            for snow in SNOW_LIST1:
                s = Snow(self, *snow)
                self.all_sprites.add(s)
                self.snowPlatforms.add(s)
            # creates the amount of ice platforms there are in the list
            for ice in ICE_LIST1:
                i = Ice(self, *ice)
                self.all_sprites.add(i)
                self.icePlatforms.add(i)
            # creates the exit in the level
            for exit in EXIT_LIST1:
                e = Exit(self, *exit)
                self.all_sprites.add(e)
                self.exit.add(e)
            #creates the amount of stars there are in the list
            for star in STAR_LIST1:
                s = Star(self, *star)
                self.all_sprites.add(s)
                self.stars.add(s)
        # level 2
        elif LEVEL == 2:
            self.starleft = len(STAR_LIST2)
            for plat in PLATFORM_LIST2:
                p = Platform(self, *plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            for snow in SNOW_LIST2:
                s = Snow(self, *snow)
                self.all_sprites.add(s)
                self.snowPlatforms.add(s)
            for ice in ICE_LIST2:
                i = Ice(self, *ice)
                self.all_sprites.add(i)
                self.icePlatforms.add(i)
            for exit in EXIT_LIST2:
                e = Exit(self, *exit)
                self.all_sprites.add(e)
                self.exit.add(e)
            for star in STAR_LIST2:
                s = Star(self, *star)
                self.all_sprites.add(s)
                self.stars.add(s)
        # level 3
        elif LEVEL == 3:
            self.starleft = len(STAR_LIST3)
            for plat in PLATFORM_LIST3:
                p = Platform(self, *plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            for snow in SNOW_LIST3:
                s = Snow(self, *snow)
                self.all_sprites.add(s)
                self.snowPlatforms.add(s)
            for ice in ICE_LIST3:
                i = Ice(self, *ice)
                self.all_sprites.add(i)
                self.icePlatforms.add(i)
            for exit in EXIT_LIST3:
                e = Exit(self, *exit)
                self.all_sprites.add(e)
                self.exit.add(e)
            for star in STAR_LIST3:
                s = Star(self, *star)
                self.all_sprites.add(s)
                self.stars.add(s)
        # level 4
        elif LEVEL == 4:
            self.starleft = len(STAR_LIST4)
            for plat in PLATFORM_LIST4:
                p = Platform(self, *plat)
                self.all_sprites.add(p)
                self.platforms.add(p)
            for snow in SNOW_LIST4:
                s = Snow(self, *snow)
                self.all_sprites.add(s)
                self.snowPlatforms.add(s)
            for ice in ICE_LIST4:
                i = Ice(self, *ice)
                self.all_sprites.add(i)
                self.icePlatforms.add(i)
            for exit in EXIT_LIST4:
                e = Exit(self, *exit)
                self.all_sprites.add(e)
                self.exit.add(e)
            for star in STAR_LIST4:
                s = Star(self, *star)
                self.all_sprites.add(s)
                self.stars.add(s)

    def fadein(self, colour):
        # sets the colour of the fade
        self.fade.fill(colour)
        # Becomes more visible as the alpha value increases
        for alpha in range(0, 300):
            self.fade.set_alpha(alpha)
            self.screen.blit(self.fade, (0, 0))
            pg.display.update()
            pg.time.delay(0)
            if alpha >= 300:
                break

    # on start
    def startScreen(self):
        # game splash/start screen
        self.screen.fill(CYAN)
        self.title_music.play(-1)
        # creates title logo
        self.screen.blit(self.titleImage, (0, HEIGHT / 8))
        # text for the title
        self.draw_text("L/R Arrows to move, UP to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Space to DASH",22, WHITE, WIDTH/2, HEIGHT * 6 / 10)
        self.draw_text("Avoid the Snowflakes", 22, WHITE, WIDTH / 2, HEIGHT * 7 / 10)
        self.draw_text("Press any key to play", 22, GREY, WIDTH / 2, HEIGHT * 8 / 10)
        self.draw_text("High Score: " + str(self.highscore), 22, PINK, WIDTH / 2, HEIGHT * 9 / 10)
        pg.display.flip()
        # wait for a key press to procced
        self.wait_for_key()
        self.fadein(WHITE)
        self.title_music.stop()

    # on game over
    def overScreen(self):
        global LEVEL
        # go back to the level
        if not self.running:
            return
        # resets to the beginning
        LEVEL = 1
        self.death_sound.play()
        pg.time.wait(500)
        self.over_music.play()
        self.screen.fill(BLUE)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("The penguin was buried in the snow", 22, WHITE, WIDTH / 2, HEIGHT * 5 / 10)
        # if the total of stars collected is greater than highscore change it to the total
        if self.startotal > self.highscore:
            self.highscore = self.startotal
            self.draw_text("NEW HIGH SCORE!", 22, RED, WIDTH / 2, HEIGHT * 6 / 10)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.startotal))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, PINK, WIDTH / 2, HEIGHT * 7 / 10)
        self.draw_text("Press a key to play again", 22, GREY, WIDTH / 2, HEIGHT * 8 / 10)
        pg.display.flip()
        self.startotal = 0
        pg.time.wait(500)
        self.wait_for_key()
        self.over_music.stop()

    # on completing a level
    def completeScreen(self):
        global LEVEL
        if not self.running:
            return
        self.complete_music.play()
        self.screen.fill(PURPLE)
        self.draw_text("LEVEL COMPlETE", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("TOTAL STARS COLLECTED:" + str(self.startotal), 22, YELLOW, WIDTH / 2, HEIGHT / 2)
        self.draw_text("The penguin is closer to home", 22, WHITE, WIDTH / 2, HEIGHT * 6 / 10)
        self.draw_text("Press any key to next level", 22, GREY, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        pg.time.wait(1000)
        self.wait_for_key()
        self.fadein(WHITE)
        self.complete_music.stop()

    # on completing the game
    def endScreen(self):
        global LEVEL
        if not self.running:
            return
        LEVEL = 1
        self.complete_music.play()
        self.screen.fill(GREEN)
        self.draw_text("Congratulations!!!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("The penguin safely returned home", 22, WHITE, WIDTH / 2, HEIGHT * 4 / 10)
        self.draw_text("TOTAL STARS COLLECTED:" + str(self.startotal), 22, YELLOW, WIDTH / 2, HEIGHT / 2)
        if self.startotal > self.highscore:
            self.highscore = self.startotal
            self.draw_text("NEW HIGH SCORE!", 22, RED, WIDTH / 2, HEIGHT * 5 / 10)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.startotal))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, PINK, WIDTH / 2, HEIGHT * 6 / 10)
        self.draw_text("Press any key to return to play again", 22, GREY, WIDTH / 2, HEIGHT * 7 / 10)
        pg.display.flip()
        pg.time.wait(1000)
        self.wait_for_key()
        self.fadein(WHITE)
        self.complete_music.stop()

    # game procceds on key press
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False

    # creates text
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)






# game class
g = Game()
g.startScreen()
while g.running:
    g.new()
    # the game is not playing or complete
    if not g.playing and not g.complete:
        g.overScreen()
    # the game is not playing but is complete, before level 5
    elif not g.playing and g.complete and LEVEL < 5:
        g.completeScreen()
    # when level 5 is reached
    elif not g.playing and g.complete and LEVEL >= 5:
        g.endScreen()
pg.quit()


