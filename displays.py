# -*- coding: utf-8 -*-
"""
Vertical display for an 88 key piano keyboard
"""

import os
import pygame
from subpixel.subpixelsurface import SubPixelSurface

import time



from file_loader import ticks2sec

from button import ButtonStates
#
import keyboard_mappings
import synesthesia
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


class Displacement(object):
    """
    Enum types of displacement
    the name indicates the axis and the direction
    """
    VERTICAL_DOWN = 'vertical_down'
    VERTICAL_UP = 'vertical_up'
    HORIZONTAL_LEFT = 'horizontal_down'
    HORIZONTAL_RIGHT = 'horizontal_right'

class NoteSprite(pygame.sprite.Sprite):
    """
    """
    def __init__(self, parent_rect, size, pos, midi_id, tick_start, tick_end, midi_publish, synesthesia, displacement=Displacement.VERTICAL_DOWN):
        """
        """
        super(NoteSprite, self).__init__()
        
        self.images = []
        
        #used to be able to know 
        #   if the note has to be removed from parent (when gets out of scope, to avoid using rendering resources)
        #   when the events note_on and note_off have to be launched (this is not the best timing method, but it might work for a demo)
        self.parent_rect = parent_rect
        #axis and direction of the displacement
        self.displacement = displacement
        #
        #note information ... maybe will be updated to include name and other informations as flat or sharp
        self.midi_id = midi_id
        self.key_id = midi_id  % 12
        self.octave = midi_id / 12
        self.pos = pos
        self.size = size
        self.tick_start = tick_start
        self.tick_end = tick_end
        #self.name = name
        self.synesthesia = synesthesia
        
        ####MIDI function that allows publishing midi events
        self.midi_publish = midi_publish
        
        self.x,self.y = pos
        w,h = size
        #if key is black
        self.rect = pygame.Rect([self.x,self.y,w,h])

        #create and append the pressed image with the same size as the background image
        self.image_off = pygame.Surface([self.rect.width, self.rect.height], pygame.HWSURFACE)
        #replacement with subpixel library
        self.image_off.set_alpha(128)
        self.image_off.fill(self.synesthesia)
        self.subpixel_image_off = SubPixelSurface(self.image_off, 5, 5)
        
        self.image_on = pygame.Surface([self.rect.width, self.rect.height], pygame.HWSURFACE)
        #self.image_off.set_alpha(255)
        self.image_on.fill(self.synesthesia)
        self.subpixel_image_on = SubPixelSurface(self.image_on , 5, 5)
        
        #append rest image        
        self.images.append(self.image_off)
        self.images.append(self.image_on)
        
        #current image index
        self.image_index = 0
                
        self.image = self.images[self.image_index]
        
        #note state
        self.state = ButtonStates.passive

    def _evaluate_visibility(self):
        """
        Check if the note has to be removed from parent 
        (when gets out of scope, to avoid using rendering resources)
        """
        pass
        
    def _evaluate_midi_event(self):
        """
        when the events note_on and note_off have to be launched 
        (this is not the best timing method, but it might work for a demo)
        when touches bottom
        """
        #TODO make this method generic for any kind of movement, 
        #for the moment will be only vertical movement
        px,py,pw,ph = self.parent_rect
        x,y,w,h = self.rect
        
        if self.displacement == Displacement.VERTICAL_DOWN:
            #check it went out of the screen (to the bottom)
            if y > (y)>(py+ph):
                # turn of midi if active
                if self.state == ButtonStates.pressed:
                    self.on_note_release()
                #erase from all the display groups
                self.remove(*self.groups)
            #check turn midi_on
            elif self.state == ButtonStates.passive and (y+h)>(py+ph):
                self.on_note_press()
        elif self.displacement == Displacement.VERTICAL_UP:
            #TODO
            pass
        elif self.displacement == Displacement.HORIZONTAL_LEFT:
            #TODO
            pass            
        elif self.displacement == Displacement.HORIZONTAL_RIGHT:
            #TODO
            pass
            
    def move(self, vector):
        """
        vector = (x,y) movement
        """
        self.x += vector[0]
        self.y += vector[1]
        self.rect.x = self.x
        self.rect.y = self.y
        #Subpixel calculations IMPORTANT
        #without this, the pygame renderer acts differently when coordinates are:
        #                    negative (negative_coord+1.x == negative_coord +2 )
        #                    positive (positive_coord+1.x == positive_coord +1 )
        #there is the need to make this better, also this library helps at easing
        #for all animations
        self.image_on = self.subpixel_image_on.at(self.x, self.y)
        self.image_off = self.subpixel_image_off.at(self.x, self.y)
        
        self._evaluate_visibility()
        self._evaluate_midi_event()
        
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
        #print "note collision check: ", self.rect, pygame.mouse.get_pos()
        #activate on key events
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.state == ButtonStates.passive and 1 in pygame.mouse.get_pressed():
                self.on_note_press()
            elif self.state == ButtonStates.pressed and  event.type == pygame.MOUSEBUTTONUP:
                self.on_note_release()
        elif self.state == ButtonStates.pressed:
            self.on_note_release()
        
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
        self.state = ButtonStates.pressed
        self.image_index = 1
        #TODO WARNING, see how this should be updated ... not sure if here
        self.on_update()
        
    def on_note_off(self):
        """
        """
        #TODO change brightness/color/etc for the note to show it has been released
        self.state = ButtonStates.passive
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
        
        self.notes = []
        #vertical time (from note appearing to note desapearing), in seconds (should be configurable)
        self.vtime = 5

        self.last_update = time.time()
        self.playing = False
        #updating, to avoid interruption of the function ... ??
        self.updating = False
                
    def play(self):
        self.playing = True
        self.last_update = time.time()
                
    def pause(self):
        self.playing = False
        
    def __verify_overlap(self):
        """
        function to find out a bug that makes some elements move faster than others up to one point
        this is SLOOOW
        This problem ws fixed with the subpixel library and was due to pygame doing differently 
        the sum when values are negative and when values are positive (rounding error I imagine)
        """
        
        for i in range(len(self.notes)-1):
            for j in range(i+1,len(self.notes)):
                n1 = self.notes[i]
                n2 = self.notes[j]
                if n1.rect.colliderect(n2.rect):
                    print "collision detected at time: ", self.last_update
                    print "n1:  ", n1.midi_id, n1.tick_start, n1.tick_end, n1.rect
                    print "n:  ", n2.midi_id, n2.tick_start, n2.tick_end, n2.rect
                    
    def on_update(self):
        """
        """
        #if False:
        if not self.updating:
            self.updating = True
            #calculate how much time was elapsed
            now = time.time()
            delta = now - self.last_update
            self.last_update = now
            #calculate vertical movement
            vmove = self.size[1] * delta / self.vtime
            #print "#############################"
            #print delta, vmove, len(self.notes)
            #for all notes, move them
            #for n in self.notes:
            for n in self.notes_group.sprites():
                #print n, n.midi_id
                n.move((0,vmove))
                #print "displacement:  ", n.midi_id, n.tick_start, n.tick_end, n.rect
            #print "#############################"
            self.updating = False
        
        #self.__verify_overlap()
        
    def on_draw(self, screen):
        """
        """
        #print "drawing "
        screen.blit(self.background, self.pos)
        self.allgroups.clear(screen, self.background)
        self.allgroups.update()
        self.allgroups.draw(screen)

        self.notes_group.clear(screen, self.background)
        self.notes_group.update()
        self.notes_group.draw(screen)

        pass
        
    def on_event(self, event):
        """
        """
        
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #TODO make this more efficient, for the moment is doing a loop on every note
            #should calculate which notes are better to call in an efficient way
            #for n in self.notes:
            for n in self.notes_group.sprites():
                n.on_event(event)
        #TODO make call to the right notes if the event is an input midi_event .. 
        pass

    def __find_note_in_mapping(self, midi_id, keyboard_map):
        """
        """
        for k in keyboard_map:
             if midi_id == k['midi_id']:
                return k
        return None
        
    def midi_publish(self, event_type, midi_id):
        """
        """
        #TODO
        print "publishing midi event: %s : %d" %(event_type, midi_id)
        pass
        
    def clean_all(self):
        """
        cleans all the notes in the current buffer
        """
        self.allgroups.empty()
        self.notes_group.empty()
        self.notes[:] = []
        
    def set_midi_info(self, midi_info, keyboard_map):
        """
        """
        self.clean_all()
        print "setting midi info"
        #
        self.midi_info = midi_info
        
        self.bpm,self.mpqn = self.midi_info.get_tempo()
        self.resolution = self.midi_info.get_resolution()

        #print "kb map", keyboard_map
        key_size = keyboard_map["key_size"]
        #TODO show loader overlay
        #now generate notes sprites
        for track in midi_info.tracks:
            for ae in track:
                #TEST
                #END TEST
                #get midi_id
                midi_id = ae.get_pitch()
                tick_duration = ae.get_duration()
                sec_duration = ticks2sec(tick_duration, self.bpm, self.resolution)
                tick_start = ae.get_init_tick()
                sec_start = ticks2sec(tick_start, self.bpm, self.resolution)
                tick_end = ae.get_end_tick()
                sec_end = ticks2sec(tick_end, self.bpm, self.resolution)
                #
                note_map = self.__find_note_in_mapping(midi_id, keyboard_map['keyboard_map'])
                #print "note found: ", note_map
                if note_map is not None:
                    height = self.size[1] * sec_duration / self.vtime
                    size = [note_map['size'][0], height]
                    #negative y position (above the display) 
                    ypos = - (self.size[1] * sec_start / self.vtime) - height + self.pos[1]
                    #ypos = - (self.pos[1] * sec_start / self.vtime) -height + self.pos[1]
                    pos = (note_map['pos'][0], ypos)
                    note = NoteSprite(self.rect, size, pos, midi_id, tick_start, tick_end, self.midi_publish, note_map['synesthesia'])
                    synesthesia = note_map['synesthesia']
                    #
                    self.notes.append(note)
                    self.notes_group.add(note)
                    #print "note ", midi_id, sec_duration, tick_duration, sec_start, tick_start, sec_end, tick_end, synesthesia, size, pos
                    #print "note ", midi_id, tick_start, tick_end, size, pos
        #TODO hide/erase loader overlay

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


