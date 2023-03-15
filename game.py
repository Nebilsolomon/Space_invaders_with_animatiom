import pygame as pg
from settings import Settings
from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from barrier import Barriers
from mystery import Mystery
import sys 


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.play_num = 2

       


       


        size = self.settings.screen_width, self.settings.screen_height   # tuple
    
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")
        self.level = 3


        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)  

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.mystery = Mystery(game = self)

       

        self.settings.initialize_speed_settings()

        





#============================================================================
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.state = "start"

        self.font_large = pg.font.Font(None, 60)
        self.font = pg.font.Font(None, 36)

        
        self.title_text = self.font_large.render("SPACE INVADERS", True, self.green)
        
        self.image1 = pg.image.load("images/alien_03-0.png")
        self.image1 = pg.transform.scale(self.image1, (100, 100))
        self.label = self.font.render("= 30", True, self.green)

        self.image2 = pg.image.load("images/alien__10.png")
        self.image2 = pg.transform.scale(self.image2, (100, 100))
        self.label2 = self.font.render("= 20", True, self.green)

        self.image3 = pg.image.load("images/alien__20.png")
        self.image3 = pg.transform.scale(self.image3, (100, 100))
        self.label3 = self.font.render("= 10", True, self.green)

        self.image4 = pg.image.load("images/mystery.png")
        self.image4 = pg.transform.scale(self.image4, (100, 100))
        self.label4 = self.font.render("= 100", True, self.green)

        self.button_width = 200
        self.button_height = 50


#===========  NEw Code for Button =================================================================

        self.button_color = pg.Color("blue")
        self.button_hover_color = pg.Color("red")
        self.button_rect = pg.Rect(500, 650, 150,  100)
        self.button_text = pg.font.SysFont(None, 30).render(" PLAY ", True, self.green)
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)


     
        
    #================================================================++++++++
        #self.button_x = self.settings.screen_width / 2 - self.button_width / 2
        #self.button_y =(self.settings.screen_height - 50)  - self.button_height / 2
        #self.button_text = self.font_large.render("PLAY", True, self.green)
        #self.button_text_x = self.button_x + self.button_width / 2 - self.button_text.get_width() / 2
        #self.button_text_y = self.button_y + self.button_height / 2  - self.button_text.get_height() / 2
    
#================================================================++++++++



    def draw(self):
        self.screen.fill(self.black)

        self.screen.blit(self.image1, (500, 150))
        self.screen.blit(self.label , (640, 180))
         
        self.screen.blit(self.image2, (500, 270))
        self.screen.blit(self.label2 , (640, 310))
        
        self.screen.blit(self.image3, (500, 380))
        self.screen.blit(self.label3 , (640, 420))

        self.screen.blit(self.image4, (500, 490))
        self.screen.blit(self.label4 , (640, 520))



        self.screen.blit(self.title_text,(400, 20) )

        pg.draw.rect(self.screen, self.button_color, self.button_rect)
        self.screen.blit(self.button_text, self.button_text_rect)





       # pg.draw.rect(self.screen, self.black, (self.button_x, self.button_y, self.button_width, self.button_height))
        #self.screen.blit(self.button_text, (self.button_text_x, self.button_text_y))






#============================================================================











    

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT: self.game_over()

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Check if user clicked on PLAY button
                if self.button_rect.x < event.pos[0] <self.button_rect.x + self.button_rect.width and self.button_rect.y < event.pos[1] < self.button_rect.y + self.button_rect.height:
                    self.state = "play"
                  #  self.game.sound.play_bg()
        
   
           
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()




        if self.button_rect.collidepoint(pg.mouse.get_pos()):
            self.button_color = self.button_hover_color
        else:
            self.button_color = pg.Color("blue")




    def reset(self):
        print('Resetting game...')
        
        # self.lasers.reset()    # handled by ship for ship_lasers and by aliens for alien_lasers
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.scoreboard.reset()
    
    def restart(self):
          
        pg.init()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.button_color = pg.Color("blue")
        self.button_hover_color = pg.Color("red")
        self.button_rect = pg.Rect(500, 650, 150,  100)
        self.button_text = pg.font.SysFont(None, 30).render(" PLAY AGAIN ", True, self.green)
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)
        
        pg.draw.rect(self.screen, self.button_color, self.button_rect)
        self.screen.blit(self.button_text, self.button_text_rect)

        pg.display.update()
        self.screen.fill(self.settings.bg_color)
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Check if user clicked on PLAY button
                if self.button_rect.x < event.pos[0] <self.button_rect.x + self.button_rect.width and self.button_rect.y < event.pos[1] < self.button_rect.y + self.button_rect.height:
                    self.play_num = 1
                else:
                    self.play_num = 2


                




     
        

        
        

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        #self.restart()
       
        pg.quit()
        sys.exit()
       

    def play(self):
        #self.sound.play_bg()
        while True:     
            self.handle_events() 

            #self.screen.fill(self.black)
            if self.state  == "start":
                
                self.sound.play_bg()
              
                self.screen.blit(self.label, (300, 50))
                self.draw()
                #pg.draw.rect(self.screen, self.green, (self.button_x, self.button_y, self.button_width, self.button_height))
                pg.display.update()

                
               # self.screen.blit(self.button_text, (self.button_text_x, self.button_text_y))
            elif self.state == "play":
            # Add your game code here
                

                pg.display.update()









                
                self.screen.fill(self.settings.bg_color)
                
                self.ship.update()
                self.aliens.update()
                self.barriers.update()
                # self.lasers.update()    # handled by ship for ship_lasers and by alien for alien_lasers
                self.scoreboard.update()
                self.mystery.update()
                pg.display.flip()


def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
