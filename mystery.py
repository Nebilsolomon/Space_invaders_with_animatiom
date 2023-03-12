

import pygame as pg
from pygame.sprite import Sprite
from laser import Lasers
from vector import Vector
from sys import exit
from timer import  Timer
from utils import Util


class Mystery(Sprite):  # TODO -- change to use YOUR OWN IMAGE for the ship AND its explosion
    ship_images = [pg.transform.rotozoom(pg.image.load(f'images/mystery.png'), 0, 1.0)]
    ship_hit_images = [pg.transform.rotozoom(pg.image.load(f'images/ship_fields{n}.png'), 0, 1.0) for n in range(9)]
    ship_explosion_images = [pg.transform.rotozoom(pg.image.load(f'images/ship_explode{n}.png'), 0, 1.0) for n in range(6)]

    def __init__(self, game):
        super().__init__()
       
        self.game = game
        self.move_left = True
        self.scoreboard = game.scoreboard
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
      # posn is the centerx, bottom of the rect, not left, top
        self.v = Vector()


        self.timer_normal = Timer(image_list=Mystery.ship_images)
        self.timer = self.timer_normal    

 
    
 






     




    def update(self):
      
        self.draw()


    def draw(self): 
        #image = self.timer.image()        
        #rect = image.get_rect()
        #rect.left += self.rect.left
        #rect.top += self.rect.top
        


        #rect.left, rect.top = self.rect.left, self.rect.top
                                             # MODIFICATION for SHIP's SHIELDS
       # self.screen.blit(image, rect)
        #self.screen.blit(self.image, self.rect)

    #    self.v += Vector(1, 0)
     #   if self.v.x < 800:
      #     self.v -= Vector(-1, 0)
       
        if self.move_left:
              print("first")
              self.rect.x += 5
              if self.rect.x > 1600:
                   print(self.rect.x)
                   self.move_left = False
        
        else:
             print("second")
             self.rect.x -= 5
             if self.rect.x <= -1600:
                   print(self.rect.x)
                   self.move_left = True


              

       # if self.rect.x < 800:
        #    self.v += Vector(3, 0)
         #   self.rect.x = self.v.x
        #else:  
         #   self.v -= Vector(2, 0)
          #  self.rect.x = self.v.x


        
          #      self.rect.x += 5

        #   _a: Vector(-1, 0)
         #           pg.K_d: Vector(1, 0),
        
        
        # Render the ship at its new location
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
