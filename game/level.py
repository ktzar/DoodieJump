import random
import pygame
import utils


"""Level"""
class Level():
    def __init__(self, stage_file='level_1'):
        self.level_data, self.rect = utils.load_image('{0}.png'.format(stage_file))
        self.ratio = 4 #ratio of pixel in stage file / pixel in game

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
                if self.level_data.get_at((x,y)) == self.colors["platform"]:
                    row.append(1)
                else:
                    row.append(0)
            self.data.append(row)


#return the enemies in the current scroll position (self.scrolled + self.ratio).
#only return enemies if self.scrolled%self.ratio == 0 (each pixel in the stage is one enemy, not self.ratio
    def platforms(self):
        platforms   = []
        for y in range(self.rect.height-1):
            pass

        return platforms
        


        
