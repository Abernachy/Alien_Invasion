
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from game_over import GameOver as gameover

def run_game():
    # Initialize pygame, settings, and screen object
        pygame.init()
        ai_settings = Settings()
        screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Make a FUCKING FUCKING BUTTON BUTTSEX
        play_button = Button(ai_settings, screen, "Click for not Projared penis")
        
        # Create an instance to store game statistics and create a scoreboard
        stats = GameStats(ai_settings)
        sb = Scoreboard(ai_settings, screen, stats)

        # Make a ship, group of bullets, and a group of aliens
        ship = Ship(ai_settings,screen) 
        bullets = Group()
        aliens = Group()

        # create a fleet of fucking aliens
        gf.create_fleet(ai_settings, screen, ship, aliens)

        
            



    #Starts the main loop for the game
        while True:
                gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

                if stats.game_active:
                    ship.update()
                    gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,bullets)
                    gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, gameover)
                    
                gf.update_screen(ai_settings,screen,stats, sb, ship, aliens, 
                    bullets, play_button, gameover)

            


              
run_game()

            
    
