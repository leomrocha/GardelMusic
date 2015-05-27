# -*- encoding: utf-8 -*-

"""
This is a basic play scene where there are 2 parts:
The display, where the music is shown
The instrument, that shows what is happening and/or what should be happening with the instrument
"""

import pygame
from keyboard import *
from displays import *

from button import Button

from file_loader import MidiInfo


class PlayScene(object):
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
        self.instrument = Keyboard(self.screen, midi_pubsub=self.midi_pubsub, pos=(0, self.h-300), width=self.w)
        
        self.player_display = PlayerVerticalDisplay(self.screen, size=(int(1040 * self.w /1060. ), self.h -400), pos=(0, 100))
        #self.instrument_group = pygame.sprite.Group()
        #self.instrument_group.add(self.instrument)
        #TEST        
        #self.keysprite = KeySprite(midi_id=56, pos=(1200,200) , size=(40,200), color='white', synesthesia=(255,100,100))
        #self.instrument_group.add(self.keysprite)
        self.play_button = Button(
                        self.screen, 
                        on_press_callback=self.on_play_button_press,
                        on_hover_callback=self.on_play_button_hover,
                        on_release_callback=self.on_play_button_release,
                        size=(75,75), 
                        pos=(self.w * 3 / 4 - 25, 10),
                        image_passive=os.path.join("assets","images","icons","ic_play_circle_big_normal_o.png"),
                        image_hover=os.path.join("assets","images","icons","ic_play_circle_normal_o.png"),
                        image_active=os.path.join("assets","images","icons","ic_play_circle_pressed_o.png"),
                        )
        
        self.dirty = True
        
    def on_play_button_press(self):
        #print "button press called"
        self.dirty = True
        
    def on_play_button_hover(self):
        #print "button hover called"
        self.dirty = True
        
    def on_play_button_release(self):
        #print "button release called"
        #
        #TEST - this is AWFUL
        fname = "../../tests_midi/python-midi/mary.mid"
        self.level_info = MidiInfo(fname)
        
        keyboard_map = self.instrument.keyboard_map
        self.player_display.set_midi_info(self.level_info, keyboard_map)
        self.dirty = True
        self.player_display.play()
        #END TEST
        pass
        
	
    def on_update(self):
        """
        """
        self.midi_pubsub.poll()
        self.instrument.on_draw(self.screen)

        #TEST
        self.player_display.on_update()
        self.play_button.on_update()
        
    def on_event(self, event):
        """
        """
        self.play_button.on_event(event)
        #self.keysprite.on_event(event)
        self.instrument.on_event(event)
        self.player_display.on_event(event)
        #self.dirty = True
        pass

    def on_draw(self, screen=None):
        """
        """
        if not screen:
            screen = self.screen

        self._draw_display()

        if self.dirty:
            self._draw_background()
            self._draw_instrument()
            self._draw_scoreboard()
            self._draw_menu()
            self.play_button.dirty = True
            self.play_button.on_draw(screen)
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
            - the one for the user to read:
                - left hand display
                - right hand display
            - the one that shows the user feedback of what is he/she doing
        """
        self.player_display.on_draw(self.screen)
        pass
        
    def _draw_instrument(self):
        """
        Instrument, one of the most important elements (piano keyboard for example)
        """
        self.instrument.on_draw(self.screen)
        
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

