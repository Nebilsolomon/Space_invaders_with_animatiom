import pygame as pg 
# import pygame.font
from pygame.sprite import Sprite, Group
from ship import Ship


import os

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.game = game
        self.ship_num = 0
       
        self.level = 0
        self.ships = Group()
  
       
     
        #self.level = self.game.ship.level
        

        self.high_score = 0
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

       # self.text_color = (30, 30, 30)
        self.text_color = (0, 255, 0)
        self.font = pg.font.SysFont(None, 48)
        
        if os.path.isfile('data.txt'):
         print("file is  exits")
        

        else:
            with open('data.txt', 'w') as f:
                    f.write(str(self.high_score)) 
        
        self.update_high_score()
       

        self.score_image = None 
        self.score_rect = None
        self.prep_score()
    def set_level(self, level):
        self.level = level
    
    def update_high_score(self):
        with open('data.txt', 'r') as f:
              
              self.high_score = int(f.read()) 
    
    

    def increment_score(self, alien): 
        if alien.type == 0:
            self.score += 30
        elif alien.type == 1:
            self.score += 20
        elif alien.type == 2:
            self.score += 10
        
        if self.score > self.high_score:
                self.high_score = self.score
                with open('data.txt', 'w') as f:
                    f.write(str(self.high_score)) 
        
        print(self.high_score , " hight score "  )



        self.prep_score()
    
    def ships_num_ship_left(self, ship_num):
        self.ship_num = ship_num
        
       
        


    

# =================================================================

    def prep_ships(self):
        #self.ships = Group()
        for ship_number in range(self.ship_num):
            ship = Ship(game= self.game) 
            ship.rect.x = 10 + ship_number * ship.rect.width 
            ship.rect.y = 10
            self.ships.add(ship)
            


#================================================================








    def prep_score(self): 

        score_str = str(self.score)
        self.score_image = self.font.render("Score = " + str(score_str), True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        # Display the hight score at the center  of the screen.

        high_score_str  = str(self.high_score)

        self.high_score_image = self.font.render("High Score = " + str(high_score_str), True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center 
        self.high_score_rect.top = 20

         # Display level  the screen.

        self.level_image = self.font.render("Level = " + str(self.level), True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()

        self.level_rect.right = self.screen_rect.right - 20

        self.level_rect.top = 50



    def reset(self): 
        self.score = 0
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.prep_ships()
        self.ships.draw(self.screen)