# -*- coding: utf-8 -*-
"""
Keyboard Widget
"""
import pygame

import keyboard_mappings

class KeySprite(pygame.sprite.Sprite):
    """
    Key sprite that
    """
    
    def __init__(self, midi_id, pos, size):
        """
        midi_id = midi_id of the represented key
        pos = position
        size = size of the key

        """
        self.midi_id = midi_id
        self.pos = pos
        self.size = size
        #if key is black
        #self.image = 
        #self.image_active = 


class WhiteKeyGroup(pygame.sprite.Group):
    """
    """
    #TODO
    pass


class BlackKeyGroup(pygame.sprite.Sprite):
    """
    """
    #TODO
    pass


class KeyboardGroup(pygame.sprite.Group):
    """
    Piano keyboard 
    is a piano keyboard implementation where everything is computer generated
    """
    #TODO
    pass

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

        #Keyboard Image        
        self.image = pygame.image.load("assets/images/keyboard/plain_keyboard.png").convert_alpha()
        self.rect = self.image.get_rect() # use image extent values
        self.rect.topleft = pos
        
    def update(self):
        """
        """
        #print "updating keyboard sprite"
        super(KeyboardSprite, self).update()
        pass
        
    def collides_key(self, pos):
        """
        Calculates the key in the keyboard that is touched by the event position
        returns:
        midi_note (pygame event notation??? TODO decide)
        bounding box (x,y,w,h) of the element
        
        """
        #TODO
        #1 see if collides with the keyboard, else return false
        #2 if so, see what note (white) it collides, calculate also the rect containing the white note (this should be pre-calculated somewhere to make it faster)
        
        #3 if height < Ybk0 return true and note that it collides (midi notation) #Ybk0 == lower Y position of black key counted from the bottom
        
        #4 if heignt >Ybk0 see if it collides with which note (the flat or the sharp ...
        
        #5 return the nothe that it collides with, position, bounding box and midi notation
        
        pass
        
        
        

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
        self.kb_sprite = KeyboardSprite([0,400])
        self.add(self.kb_sprite)
        
        #Active Key Images (colors only)
        #TODO
        
        #Active Finger Images (numbers 1-5)
        #TODO
        
        #Arrows showing next key to press
        #TODO
    
    def update(self):
        super(Keyboard, self).update()
        
    def on_mouse_down(self, pos):
        """
        """
        pass
    
    def on_mouse_up(self, pos):
        """
        """
        pass
        
    #MIDI events
    #TODO on key on
    #TODO on key off

