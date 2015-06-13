# -*- encoding: utf-8 -*-

"""
Play Scene
This is a basic play scene where there are 2 parts:
The display, where the music is shown
The instrument, that shows what is happening and/or what should be happening with the instrument
"""

import pygame
from keyboard import *
from displays import *
from sheet_display import *
import controls

from button import Button

from file_loader import MidiInfo


import keyboard_mappings

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
        kb_height = keyboard_mappings.get_height(self.w)
        self.instrument = Keyboard(self.screen, midi_pubsub=self.midi_pubsub, pos=(0, self.h-kb_height), width=self.w)
        
        #pd_height = self.h - kb_height - 75
        pd_height = self.h - kb_height - 10
        #self.player_display = PlayerVerticalDisplay(self.screen, self.midi_pubsub, size=(int(1040 * self.w /1060.), pd_height), pos=(10, 75))
        #self.player_display = PlayerVerticalDisplay(self.screen, self.midi_pubsub, size=(self.w, pd_height), pos=(0, 10))
        pd_height = self.h - kb_height - 75
        #horizontal same distribution as piano keys
        #self.player_display = PlayerHorizontalDisplay(self.screen, self.midi_pubsub, size=(self.w, pd_height), pos=(0, 75))
        #horizontal proportional
        #self.player_display = PlayerDialDisplay(self.screen, self.midi_pubsub, size=(self.w, pd_height), pos=(0, 75))
        #horizontal sheet music
        self.player_display = PlayerSheetDisplay(self.screen, self.midi_pubsub, size=(self.w, pd_height), pos=(0, 75))
        #self.instrument_group = pygame.sprite.Group()
        #self.instrument_group.add(self.instrument)
        #TEST        
        #self.keysprite = KeySprite(midi_id=56, pos=(1200,200) , size=(40,200), color='white', synesthesia=(255,100,100))
        #self.instrument_group.add(self.keysprite)
        self.playback_controls = controls.PlaybackControlBar(screen=self.screen,
                                                            pos=(self.w - 220 , 10),
                                                            size=(200,50),
                                                            on_backwards_callback=self.on_backwards,
                                                            on_play_toggle_callback=self.on_play_toggle, 
                                                            on_stop_callback=self.on_stop,
                                                            on_forward_callback=self.on_forward
                                                            )
        '''
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
        '''
        self.hand_select_controls = controls.HandsControlBar(screen=self.screen,
                                                            pos=(self.w - 340 , 10),
                                                            size=(100,50),
                                                            on_left_hand_callback=self.player_display.on_lh_toggle,
                                                            on_right_hand_callback=self.player_display.on_rh_toggle, 
                                                            )
        self.dirty = True
        
        ###test file names:
        fname = "assets/midi/yiruma-river_flows_in_you.mid"
        #fname="assets/midi/mary.mid"
        #load midi, this is a test, should be done somehow by the parent
        self.load_midi(fname)
        
    def on_backwards(self):
        """
        """
        #print "going backwards"
        self.player_display.step_back(1)
        
    def on_play_toggle(self):
        """
        """
        if self.player_display.playing:
            self.player_display.pause()
        else:
            self.player_display.play()
        
    def on_stop(self):
        """
        """
        self.player_display.stop()
        
    def on_forward(self):
        """
        """
        #print "going forward"
        self.player_display.step_forward(1)

    def load_midi(self, fname="assets/midi/mary.mid"):
        #print "button release called"
        #
        #TEST - this is AWFUL
        
        #fname = "assets/midi/yiruma-river_flows_in_you.mid"
        self.level_info = MidiInfo(fname)
        
        keyboard_map = self.instrument.keyboard_map
        self.player_display.set_midi_info(self.level_info, keyboard_map)
        
	
    def on_update(self):
        """
        """
        self.midi_pubsub.poll()
        self.instrument.on_draw(self.screen)

        #TEST
        self.player_display.on_update()
        self.playback_controls.on_update()
        self.hand_select_controls.on_update()
        
    def on_event(self, event):
        """
        """
        self.instrument.on_event(event)
        self.player_display.on_event(event)
        self.playback_controls.on_event(event)
        self.hand_select_controls.on_event(event)
        #self.dirty = True
        pass

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
            self.playback_controls.dirty = True
            self.playback_controls.on_draw(screen)
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
        self.playback_controls.on_draw(self.screen)
        self.hand_select_controls.on_draw(self.screen)

