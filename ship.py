import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Load the ship image and get its rect
        ship_asset = 'ship.png'
        self.image = pygame.image.load(ship_asset)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Stores a decimal value for the ship's center
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)


        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """Center the ship on the screen """
        
        self.centery = self.screen_rect.bottom - 21
        self.center = self.screen_rect.centerx
   
    def update(self):
        """Update the ship's position based on movement flags"""
        # update the shpi's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left >0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        #update the rect object from self.center
        self.rect.centerx = self.center
        self.rect.centery = self.centery

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

            
