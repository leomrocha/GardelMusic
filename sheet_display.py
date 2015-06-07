# -*- coding: utf-8 -*-
"""
Sheet Display (complex) for piano music sheet
"""

import os
import pygame
from subpixel.subpixelsurface import SubPixelSurface

import time

from file_loader import ticks2sec

from button import *
#
import keyboard_mappings
import synesthesia

from displays import *

####
#TODO 
#   make all the dimensions dynamic and allow other piano configurations
#       for this should (use keyboard_mappings:
#import keyboard_mappings
#END todo
####

################################################################################
#constants  # already defined in displays.py commented here just for memory 
##########

#REF_NOTE_WIDTH_WHITE = 20
#REF_NOTE_WIDTH_BLACK = 15
#REF_SCREEN_WIDTH = 1040
#REF_SCREEN_HEIGHT = 400

#REF_NUMBER_KEYS = 88

class SheetLayer(object):
    """    
    """
    def __init__(self, screen, pos, size, notes, musical_key):
        """
        """
        pass



class PlayerSheetDisplay(object):
    """
    """
    def __init__(self, screen, midi_pubsub, size, pos=(0,0), screen_time=15):
        """
        screen, 
        midi_pubsub, 
        background_image, already loaded pygame bakground image
        size, 
        pos=(0,0)
        screen_time=10  ##represents the time that the screen (height or width according to the display type)
                        ## i.e. it represents in play time (the time that a note will take to pass over the screen
        """    
       #vars
        self.screen = screen
        self.midi_pubsub = midi_pubsub
        self.size = size
        self.pos = pos
        self.screen_time = screen_time
        #just to have nice overlay
        self.LEFT_OVERLAY_PROPORTION = 3./screen_time
        self.RIGHT_OVERLAY_PROPORTION = 4./screen_time
        
        self.rect = pygame.rect.Rect(pos, size)
        #sprite groups   
        self.notes_group = pygame.sprite.Group()
        #left and right hand groups
        self.lh_notes_group = pygame.sprite.Group()
        self.rh_notes_group = pygame.sprite.Group()
        #overlay
        self.overlay_group = pygame.sprite.Group()
        #moving dial
        self.dial_group = pygame.sprite.Group()
        #buttons groups
        #self.button_group = pygame.sprite.Group()
        
        self.notes = []
        self.lh_notes = []
        self.rh_notes = []
        
        self.notes_playing = []
        self.lh_notes_playing = []
        self.rh_notes_playing = []
        #self.notes_on_display = []
        
        self.lh_active = True #False  #
        self.rh_active = True #False  #
        #some constant calculations:
        #initial x_pos for dial and notes
        self.x0 = size[0] * self.LEFT_OVERLAY_PROPORTION
        #area where the 
        self.play_time = self.screen_time * (1 - self.LEFT_OVERLAY_PROPORTION - self.RIGHT_OVERLAY_PROPORTION)
        
        ## hand controls buttons
        bw = bh = int(self.LEFT_OVERLAY_PROPORTION / 4.)
        bsize = (bw, bh)
        
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
        
        self._set_background()
        
        self.dial = None
        self._set_dial()
        
        self._set_overlay()

    def on_lh_toggle(self, *args):
        """
        """
        self.lh_active = not self.lh_active
        
    def on_rh_toggle(self, *args):
        """
        """
        self.rh_active = not self.rh_active

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
        #turn off all notes
        for n in self.notes_playing:
            n.on_note_off()
        
        self.notes_playing = []
        #reset dial position
        self.dial.reset_pos()
        #print "calling stop"
        self.playing = False
        #recreate all notes buffer
        self.lh_notes_group.empty()
        self.rh_notes_group.empty()
        #add all the notes resetting their possitions

        if self.lh_active:
            for n in self.lh_notes:
                self.lh_notes_group.add(n)
                n.reset_pos()
        
        if self.rh_active:
            for n in self.rh_notes:
                self.rh_notes_group.add(n)
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
        self.lh_notes_group.empty()
        self.rh_notes_group.empty()
        #add all the notes resetting their possitions

        if self.lh_active:
            for n in self.lh_notes:
                self.lh_notes_group.add(n)
                n.reset_pos()
        
        if self.rh_active:
            for n in self.rh_notes:
                self.rh_notes_group.add(n)
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
        #TODO send signal to turn off every MIDI key that is still active
        
        
    def on_event(self, event):
        """
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #TODO make this more efficient, for the moment is doing a loop on every note
            #should calculate which notes are better to call in an efficient way
            if self.lh_active:
                for n in self.lh_notes_group.sprites():
                    n.on_event(event)
            if self.rh_active:
                for n in self.rh_notes_group.sprites():
                    n.on_event(event)
        #TODO make call to the right notes if the event is an input midi_event .. 

    def _update_notes(self, extra_time=0):
        #calculate how much time was elapsed
        now = time.time()
        delta = now - self.last_update + extra_time
        self.last_update = now
        #calculate vertical movement
        displacement = self._get_note_displacement(delta)
        #check if end play
        notes = []
        if self.lh_active:
            notes.extend(self.lh_notes_group.sprites())
        if self.rh_active:
            notes.extend(self.rh_notes_group.sprites())
            
        if len(notes)<=0:
            self.on_end_playing()
            
        for n in notes:
            #print n, n.midi_id
            n.move(displacement)
            self._evaluate_midi_event(n)
            
        self.current_time += delta
        
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
        #print "publishing midi event: %s : %d" %(event_type, midi_id)
        self.midi_pubsub.publish(event_type, midi_id)
        
    def clean_all(self):
        """
        cleans all the notes in the current buffer
        """
        #self.allgroups.empty()
        self.notes_group.empty()
        self.notes[:] = []
        
        self.lh_notes_group.empty()
        self.lh_notes[:] = []
        
        self.rh_notes_group.empty()
        self.rh_notes[:] = []

    def __set_midi_track(self, track, notes_list, notes_group, keyboard_map):
        """
        processes one track and sets the notes list and notes group
        """
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
                notes_list.append(note)
                notes_group.add(note)
                #print "note ", midi_id, sec_duration, tick_duration, sec_start, tick_start, sec_end, tick_end, synesthesia, size, pos
                #print "note ", midi_id, tick_start, tick_end, size, pos

    def set_midi_info(self, midi_info, keyboard_map):
        """
        """
        self.clean_all()
        #print "setting midi info"
        #
        self.midi_info = midi_info
        
        self.bpm,self.mpqn = self.midi_info.get_tempo()
        self.resolution = self.midi_info.get_resolution()

        #print "kb map", keyboard_map
        key_size = keyboard_map["key_size"]
        #TODO show loader overlay
        #now generate notes sprites
        ##TODO left and right hands
        if len(midi_info.tracks) >= 1:
            #set right track
            rt = midi_info.tracks[0]
            if self.rh_active:
                self.__set_midi_track(rt, self.rh_notes, self.rh_notes_group, keyboard_map)
        if len(midi_info.tracks) >= 2:
            #left track
            lt = midi_info.tracks[1]
            if self.lh_active:
                self.__set_midi_track(lt, self.lh_notes, self.lh_notes_group, keyboard_map)
        #for the moment discards all other track        
        
        #TODO hide/erase loader overlay
    def _set_dial(self):
        """
        """
        pos = (self.pos[0] + self.size[0] * self.LEFT_OVERLAY_PROPORTION, self.pos[1])
        size = (2,self.size[1])
        self.dial = DialSprite(pos=pos, size=size)
        self.dial_group.add(self.dial)        
        
    def _set_background(self):
        """
        """
        #generic background,
        self.bkg_white = pygame.Surface([self.size[0], self.size[1]], pygame.HWSURFACE, 32)
        #replacement with subpixel library
        self.bkg_white.fill((250,250,240))
        bkg_colors = pygame.image.load("assets/images/sheet/sheet_background_colors.png").convert_alpha()
        self.bkg_colors = pygame.transform.scale(bkg_colors, self.size)
        bkg_lines = pygame.image.load("assets/images/sheet/sheet_lines.png").convert_alpha()
        self.bkg_lines = pygame.transform.scale(bkg_lines, self.size)
        #hand specific background
        self._set_lh_background()
        self._set_rh_background()
    
    def _set_lh_background(self):
        #replacement with subpixel library
        f_clef = pygame.image.load("assets/images/sheet/sheet_f_clef_lines.png").convert_alpha()
        self.bkg_f_clef = pygame.transform.scale(f_clef, self.size)

    def _set_rh_background(self):
        #replacement with subpixel library
        g_clef = pygame.image.load("assets/images/sheet/sheet_g_clef_lines.png").convert_alpha()
        self.bkg_g_clef = pygame.transform.scale(g_clef, self.size)

        
    def _draw_background(self):
        """
        """
        #general background
        self.screen.blit(self.bkg_white, self.pos)
        self.screen.blit(self.bkg_colors, self.pos)
        self.screen.blit(self.bkg_lines, self.pos)
        #hand specific backgorund
        if self.lh_active:
            self.screen.blit(self.bkg_f_clef, self.pos)
        if self.rh_active:
            self.screen.blit(self.bkg_g_clef, self.pos)

    def _evaluate_midi_event(self):
        """
        """
        notes = self.lh_notes_group.sprites()
        notes.extend(self.rh_notes_group.sprites())
        #check midi playing end
        midi_end = False
        if len(notes)<=0:
            midi_end = True
        #TODO improve this hack because it's ugly and unefficient
        elif len(self.notes_playing) <= 0:
            #print "no notes playing"
            lhnl = len([n for n in self.lh_notes_group if ((n.x + n.size[0]) > self.dial.x)])
            rhnl = len([n for n in self.rh_notes_group if ((n.x + n.size[0]) > self.dial.x)])
            if lhnl <= 0 and rhnl <=0:
                #print "no more notes ", lhnl, rhnl 
                midi_end = True
        if midi_end:
            #print "midi file end"
            self.on_end_playing()
        #turn off notes
        for n in self.notes_playing:
            if not pygame.sprite.collide_rect(self.dial, n):
                n.on_note_off()
                self.notes_playing.remove(n)
        #turn on notes
        for n in notes:
            if n not in self.notes_playing:
                #TODO add condition to avoid comparing with notes beyond the screen.
                #print n, n.midi_id
                if pygame.sprite.collide_rect(self.dial, n):
                    n.on_note_on()
                    self.notes_playing.append(n)
                

    def _get_dial_displacement(self, delta_time):
        """
        """
        hmove = self.size[0] * delta_time / self.screen_time
        return (hmove, 0)
        
    def _update_dial(self, extra_time=0):
        """
        """
        #print "updating dial"
        #calculate how much time was elapsed
        now = time.time()
        delta = now - self.last_update + extra_time
        self.last_update = now
        #calculate vertical movement
        displacement = self._get_dial_displacement(delta)
        self.dial.move(displacement)
        #verify dial positionm:
        #  if dial got over right overlay, reset position
        if self.dial.x >= self.size[0] * (1-self.RIGHT_OVERLAY_PROPORTION):
            self.dial.reset_pos()
            #update notes positions:
            n_displ = - self.size[0] * (1 - self.LEFT_OVERLAY_PROPORTION - self.RIGHT_OVERLAY_PROPORTION)
            #notes = self.notes_group.sprites()
            notes = self.lh_notes_group.sprites()
            notes.extend(self.rh_notes_group.sprites())
            #if len(notes)<=0:
            #    self.on_end_playing()
            for n in notes:
                #print n, n.midi_id
                n.move((n_displ,0))
        #verify dial inter
        self.current_time += delta
        self._evaluate_midi_event()

    def on_update(self):
        """
        """
        
        self.update()
        if self.playing:
            self._update_dial()

    def update(self):
        """
        """
        
        #self.notes_group.update()
        self.lh_notes_group.update()
        self.rh_notes_group.update()
        
        self.overlay_group.update()
        self.dial_group.update()
        
        #self.button_group.update()
        
    def on_draw(self, screen):
        """
        """
        #draw background
        self._draw_background()

        #self.notes_group.clear(screen, self.bkg_white)
        #self.notes_group.update()
        #self.notes_group.draw(screen)

        #self.lh_notes_group.clear(screen, self.bkg_white)
        self.lh_notes_group.update()
        self.lh_notes_group.draw(screen)

        #self.rh_notes_group.clear(screen, self.bkg_white)
        self.rh_notes_group.update()
        self.rh_notes_group.draw(screen)

        self.overlay_group.update()
        self.overlay_group.draw(screen)

        self.dial_group.update()
        self.dial_group.draw(screen)
        
        #self.button_group.update()
        #self.button_group.draw(screen)
        
    def _calc_note_size(self, midi_id, sec_duration, note_map):
        """
        """
        width = self.size[0] * sec_duration / self.screen_time
        h_mult = 1
        if keyboard_mappings.get_key_color(midi_id) == "black":
            h_mult = 0.8
        #TODO take out this hardcoded 28 and make it dynamic somehow for different backgrounds
        height = h_mult * self.size[1]/ 28
        size = [width,  height] 
        return size

    def _calc_note_pos(self, midi_id, size, sec_start, sec_duration, sec_end, note_map):
        """
        """
        #TODO TODO TODO all this method
        xpos = (self.size[0] * sec_start / self.screen_time) + self.x0 
        k_height = 2 * self.size[1]/REF_NUMBER_KEYS
        
        #center_y = self.size[1] - ( (midi_id - 21) * self.size[1] / REF_NUMBER_KEYS )
        #center_y = self.pos[1] + self.size[1] -( (midi_id - 21) * self.size[1] / REF_NUMBER_KEYS )
        #TODO warning take out the hardcoded 21
        center_y =  ( (midi_id - 21) * self.size[1] / REF_NUMBER_KEYS )
        vpos = center_y - k_height / 2.
        ypos = self.size[1] - vpos + self.pos[1]
        pos = (xpos, ypos)
        return pos
