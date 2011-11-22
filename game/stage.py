import os, pygame, time
import random
from pygame.locals import *
from sprites import *
import utils

class Stage():
    def __init__(self, screen):
        self.screen = screen
        self.initialise()
        self.debug = False

    def player_dies(self):
        self.game_finished = True

    def initialise(self):
        #Initialize Everything
        pygame.display.flip()

        self.game_paused = False
        #sounds
        self.sounds = {};
        self.sounds['plop'] = utils.load_sound('plop.wav')

        #Create The Backgound
        self.background, foo = utils.load_image('background.png')

        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.platforms          = pygame.sprite.Group()
        self.flying_scores      = pygame.sprite.Group()
        self.sprites            = pygame.sprite.Group()
        self.hud                = pygame.sprite.Group()

        for i in range(0,640,20):
            self.platforms.add(Platform(pygame.Rect(i, 600,10,10)))
        for i in range(15):
            self.platforms.add(Platform(pygame.Rect(random.randint(0,480), random.randint(0,640),10,10)))

        self.player = Player(self)
        self.sprites.add(self.player)

        #game variables
        self.score  = Score_Meter((10,10,10,10))
        self.hud.add(self.score)

        self.font = utils.load_font('chitown.ttf', 20)

        self.game_started   = False
        self.game_finished  = False
        self.level_finished = False


    def handle_event(self):
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                #exit
                return
            elif event.type == KEYDOWN:
                if self.game_finished == False:
                    self.game_started = True
                if event.key == K_ESCAPE:
                    self.game_finished = True
                elif event.key == K_RIGHT:
                    self.player.move_right()
                elif event.key == K_LEFT:
                    self.player.move_left()
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.player.stop()
                elif event.key == K_LEFT:
                    self.player.stop()
        return False

    #Main Loop, return  bool = if the game is over
    def loop(self):
        exit = self.handle_event()
        self.screen.blit(self.background, (0, 0))
        if self.game_finished:
            return True
        if exit == True:
            return True
        if self.game_started == False:
            start_text = self.font.render('Press any key to start', 2, (255,255,255))
            self.screen.blit(start_text, (100, 200))
            pygame.display.flip()
            return False

        if self.game_paused == 1:
            start_text = self.font.render('Game paused', 2, (255,255,255))
            self.screen.blit(start_text, (150, 200))
            pygame.display.flip()
            return False


        #Check if the playr has bounced in any platform
        collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in collisions:
            if platform.rect.top > self.player.rect.top+self.player.rect.height-20 and\
                platform.rect.left < self.player.rect.left + self.player.rect.width /2 and\
                platform.rect.left + platform.rect.width > self.player.rect.left + self.player.rect.width/2:
                self.player.bounce()
                move_platforms = self.player.rect.top + self.player.rect.height + 40 #-40 is the gap
                for platform in self.platforms:
                    platform.move_down(move_platforms)
                break

        #draw the level
        self.hud.update()
        self.sprites.update()
        self.platforms.update()
        self.flying_scores.update()

        if self.game_finished == True:
            gameover_text = self.font.render("Game Over", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 200))
            gameover_text = self.font.render("Press Esc", 2, (255, 255, 255))
            self.screen.blit(gameover_text, (200, 230))
        else:
            self.hud.draw(self.screen)
            self.sprites.draw(self.screen)
            self.platforms.draw(self.screen)
            self.flying_scores.draw(self.screen)

        #draw all the groups of sprites
        pygame.display.flip()
        return False

    #Game Over




