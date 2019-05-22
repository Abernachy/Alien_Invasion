import pygame.font

class GameOver():
    """
    This class is for the game over button that appears when the user 
    runs out of lives
    This code is copied mostly from the button code and then mutated
    to my heart's desire

    Also I want this box clickable so the user can reset the game
    """
    def __init__(self, ai_settings, screen, gomsg):
        """ This initailizes the attributes n shit """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # This will be the dimensions of the object.  Looking to take up a chunk
        # of the screen
        self.width, self.height = 900, 450
        self.goprompt_color = (255, 255, 255)
        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None, 40)

        # Build the object and center it
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The message for the object, using a prep function
        self.prep_gomsg(gomsg)
        

    

    def prep_gomsg(self, gomsg):
        """Turns the msg object into an image and centers text on the object """
        self.gomsg_image= self.font.render(gomsg, True,self.text_color,self.goprompt_color)
        self.gomsg_image_rect = self.gomsg_image.get_rect()
        self.gomsg_image_rect.center = self.rect.center

    def draw_goscreen(self):
        # Draws the blank object then the message
        self.screen.fill(self.goprompt_color, self.rect)
        self.screen.blit(self.gomsg_image, self.gomsg_image_rect)