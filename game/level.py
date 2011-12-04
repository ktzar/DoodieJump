import random
import pygame
import utils


"""Level"""
class Level():
    def __init__(self, stage_file='level_1'):
        self.scroll = 0
        self.level_data, self.rect = utils.load_image('{0}.png'.format(stage_file))
        self.ratio = 8 #ratio of pixel in stage file / pixel in game
        self.y_ratio = 32 #vertical ratio of pixel in stage file / pixel in game

        self.colors = { \
            "platform":(0,0,0,255), \
            'bg':(225,225,225,255) \
        }

        self.data = []
        for y in range(0, self.rect.height):
            #will store top and bottom limits and append it to self.limits
            #to control the ship not getting over this
            row = []
            for x in range(0,self.rect.width):
                if self.level_data.get_at((x,self.rect.height - y-1)) == self.colors["platform"]:
                    row.append(1)
                else:
                    row.append(0)
            self.data.append(row)
        print self.data

#return the enemies in the current scroll position (self.scrolled + self.ratio).
#only return enemies if self.scrolled%self.ratio == 0 (each pixel in the stage is one enemy, not self.ratio
    def platforms(self):
        platforms   = []
        for x in range(self.rect.width-1):
            print "Checking {0},{1}".format(self.scroll,x)
            if self.data[self.scroll][x] == 1:
                platforms.append(x)
        return platforms


    def level_finished(self):
        if self.scroll > len(self.data) :
            return True
        else:
            return False
        


        
