import os, pygame, time, random, math
from pygame.locals import *
import utils
#import pdb

#Sprite that shows a number fading out, when faded dies
class Flying_Score(pygame.sprite.Sprite):

    def __init__(self, position, score):
        self.age = 0 #To animate it and decide when to kill()
        pygame.sprite.Sprite.__init__(self)
        font        = utils.load_font('chitown.ttf', 20)
        score       = '{0}'.format(score)
        surf_text   = font.render(score, 2, (10,10,10))
        self.rect   = position.copy()
        self.image  = pygame.Surface(font.size(score))
        #Blitting into a new Surface is needed to apply alpha, doesn't work in the surface from font.render
        self.image.blit(surf_text, (0,0))
        self.image.set_colorkey((0,0,0))

    #Move upwards and dither a bit
    def update(self):
        new_alpha = max(0,255-self.age * 10)
        self.image.set_alpha (new_alpha)
        self.age += 1
        self.rect.top -= self.age/4 + random.randint(1,2)
        self.rect.left -= 10*math.sin(self.age/4)
        if self.age > 25:
            self.kill()

class Score_Meter(pygame.sprite.Sprite):

    font = False

    def __init__(self, position):
        if Score_Meter.font == False:
            Score_Meter.font = utils.load_font('chitown.ttf', 36)
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.target_score = 0
        self.rect = position
        self.reload_image()

    def reload_image(self):
        score_text = 'Score: {0}'.format((self.score))
        text = Score_Meter.font.render(score_text, 1, (255, 0, 0))
        text_shadow = Score_Meter.font.render(score_text, 1, (255,255,255))
        self.image = pygame.Surface(Score_Meter.font.size(score_text))
        self.image.blit(text_shadow, (2,2))
        self.image.blit(text, (0,0))
        self.image.set_colorkey((0,0,0))

    def add_score(self, score):
        self.target_score += score

    def update(self):
        if self.target_score > self.score:
            self.score += (self.target_score - self.score ) / 10 + random.randint(5,9)
            if self.score > self.target_score:
                self.score = self.target_score
            self.reload_image()


class Player(pygame.sprite.Sprite):

    JUMPING = 0
    FALLING = 1

    def __init__(self, stage):
        self.stage = stage
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('player.png')
        self.jump_age       = 0
        self.rect.top       = 500
        self.x_acc          = 0
        self.jump_frames    = 75
        self.jump_height    = 150
        self.state          = Player.JUMPING
        self.moving         = False
        self.y_reference = self.rect.top

        def jump(x):
            x = 3.14 / self.jump_frames * x
            temp = self.jump_height*math.fabs(math.sin(x))
            return temp
        self.y_positions = map(jump, range(0,self.jump_frames,1))

    def move_right(self):
        self.moving = True 
        self.x_acc = 4

    def move_left(self):
        self.moving = True 
        self.x_acc = -4
    
    def stop(self):
        self.moving = False 

    def bounce(self):
        if self.jump_age > self.jump_frames / 2:
            #print "Bounce"
            self.y_reference = self.rect.top
            self.jump_age = 0
            self.state = Player.JUMPING

    def update(self):

        #Deccelerate and move
        #pdb.set_trace()

        if self.moving == False:
            self.x_acc *= 0.9
            if math.fabs(self.x_acc) < 0.2:
                self.x_acc = 0
        self.rect.left += self.x_acc

        #bounce in the floor
        if self.rect.top + self.rect.height > 630:
            self.stage.player_dies()

        #bouncing against the walls
        if self.rect.left < 0 or self.rect.left + self.rect.width > 480:
            self.x_acc = - self.x_acc
            self.moving = False

        #End of jump
        #print "{0}/{1}".format(self.jump_age, self.jump_frames)
        if self.jump_age == self.jump_frames - 1:
            #print "Falling"
            self.state = Player.FALLING
            self.y_reference += 15
            pass
        else:
            if self.jump_age >= self.jump_frames-1:
                self.y_reference += 1#self.jump_age = 0
            else:
                self.jump_age += 1

        #bouncing
        jumping_pos = self.y_positions[self.jump_age]
        top = self.y_reference - jumping_pos
        self.rect.top = top

class Platform(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image('platform.png')
        self.rect.top = position.top
        self.rect.left = position.left
        self.new_top = position.top
        self.already_bounced = False
    def update(self):
        if self.new_top > self.rect.top :
            self.rect.top += 1
        if self.rect.top > 640:
            print "kill"
            self.kill()

    def move_down(self, new_top):
        self.new_top = self.rect.top + (640 - new_top)

