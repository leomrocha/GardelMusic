
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
        
