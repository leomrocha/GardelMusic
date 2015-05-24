# -*- coding: utf-8 -*-
"""
Keyboard Widget
"""
import os
import pygame

import keyboard_mappings


#make this global so they don't load many times (has o
black_key_image = None
white_key_image = None



class KeySprite(pygame.sprite.DirtySprite):
    """
    Key sprite that
    """
    def __init__(self, midi_id, pos, size, color, synesthesia=(100,100,100)):
        """
        midi_id = midi_id of the represented key
        pos = position
        size = size of the key
        color = [white|black]
        synesthesia = the color that the key takes when activated. By default a shade of grey
        
        """
        #WARNING AWFUL
        #this is here to load for the first time the images as the display MUST be initialized
        try:
            if black_key_image is None or white_key_image is None:
                black_key_image = pygame.image.load(os.path.join("assets","images","keyboard","black_key.png")).convert_alpha()
                white_key_image = pygame.image.load(os.path.join("assets","images","keyboard","white_key.png")).convert_alpha()
        except:
            black_key_image = pygame.image.load(os.path.join("assets","images","keyboard","black_key.png")).convert_alpha()
            white_key_image = pygame.image.load(os.path.join("assets","images","keyboard","white_key.png")).convert_alpha()
        ##END awful
        
        super(KeySprite, self).__init__()
        
        self.images = []
        
        self.midi_id = midi_id
        self.key_id = midi_id  % 12
        self.octave = midi_id / 12
        self.key_color = color
        self.pos = pos
        self.size = size
        self.synesthesia = synesthesia
        #TODO make this efficient (for the moment will load a copy o the image for every key)
        #if key is black
        if color == 'black':
            self.image = black_key_image = pygame.transform.scale(black_key_image, size)
        else:
            self.image = white_key_image = pygame.transform.scale(white_key_image, size)
        
        #append rest image        
        self.images.append(self.image)
        
        #current image index
        self.image_index = 0
        
        self.rect = pygame.Rect(self.image.get_rect())
        print self.rect, self.rect.width, self.rect.height
        #create and append the pressed image with the same size as the background image
        pressed_image = pygame.Surface((self.rect.width, self.rect.height))
        pressed_image.fill(self.synesthesia)
        
        self.images.append(pressed_image)
        
        #update key position
        self.x = pos[0]
        self.y = pos[1]
        
        #key state ('rest' | 'pressed')
        self.state = 'rest'
        
    def on_key_press(self):
        """
        when the key is pressed by the user on the screen
        """
        #TODO emit note on midi event
        self.on_note_on()
        
    def on_key_release(self):
        """
        when the key is pressed by the user on the screen
        """
        #TODO emit note off midi event
        self.on_note_off()
        
    def on_note_on(self, finger=0):
        """
        Key activation
        """
        #draw the colored overlay
        
        #if finger >=1 && <=5 also overlay the finger id on the key
        self.state = 'pressed'
        self.image_index = 1
        
    def on_note_off(self):
        """
        """
        #TODO erase all the overlay
        #TODO reset to the original image
        self.state = 'rest'
        self.image_index = 0

    def on_update(self):
        """
        """
        self.image = self.images[self.image_index]
        pass
        
    def on_event(self, event=None):
        """
        """
        pass
        
    def on_draw(self):
        """
        """
        pass
        

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

