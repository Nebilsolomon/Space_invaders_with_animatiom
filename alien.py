from ast import Or
from email.headerregistry import HeaderRegistry
from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from timer import Timer
from vector import Vector


class Alien(Sprite): 
    alien_images = [[pg.transform.rotozoom(pg.image.load(f'images/alien_03-{n}.png'), 0, 2) for n in range(2)],
                    [pg.transform.rotozoom(pg.image.load(f'images/alien__1{n}.png'), 0, 0.7) for n in range(2)],
                    [pg.transform.rotozoom(pg.image.load(f'images/alien__2{n}.png'), 0, 0.7) for n in range(2)]]

    aelist0 = [10, 10, 'blank']
    aelist1 = [20, 20, 'blank']
    aelist2 = [30, 30, 'blank']
    alien_explosion_images = [[pg.transform.rotozoom(pg.image.load(f'images/explosion_{el}.png'), 0, 1.5) for el in aelist2],
                              [pg.transform.rotozoom(pg.image.load(f'images/explosion_{el}.png'), 0, 1.5) for el in aelist1] ,
                              [pg.transform.rotozoom(pg.image.load(f'images/explosion_{el}.png'), 0, 1.5) for el in aelist0]]
 

    def __init__(self, game, type, alien_number):
        super().__init__()
        self.level = 0 
        self.v =  Vector(1,0)
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/alien0.bmp')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
       
        self.type = type
        self.sb = game.scoreboard
        self.dying = self.dead = False
        
        start_index = 0 if alien_number % 2 == 0 else 1
        self.timer_normal = Timer(Alien.alien_images[type], start_index=start_index, delay=300)
        self.timer_explosion = Timer(Alien.alien_explosion_images[type], delay=300, is_loop=False)
        self.timer = self.timer_normal                                    

    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)
    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion
          #  self.sb.increment_score()
    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed * settings.fleet_direction)
        self.rect.x = self.x

   


         

        




        self.draw()
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.centerx, rect.centery = self.rect.centerx, self.rect.centery
        self.screen.blit(image, rect)


#================================================================

class Aliens:
    def __init__(self, game): 
        self.model_alien = Alien(game=game, type=0, alien_number=0)
        self.game = game
        self.sb = game.scoreboard
        self.v =  Vector(1,0)
        self.aliens = Group()
        self.level = 0
        self.left_ship = 3
        self.sb.prep_ships(3)
      

        self.ship_lasers = game.ship_lasers.lasers    # a laser Group
        self.aliens_lasers = game.alien_lasers

        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.create_fleet()
       

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1 * alien_height))
        number_rows = 6
        return number_rows        

    def reset(self):
        # pass
        self.aliens.empty()
        self.create_fleet()
        self.aliens_lasers.reset()
       

    def create_alien(self, alien_number, row_number):
        type = row_number // 2
        alien = Alien(game=self.game, type=type, alien_number=alien_number)

        # alien = Alien(game=self.game, type=0)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number 
        self.aliens.add(alien)     

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                   self.create_alien(alien_number, row_number)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                    

                self.v.x *= -1
                for alien in self.aliens:
                    alien.v.x *= -1
                    alien.rect.y += (self.settings.fleet_drop_speed) * 10
                
                break

    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.level += 1
            self.sb.set_level(self.level)
            self.game.reset()
            self.settings.fleet_drop_speed += 2

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return
    
        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1


    def check_collisions(self):  
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)  
        if collisions:
            for alien in collisions:
                print("collisions:   alienns " )
                self.sb.increment_score(alien)
                print(alien.type)


                alien.hit()

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            print("collisions:   shipppp ") 
            self.left_ship -= 1
            self.sb.ships.empty()
            self.sb.set_left_ship(self.left_ship)
            self.sb.left_ship = self.left_ship
            self.sb.prep_ships(self.left_ship)
            self.sb.ships.draw(self.screen)
            self.ship.hit()

        # aliens_lasers collide with barrier?
        # ship_lasers collide with barrier?
        # aliens_lasers collide with ship_lasers ?


    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        for alien in self.aliens.sprites():
            if alien.dead:      # set True once the explosion animation has completed
                alien.remove()
            alien.update()
        self.aliens_lasers.update()

    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 
