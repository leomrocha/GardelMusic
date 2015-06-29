# -*- encoding: utf-8 -*-

"""
Follow Scene
This is a basic Follow game like scene where there are 2 parts:
The display, where the hand and color sequence is shown
The instrument, that shows what is happening and/or what should be happening with the instrument
"""

import pygame
from keyboard import *
from displays import *
from follow_display import *
from file_loader import MidiInfo



class FollowScene(object):
    """
    """

    def __init__(self, director, midi_pubsub):
        self.director = director
        self.screen = director.screen
        self.w, self.h = director.screen.get_size()
        
        self.midi_pubsub = midi_pubsub
        self.dirty = True
        
        self.setup_scene()
        
    def setup_scene(self):
        """
        sets ups the scene (scoreboard, instrument, displays, menus, etc
        """
        #TODO make something more dynamic, for the moment only shows the hardcoded keyboard
        #self.instrument = KeyboardSprite()
        kb_height = keyboard_mappings.get_height(self.w)
        self.instrument = Keyboard(self.screen, midi_pubsub=self.midi_pubsub, pos=(0, self.h-kb_height), width=self.w)
        
        fd_height = self.h - kb_height - 75
        #horizontal sheet music
        self.follow_display = FollowDisplay(self.screen, self.midi_pubsub, size=(self.w, fd_height), pos=(0, 75))

        self.dirty = True
        
        ###test file names:
        #fname = "assets/midi/yiruma-river_flows_in_you.mid"
        fname="assets/midi/mary.mid"
        #load midi, this is a test, should be done somehow by the parent
        self.load_midi(fname)
        

    def load_midi(self, fname="assets/midi/mary.mid"):
        #print "button release called"
        #
        #TEST - this is AWFUL
        
        #fname = "assets/midi/yiruma-river_flows_in_you.mid"
        self.level_info = MidiInfo(fname)
        
        keyboard_map = self.instrument.keyboard_map
        self.follow_display.set_midi_info(self.level_info)
        
	
    def on_update(self):
        """
        """
        self.midi_pubsub.poll()
        self.instrument.on_draw(self.screen)

        #TEST
        self.follow_display.on_update()
        
    def on_event(self, event):
        """
        """
        self.instrument.on_event(event)
        self.follow_display.on_event(event)

    def on_draw(self, screen=None):
        """
        """
        if not screen:
            screen = self.screen
        #if True:
        
        if self.dirty:
            self._draw_background()
            #self._draw_display()
            #self._draw_instrument()
            #self._draw_scoreboard()
            #self._draw_menu()
            self.dirty = False

        self._draw_display()
        self._draw_instrument()
        self._draw_scoreboard()
        self._draw_menu()

    def _draw_background(self):
        """
        Scene background
        """
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((250, 250, 240))
        #self.screen.fill((50, 50, 50))
        self.screen.blit(background, (0, 0))


    def _draw_display(self):
        """
        Music display, this are 2 overlayed displays:
            - the one for the user to read:
                - left hand display
                - right hand display
            - the one that shows the user feedback of what is he/she doing
        """
        self.follow_display.on_draw(self.screen)
        
    def _draw_instrument(self):
        """
        Instrument, one of the most important elements (piano keyboard for example)
        """
        self.instrument.on_draw(self.screen)
        
    def _draw_scoreboard(self):
        """
        Scoreboard for the user to know his/her status
        """
        pass
        
    def _draw_menu(self):
        """
        Menu (go back, pause, stop, volume and so on)
        """
        pass

