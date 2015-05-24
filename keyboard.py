
import pygame


class Keyboard(pygame.sprite.Group):
    """
    Piano Keyboard
    """
    def __init__(self):
        """
        """
        #Super constructor
        #super().__init__()
        #
        xpos = 0
        ypos = 0
        
        self.kb = pygame.sprite.Sprite()
        self.kb.image = pygame.image.load("assets/images/keyboard/plain_keyboard.png").convert_alpha()
        self.kb.rect = self.kb.image.get_rect() # use image extent values
        self.kb.rect.topleft = [xpos, ypos]
        
        self.add(self.kb)        
        self.draw()
        
        '''
        #taken out for a simpler approach for a demo, will only be done with an image with a Surface
        #Load Keyboard images
        self.background = 
        self.white_keys = 
        self.black_keys = 
        self.color_bar = 
        
        self.img_background = pygame.image.load("assets/images/keyboard/keyboard_background.png").convert_alpha()
        self.img_white_keys = pygame.image.load("assets/images/keyboard/keyboard_white-keys.png").convert_alpha() 
        self.img_black_keys = pygame.image.load("assets/images/keyboard/keyboard_black-keys.png").convert_alpha() 
        self.img_color_bar = pygame.image.load("assets/images/keyboard/keyboard_color-bar.png").convert_alpha()
        #when color bar will be separated for white and black keys
        #color_bar_wk = 
        #color_bar_bk = 
        
        self.
        #END taken out for a simpler approach for a demo, will only be done with an image with a Surface
        '''
