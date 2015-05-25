# -*- encoding: utf-8 -*-

"""
This is a basic play scene where there are 2 parts:
The display, where the music is shown
The instrument, that shows what is happening and/or what should be happening with the instrument
"""

import pygame
from keyboard import *

class PlayScene(object):
    """
    """

    def __init__(self, director):
        self.director = director
        self.screen = director.screen
        self.w, self.h = director.screen.get_size()
        
        self.dirty = True
        
        self.setup_scene()
        
    def setup_scene(self):
        """
        sets ups the scene (scoreboard, instrument, displays, menus, etc
        """
        #TODO make something more dynamic, for the moment only shows the hardcoded keyboard
        #self.instrument = KeyboardSprite()
        self.instrument = Keyboard(self.screen, pos=(0, self.h-250), width=self.w)
        
        #self.instrument_group = pygame.sprite.Group()
        #self.instrument_group.add(self.instrument)
        #TEST        
        #self.keysprite = KeySprite(midi_id=56, pos=(1200,200) , size=(40,200), color='white', synesthesia=(255,100,100))
        #self.instrument_group.add(self.keysprite)
        pass
	
    def on_update(self):
        """
        """
        self.instrument.on_draw(self.screen)
        pass
        
    def on_event(self, event):
        """
        """
        
        #self.keysprite.on_event(event)
        self.instrument.on_event(event)
        #self.dirty = True
        pass

    def on_draw(self, screen=None):
        """
        """
        if not screen:
            screen = self.screen
        if self.dirty:
            self._draw_background()
            self._draw_display()
            self._draw_instrument()
            self._draw_scoreboard()
            self._draw_menu()
            self.dirty = False
        
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
            - the one for the user to read
            - the one that shows the user feedback of what is he/she doing
        """
        pass
        
    def _draw_instrument(self):
        """
        Instrument, one of the most important elements (piano keyboard for example)
        """
        #self.instrument_group.draw(self.screen)
        
        pass
        
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

