"""
Keyboard Widget
"""
import pygame


class KeyboardSprite(pygame.sprite.Sprite):
    """
    Piano Keyboard Sprite
    """
    def __init__(self, pos=(0,0)):
        """
        """
        #Super constructor
        #super().__init__()
        super(KeyboardSprite, self).__init__()
        #pygame.sprite.Sprite.__init__(self)
        #
        
        #self.kb = pygame.sprite.Sprite()
        self.image = pygame.image.load("assets/images/keyboard/plain_keyboard.png").convert_alpha()
        self.rect = self.image.get_rect() # use image extent values
        self.rect.topleft = pos
        
    def update(self):
        """
        """
        #print "updating keyboard sprite"
        super(KeyboardSprite, self).update()
        pass
        
    #TODO on mouse down
    #TODO on mouse up
    #TODO on key down
    #TODO on key up
    #MIDI events
    #TODO on key on
    #TODO on key off


class Keyboard(pygame.sprite.Group):
    """
    """
    def __init__(self, pos=(0,0)):
        """
        """
        #Super constructor
        #super().__init__()
        super(Keyboard, self).__init__()
        #pygame.sprite.Sprite.__init__(self)
        #
        self.kb_sprite = KeyboardSprite([0,450])
        self.add(self.kb_sprite)
    
    def update(self):
        super(Keyboard, self).update()

