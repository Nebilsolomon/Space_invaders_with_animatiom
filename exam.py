import pygame as pg
import sys 

class Game:
    def __init__(self):
        pg.init()
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)

        size = (400, 300)
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption("Button Example")
        #self.screen.fill(self.white)


       
      
   
        #================================================

        self.button_color = pg.Color("blue")
        self.button_hover_color = pg.Color("red")
        self.button_rect = pg.Rect(150, 100, 100, 50)
        self.button_text = pg.font.SysFont(None, 30).render("Play", True, self.green)
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)
        #================================================

        
    
    def play(self):
        
        while True:
    # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN and self.button_rect.collidepoint(event.pos):
                    self.button_color = self.button_hover_color

            # Clear the screen
            self.screen.fill(pg.Color("white"))
                  
            pg.draw.rect(self.screen, self.button_color, self.button_rect)
            self.screen.blit(self.button_text, self.button_text_rect)

            # Check if the mouse is over the button
            if self.button_rect.collidepoint(pg.mouse.get_pos()):
                self.button_color = self.button_hover_color
            else:
                self.button_color = pg.Color("blue")

            # Update the display
            pg.display.update()








    









def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()



