# -*- coding: utf-8 -*-
"""
Vertical display for an 88 key piano keyboard
"""

import os
import pygame

####
#TODO 
#   make all the dimensions dynamic and allow other piano configurations
#       for this should (use keyboard_mappings:
#import keyboard_mappings
#END todo
####

################################################################################
#constants
##########

REF_NOTE_WIDTH_WHITE = 20
REF_NOTE_WIDTH_BLACK = 15
#REF_SCREEN_WIDTH = 1060
REF_SCREEN_WIDTH = 1040
REF_SCREEN_HEIGHT = 400

REF_NUMBER_KEYS = 88


################################################################################


class NoteSprite(pygame.sprite.Sprite):
    """
    """
    def __init__(self, size, pos, midi_id, midi_publish, synesthesia):
        """
        """
        super(NoteSprite, self).__init__()
        
        self.images = []
        
        self.midi_id = midi_id
        self.key_id = midi_id  % 12
        self.octave = midi_id / 12
        self.pos = pos
        self.size = size
        #self.name = name
        self.synesthesia = synesthesia
        
        ####MIDI function that allows publishing midi events
        self.midi_publish = midi_publish
        
        #if key is black
        self.rect = pygame.Rect(size)
        #create and append the pressed image with the same size as the background image
        self.image_off = pygame.Surface([self.rect.width, self.rect.height], pygame.HWSURFACE)
        self.image_off.set_alpha(128)
        self.image_off.fill(self.synesthesia)
        
        self.image_on = pygame.Surface([self.rect.width, self.rect.height], pygame.HWSURFACE)
        #self.image_off.set_alpha(255)
        self.image_on.fill(self.synesthesia)
        
        #append rest image        
        self.images.append(self.image_off)
        self.images.append(self.image_on)
        
        #current image index
        self.image_index = 0
        
        
    def on_draw(self, scene):
        """
        """
        pass

    def on_update(self):
        """
        """
        #print "calling on_update", self.image_index
        self.image = self.images[self.image_index]
        
        
    def on_event(self, event=None):
        """
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #print "mouse over"
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print "mouse button pressed"
                self.on_key_press()
            if event.type == pygame.MOUSEBUTTONUP:
                #print "mouse button released"
                self.on_key_release()
                
        elif self.image_index != 0:
            self.on_key_release()
        
        self.on_update()
        
        
        
    def on_note_press(self):
        """
        when the note is pressed by the user on the screen
        """
        #TODO emit note on midi event
        self.midi_publish("note_on", self.midi_id)
        self.on_note_on()
        
    def on_note_release(self):
        """
        when the note is released by the user on the screen
        """
        self.midi_publish("note_off", self.midi_id)
        self.on_note_off()
        
    def on_note_on(self):
        """
        Key activation
        """
        #TODO change brightness/color/etc for the note to show it has been pressed
        
        #if finger >=1 && <=5 also overlay the finger id on the key
        self.state = 'pressed'
        self.image_index = 1
        #TODO WARNING, see how this should be updated ... not sure if here
        self.on_update()
        
    def on_note_off(self):
        """
        """
        #TODO change brightness/color/etc for the note to show it has been released
        self.state = 'rest'
        self.image_index = 0
        #TODO WARNING, see how this should be updated ... not sure if here
        self.on_update()

################################################################################

class PlayerVerticalDisplay(object):
    """
    display that shows a given file
    input format: MIDI
    TODO add annotations (for hand and 
    """
    def __init__(self, screen, size, pos=(0,0)):
        """
        """
        self.screen = screen
        self.pos = pos
        self.size = size
        
        #Bak=ckground Image        
        bkg = pygame.image.load("assets/images/displays/vertical_display_lines.png").convert_alpha()
        
        self.background = pygame.transform.scale(bkg, size)
        self.rect = self.background.get_rect() # use image extent values
        self.rect.topleft = pos
        
        self.notes_group = pygame.sprite.Group()
        # LayeredUpdates instead of group to draw in correct order
        self.allgroups = pygame.sprite.Group()
        
        #KeySprite.groups = self.allkeys, self.allgroups
        NoteSprite.groups = self.allgroups, self.notes_group
        
        
                
    def on_update(self):
        """
        """
        pass
    
    def on_draw(self, screen):
        """
        """
        screen.blit(self.background, self.pos)
        pass
        
    def on_event(self, event):
        """
        """
        pass

################################################################################
class PlayerHorizontalDisplay(object):
    """
    display that shows a given file
    input format: MIDI
    TODO add annotations (for hand and 
    """
    def __init__(self, screen, pos, size):
        """
        """
        pass
        
    def on_update(self):
        """
        """
        pass
    
    def on_draw(self, scene):
        """
        """
        pass
        
    def on_event(self, event):
        """
        """
        pass


################################################################################

class PlayerSheetDisplay(object):
    """
    display that shows a given file
    input format: MIDI
    TODO add annotations (for hand and 
    """
    def __init__(self, screen, pos, size):
        """
        """
        pass
        
    def on_update(self):
        """
        """
        pass
    
    def on_draw(self, scene):
        """
        """
        pass
        
    def on_event(self, event):
        """
        """
        pass


