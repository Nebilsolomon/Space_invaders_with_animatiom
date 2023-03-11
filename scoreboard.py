import pygame as pg 
# import pygame.font
import os

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 0
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

    def prep_score(self): 

        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        # Display the hight score at the center  of the screen.

        high_score_str  = str(self.high_score)

        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center 
        self.high_score_rect.top = 20



    def reset(self): 
        self.score = 0
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)