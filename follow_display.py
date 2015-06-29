# -*- coding: utf-8 -*-
"""
Follow display for piano follow game
2 hands, each finger has a number and the background of each finger gets 
iluminated for a certain time and with the corresponding color
this also sends the signal to the piano that iluminates the key and makes a sound
"""

import os
import pygame
from subpixel.subpixelsurface import SubPixelSurface

import time

from file_loader import ticks2sec

from button import *
#
import keyboard_mappings
import sheet_mappings
import synesthesia

from displays import *


class FollowDisplay(object):
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


        self.playing = False
        #updating, to avoid interruption of the function ... ??
        self.updating = False
        
        self._set_background()
        
    def on_event(self, event):
        """
        """
        #TODO
        pass
        
    def midi_publish(self, event_type, midi_id):
        """
        """
        #print "publishing midi event: %s : %d" %(event_type, midi_id)
        self.midi_pubsub.publish(event_type, midi_id)
        
    def clean_all(self):
        """
        cleans all the notes in the current buffer
        """
        pass
        
    def set_midi_info(self, midi_info):
        """
        """
        self.clean_all()
        #print "setting midi info"
        #
        self.midi_info = midi_info
        
        self.bpm,self.mpqn = self.midi_info.get_tempo()
        self.resolution = self.midi_info.get_resolution()

        #TODO 
        pass        
        
    def _set_background(self):
        """
        """
        #generic background,
        bkg_hands = pygame.image.load("assets/images/controls/hands_white_finger_numbers.png").convert_alpha()
        self.bkg_hands = pygame.transform.scale(bkg_hands, self.size)
        
    def _draw_background(self):
        """
        """
        #general background
        self.screen.blit(self.bkg_hands, self.pos)

    def _evaluate_midi_event(self):
        """
        """
        pass
        #TODO                

    def on_update(self):
        """
        """
        
        self.update()

    def update(self):
        """
        """
        #TODO
        pass 
               
    def on_draw(self, screen):
        """
        """
        #draw background
        self._draw_background()
        #TODO
        pass
                
