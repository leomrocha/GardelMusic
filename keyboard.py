
import pygame


class Keyboard(pygame.sprite.Sprite):
    """
    Piano Keyboard
    """
    def __init__(self):
        """
        """
        #Sprite constructor
        #super().__init__()
        #
        #Load Keyboard images
        self.background = pygame.image.load("assets/images/keyboard/keyboard_background.png").convert()
        self.white_keys = pygame.image.load("assets/images/keyboard/keyboard_white-keys.png").convert() 
        self.black_keys = pygame.image.load("assets/images/keyboard/keyboard_black-keys.png").convert() 
        self.color_bar = pygame.image.load("assets/images/keyboard/keyboard_color-bar.png").convert()
        #when color bar will be separated for white and black keys
        #color_bar_wk = 
        #color_bar_bk = 
        
        self.rect = self.background.get_rect()
