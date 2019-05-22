import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from game_over import GameOver
from button import Button



""" CHECK EVENT FUNCTIONS"""

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # Moves the ship to the right
        ship.moving_right = True
    elif event.key ==pygame.K_LEFT:
        ship.moving_left = True
    elif event.key ==pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
           

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key==pygame.K_DOWN:
        ship.moving_down = False
        

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats,sb,  play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks the fucking button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Reset the game settings
        ai_settings.initialize_dynamic_settings()
        # hide the mouse cursor
        pygame.mouse.set_visible(False)
        
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Resets the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # set the game over flag to 0
        ai_settings.game_over_flag = 0

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


"""UPDATE SCREEN FUNCTIONS"""
            
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, gameover):
    """Update images on the screen and flip to the new screen """
    # redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    # Redraw the bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active and ai_settings.game_over_flag == 0:
        play_button.draw_button()
    elif not stats.game_active and ai_settings.game_over_flag >= 1:
        game_over(ai_settings, screen, stats, sb, ship, aliens, bullets)
    

    # Make the most recently drawn screen visible
    pygame.display.flip()

"""BULLET RELATED FUNCTIONS """

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """update the position of bullets and get rid of old bullets"""
    #update bullet positions
    bullets.update()
    
    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,stats, sb, ship,aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions """
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score +=ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)


    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level +=1
        if stats.level >= 10:
            ai_settings.game_over_flag = 2
            stats.game_active = False
            game_over(ai_settings,screen,stats,sb,ship,aliens,bullets)
            pygame.mouse.set_visible (True)
        
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

   
def fire_bullet(ai_settings,screen,ship,bullets):
    """Fire a bullet if limit not reached yet"""
    # Creates the bullet and adds it to the bullet's group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

"""ALIEN AND FLEET RELATED FUNCTIONS"""

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change their direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *=-1

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, gameover):
    """
    Check if thefleet is at an edge and updates the positions of all aliens
    """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, gameover)
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row """
    available_space_x = ai_settings.screen_width -2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height -(3*alien_height)- ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
            

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row """
    
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2* alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen,ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Create the first frow of aliens
    for row_number in range(number_rows):    
        for alien_number in range(number_aliens_x):
        # create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

"""Collision/hitting functions {self and edges}"""

def check_aliens_bottom( ai_settings,screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, gameoverscreen)
            break


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, gameover):
    """Respond to ship being hit by aliens """
    if stats.ships_left > 0:
        # decrement ships left
        stats.ships_left -=1

        # Update scoreboard
        sb.prep_ships()

    else:
        # Sets gmae over flag to 1 for user losing the game
        # (by the way you, just lost the game)
        ai_settings.game_over_flag = 1
        stats.game_active = False
        game_over(ai_settings,screen,stats,sb,ship,aliens,bullets)
        pygame.mouse.set_visible (True)
        
        

    # empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    #create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship() 

    # pause
    sleep(0.5)

def game_over(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Sets up the game over screens for the player """
    """1 for losing the game, 2 for winning the game, default is 0"""
    if ai_settings.game_over_flag ==1:
        gameoverscreen = GameOver(ai_settings, screen,
            "You and your friends are dead, Game Over. Click to restart")
        gameoverscreen.draw_goscreen()
    elif ai_settings.game_over_flag ==2:
        gameoverscreen = GameOver(ai_settings, screen,
        "Congraturations, you have won.  Go get a Dairy Queen")
        gameoverscreen.draw_goscreen()




def check_high_score(stats,sb):
    """Check to see if there's a new high score """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()



          
