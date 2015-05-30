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

class NoteSprite(pygame.sprite.Sprite):
    """
    """
    def __init__(self, parent_rect, size, pos, midi_id, tick_start, tick_end, midi_publish, synesthesia):
        """
        """
        super(NoteSprite, self).__init__()
        
        self.images = []
        
        #used to be able to know 
        #   if the note has to be removed from parent (when gets out of scope, to avoid using rendering resources)
        #   when the events note_on and note_off have to be launched (this is not the best timing method, but it might work for a demo)
        self.parent_rect = parent_rect
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
        self.image_off = pygame.Surface([self.rect.width, self.rect.height], pygame.HWSURFACE, 32)
        #replacement with subpixel library
        self.image_off.set_alpha(128)
        self.image_off.fill(self.synesthesia)
        self.subpixel_image_off = SubPixelSurface(self.image_off, 5, 5)
        
        self.image_on = pygame.Surface([self.rect.width, self.rect.height], pygame.HWSURFACE, 32)
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
        #update
        self.update=self.on_update
        
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
        
    def reset_pos(self):
        """
        resets the position to the original one
        """
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect.x = self.x
        self.rect.y = self.y
        #Subpixel calculations IMPORTANT
        self.image_on = self.subpixel_image_on.at(self.x, self.y)
        self.image_off = self.subpixel_image_off.at(self.x, self.y)
        #reset state 
        self.state = ButtonStates.passive
        self.on_note_off()
        
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
        
        #self.on_update()
        
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
        #self.on_update()
        
    def on_note_off(self):
        """
        """
        #TODO change brightness/color/etc for the note to show it has been released
        self.state = ButtonStates.passive
        self.image_index = 0
        #TODO WARNING, see how this should be updated ... not sure if here
        #self.on_update()

################################################################################

class AbstractDisplay(object):
    """
    """
    def __init__(self, screen, midi_pubsub, size, pos=(0,0), screen_time=10):
        """
        screen, 
        midi_pubsub, 
        background_image, already loaded pygame bakground image
        size, 
        pos=(0,0)
        screen_time=10  ##represents the time that the screen (height or width according to the display type)
                        ## i.e. it represents in play time (the time that a note will take to pass over the screen
        """    
        self.screen = screen
        self.pos = pos
        self.size = size
        
        self.midi_pubsub = midi_pubsub

        #self.background = pygame.transform.scale(background_image, size)
        #self.rect = self.background.get_rect() # use image extent values
        self.rect = pygame.rect.Rect((0,0), size)
        self.rect.topleft = pos
        
        self.notes_group = pygame.sprite.Group()
        # LayeredUpdates instead of group to draw in correct order
        self.allgroups = pygame.sprite.Group()
        
        #KeySprite.groups = self.allkeys, self.allgroups
        #NoteSprite.groups = self.allgroups, self.notes_group
        NoteSprite.groups = self.notes_group
        
        self.notes = []

        #Default
        self.screen_time = screen_time
        #Keep track of the play time
        self.current_time = 0
        #keep track of the displacement
        self.current_displacement = 0
        #timestamp of last update
        self.last_update = time.time()
        self.playing = False
        #updating, to avoid interruption of the function ... ??
        self.updating = False
                
    def play(self):
        """
        """
        #print "calling play"
        self.playing = True
        self.last_update = time.time()
                
    def pause(self):
        """
        """
        #print "calling pause"
        self.playing = False
        
    def stop(self):
        """
        """
        #print "calling stop"
        self.playing = False
        #recreate all notes buffer
        self.notes_group.empty()
        #add all the notes resetting their possitions
        for n in self.notes:
            self.notes_group.add(n)
            n.reset_pos()
        # set time to 0
        self.current_time = 0

    def step_forward(self, secs):
        """
        secs = seconds to go forward
        """
        #print "going forwards  %d secs" %secs
        self._update_notes(secs)
    
    def step_back(self, secs):
        """
        secs = seconds to go back
        """
        #TODO check if this algorithm can be made faster, for the moment recreates everything
        #print "going backwards  %d secs" %secs
        #reset display group, because there are keys that have been already erased from screen
        #now update positions
        #take current time
        curr_time = self.current_time
        #print 'curr_time = ',curr_time
        next_time = max(0,curr_time-secs)
        #clear all the notes from the group
        self.notes_group.empty()
        #add all the notes
        for n in self.notes:
            self.notes_group.add(n)
            n.reset_pos()
        #reset all positions and things
        self.current_time = 0
        #set new time to next_time
        self._update_notes(next_time)
        
    def on_end_playing(self):
        """
        """
        print "end playing"
        self.playing = False
        self.stop()
        #TODO send a signal to parent to tell the rest of the app that reproduction ended
        
        
    def _evaluate_midi_event(self, note_sprite):
        """
        when the events note_on and note_off have to be launched 
        (this is not the best timing method, but it might work for a demo)
        
        note_sprite: the note sprite to be evaluated
        """
        raise NotImplemented("_evalaute_midi_event not implemented, MUST subclass it")  


    def on_draw(self, screen):
        """
        """
        #print "drawing "
        #screen.blit(self.background, self.pos)
        #self.allgroups.clear(screen, self.background)
        self.allgroups.update()
        self.allgroups.draw(screen)

        #self.notes_group.clear(screen, self.background)
        self.notes_group.update()
        self.notes_group.draw(screen)
        
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

    def _get_note_displacement(self, delta_time):
        """
        calculates the displacement of the note corresponding to a delta time,
        this is abstract for every display to implement it's own
        """
        raise NotImplemented("_get_note_displacement not implemented, MUST subclass it")
        
    def _update_notes(self, extra_time=0):
        #calculate how much time was elapsed
        now = time.time()
        delta = now - self.last_update + extra_time
        self.last_update = now
        #calculate vertical movement
        displacement = self._get_note_displacement(delta)
        #check if end play
        notes = self.notes_group.sprites()
        if len(notes)<=0:
            self.on_end_playing()
            
        for n in notes:
            #print n, n.midi_id
            n.move(displacement)
            self._evaluate_midi_event(n)
            
        self.current_time += delta
        
    def on_update(self):
        """
        """
        if self.playing:
            self._update_notes()

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
        #print "publishing midi event: %s : %d" %(event_type, midi_id)
        self.midi_pubsub.publish(event_type, midi_id)
        pass
        
    def clean_all(self):
        """
        cleans all the notes in the current buffer
        """
        self.allgroups.empty()
        self.notes_group.empty()
        self.notes[:] = []
    
    def _calc_note_size(self, midi_id, sec_duration, note_map):
        """
        """
        raise NotImplemented("_calc_note_size not implemented, MUST subclass it")
        
    def _calc_note_pos(self, midi_id, sec_start, sec_duration, sec_end, note_map):
        """
        """
        raise NotImplemented("_calc_note_pos not implemented, MUST subclass it")
        
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
                    size = self._calc_note_size(midi_id, sec_duration, note_map)
                    pos = self._calc_note_pos(midi_id, size, sec_start, sec_duration, sec_end, note_map)
                    note = NoteSprite(self.rect, size, pos, midi_id, tick_start, tick_end, self.midi_publish, note_map['synesthesia'])
                    synesthesia = note_map['synesthesia']
                    #
                    self.notes.append(note)
                    self.notes_group.add(note)
                    #print "note ", midi_id, sec_duration, tick_duration, sec_start, tick_start, sec_end, tick_end, synesthesia, size, pos
                    #print "note ", midi_id, tick_start, tick_end, size, pos
        #TODO hide/erase loader overlay

################################################################################

class PlayerVerticalDisplay(AbstractDisplay):
    """
    display that shows a given file
    input format: MIDI
    TODO add annotations (for hand and 
    """
    def __init__(self, screen, midi_pubsub, size, pos=(0,0), screen_time=5):
        """
        """
        bkg = pygame.image.load("assets/images/displays/vertical_display_lines.png").convert_alpha()
        self.background = pygame.transform.scale(bkg, size)
        
        super(PlayerVerticalDisplay, self).__init__(screen, midi_pubsub, size, pos, screen_time)
                
    #def __verify_overlap(self):
    #    """
    #    function to find out a bug that makes some elements move faster than others up to one point
    #    this is SLOOOW
    #    This problem ws fixed with the subpixel library and was due to pygame doing differently 
    #    the sum when values are negative and when values are positive (rounding error I imagine)
    #    """
    #    
    #    for i in range(len(self.notes)-1):
    #        for j in range(i+1,len(self.notes)):
    #            n1 = self.notes[i]
    #            n2 = self.notes[j]
    #            if n1.rect.colliderect(n2.rect):
    #                print "collision detected at time: ", self.last_update
    #                print "n1:  ", n1.midi_id, n1.tick_start, n1.tick_end, n1.rect
    #                print "n:  ", n2.midi_id, n2.tick_start, n2.tick_end, n2.rect
                 
                 
    def _get_note_displacement(self, delta_time):
        """
        """
        vmove = self.size[1] * delta_time / self.screen_time
        return (0, vmove)

    def _calc_note_size(self, midi_id, sec_duration, note_map):
        """
        """
        height = self.size[1] * sec_duration / self.screen_time
        size = [note_map['size'][0], height]
        return size

    def _calc_note_pos(self, midi_id, size, sec_start, sec_duration, sec_end, note_map):
        """
        """
        height = size[1]
        #negative y position (above the display) 
        ypos = - (self.size[1] * sec_start / self.screen_time) - height + self.pos[1]
        #ypos = - (self.pos[1] * sec_start / self.screen_time) -height + self.pos[1]
        pos = (note_map['pos'][0], ypos)
        return pos

    def _evaluate_midi_event(self, note_sprite):
        """
        when the events note_on and note_off have to be launched 
        (this is not the best timing method, but it might work for a demo)
        when touches bottom
        """
        #print "evaluating note midi event"
        #TODO move this from hte notes to somewhere else, because this breaks portability and other things
        # .... a refactoring WILL BE NECESSARY!!
        #maybe see to pass this method as parameter in the note creation ?
        px,py,pw,ph = self.rect
        x,y,w,h = note_sprite.rect
        
        #check it went out of the screen (to the bottom)
        if y >(py+ph):
            # turn of midi if active
            if note_sprite.state == ButtonStates.pressed:
                note_sprite.on_note_release()
            #erase from all the display groups
            #self.remove(*self.groups)
            note_sprite.kill()
        #check turn midi_on
        elif note_sprite.state == ButtonStates.passive and (y+h)>(py+ph):
            note_sprite.on_note_press()

    def on_draw(self, screen):
        """
        """
        #print "drawing "
        screen.blit(self.background, self.pos)
        #self.allgroups.clear(screen, self.background)
        #self.allgroups.update()
        #self.allgroups.draw(screen)

        self.notes_group.clear(screen, self.background)
        self.notes_group.update()
        self.notes_group.draw(screen)
################################################################################

class VerticalDial(pygame.sprite.Sprite):
    """
    """
    def __init__(self, pos, size, ):
        """
        """
        #TODO
        pass


class PlayerHorizontalDisplay(AbstractDisplay):
    """
    display that shows a given file
    input format: MIDI
    TODO many things ...
        - hand annotations
        - finger annotations
        - other nice thingies
    """
    def __init__(self, screen, midi_pubsub, size, pos=(0,0), screen_time=15):
        """
        """
        bkg = pygame.image.load("assets/images/displays/horizontal_display_lines.png").convert_alpha()
        self.background = pygame.transform.scale(bkg, size)
        
        self.REF_HEIGHT = 400
        self.REF_WIDTH = 800
        self.REF_NUMBER_NOTES = 88
        
        #TODO take out all this hardcoded values fromo here, 
        #this are the dimensions of the vertical display and the calculations from keyboard mappings come from here        
        self.REF_HEIGHT_VERTICAL = 400
        self.REF_WIDTH_VERTICAL = 1040

        super(PlayerHorizontalDisplay, self).__init__(screen, midi_pubsub, size, pos, screen_time)
        
        self.overlay_group = pygame.sprite.Group()

        self.LEFT_OVERLAY_PROPORTION =  1./6
        self.RIGHT_OVERLAY_PROPORTION =  1./4 #2. / 6
        
        self._set_overlay()

    def _set_overlay(self):
        """
        sets overlay shadows for display references
        """
        #left overlay
        left_overlay_size = (self.size[0] * self.LEFT_OVERLAY_PROPORTION ,self.size[1])
        self.left_overlay = pygame.sprite.Sprite()
        self.left_overlay.image = pygame.Surface(left_overlay_size, pygame.HWSURFACE, 32)
        self.left_overlay.image.set_alpha(128)
        #self.left_overlay.image.fill((61,61,61))     # fill black
        self.left_overlay.image.fill((51,53,64))     # fill black
        #self.left_overlay.image.fill((250,250,250))     # fill white ->should make a white background behind the keys for the transparency to work well, but black behind it to fill the borders in black
        self.left_overlay.rect = self.left_overlay.image.get_rect()
        self.left_overlay.rect.x = self.pos[0]
        self.left_overlay.rect.y = self.pos[1]

        self.overlay_group.add(self.left_overlay)
        #right overlay
        right_overlay_size = (self.size[0] * self.RIGHT_OVERLAY_PROPORTION ,self.size[1])
        self.right_overlay = pygame.sprite.Sprite()
        self.right_overlay.image = pygame.Surface(right_overlay_size, pygame.HWSURFACE, 32)
        self.right_overlay.image.set_alpha(128)
        #self.right_overlay.image.fill((61,61,61))     # fill black
        self.right_overlay.image.fill((51,53,64))     # fill black
        #self.right_overlay.image.fill((250,250,250))     # fill white ->should make a white background behind the keys for the transparency to work well, but black behind it to fill the borders in black
        self.right_overlay.rect = self.right_overlay.image.get_rect()
        self.right_overlay.rect.x = self.pos[0] + self.size[0] - right_overlay_size[0]
        self.right_overlay.rect.y = self.pos[1]

        self.overlay_group.add(self.right_overlay)

        
    def _get_note_displacement(self, delta_time):
        """
        """
        hmove = - self.size[0] * delta_time / self.screen_time
        return (hmove, 0)

    def _calc_note_size(self, midi_id, sec_duration, note_map):
        """
        """
        width = self.size[0] * sec_duration / self.screen_time
        size = [width, self.size[1]/self.REF_NUMBER_NOTES] #TODO recalculate this
        return size

    def _calc_note_pos(self, midi_id, size, sec_start, sec_duration, sec_end, note_map):
        """
        """
        width = size[0]
        xpos = (self.size[0] * sec_start / self.screen_time) + (self.size[0] * (1-self.RIGHT_OVERLAY_PROPORTION))
        vpos = self.REF_HEIGHT * note_map['pos'][0] / self.REF_WIDTH_VERTICAL
        ypos = self.size[1] - vpos
        pos = (xpos, ypos)
        return pos

    def _evaluate_midi_event(self, note_sprite):
        """
        when the events note_on and note_off have to be launched 
        (this is not the best timing method, but it might work for a demo)
        when touches bottom
        """
        #print "evaluating note midi event"
        #TODO move this from hte notes to somewhere else, because this breaks portability and other things
        # .... a refactoring WILL BE NECESSARY!!
        #maybe see to pass this method as parameter in the note creation ?
        px,py,pw,ph = self.rect
        x,y,w,h = note_sprite.rect
        
        #check it went out of the screen (to the left)
        if x+w < 0:
            #erase from all the display groups
            #self.remove(*self.groups)
            note_sprite.kill()
        #check if should turn it off
        elif x+w < self.size[0] * self.LEFT_OVERLAY_PROPORTION:
            # turn of midi if active
            if note_sprite.state == ButtonStates.pressed:
                note_sprite.on_note_release()
        #check turn midi_on
        elif note_sprite.state == ButtonStates.passive and x < self.size[0] * self.LEFT_OVERLAY_PROPORTION:
            note_sprite.on_note_press()

    def update(self):
        """
        """
        #print "drawing "
        self.allgroups.update()
        self.notes_group.update()
        self.overlay_group.update()

    def on_draw(self, screen):
        """
        """
        #print "drawing "
        screen.blit(self.background, self.pos)
        #self.allgroups.clear(screen, self.background)
        #self.allgroups.update()
        #self.allgroups.draw(screen)

        self.notes_group.clear(screen, self.background)
        self.notes_group.update()
        self.notes_group.draw(screen)
        
        #self.overlay_group.clear(screen, self.background)
        self.overlay_group.update()
        self.overlay_group.draw(screen)


################################################################################

class PlayerDialDisplay(AbstractDisplay):
    """
    display that shows a given file
    input format: MIDI
    TODO many things ...
        - hand annotations
        - finger annotations
        - other nice thingies
    """
    def __init__(self, screen, midi_pubsub, size, pos=(0,0), screen_time=15):
        """
        """
        
        #load background
        sheet_background_colors.png
        bkg = pygame.image.load("assets/images/sheet/sheet_lines.png").convert_alpha()
        
        super(PlayerDialDisplay, self).__init__(screen, midi_pubsub, bkg, size, pos, screen_time, bkg)
        

################################################################################

class PlayerSheetDisplay(AbstractDisplay):
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


