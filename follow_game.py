# -*- coding: utf-8 -*-
"""
Follow Game Engine

This engine handles the follow game, it will be able to track the progress of the user
This engine does not contain any graphic element, it only will follow the user entries and
present the user with the elements to follow
"""

import os
import pygame

import time


class FollowGameEngine(object):
    """
    """
    def __init__(self, midi_pubsub, drill=None, max_lives=3):
        """
        drill: the drill for the game engine to play
        """
        #pubsub for user interaction and music playing
        self.midi_pubsub = midi_pubsub
        #drill that will be presented to the player
        self._drill = drill
        
        #game stats
        self._max_lives = max_lives
        self._current_lives = max_lives
        self._current_points = 0
        self._play_time = 0
        self._start_time = 0
        self._stop_time = 0
        
        #game state:
        
        self._playing = False
        self.
        #register function callbacks
        self.midi_pubsub.subscribe('note_on', self.on_note_on)
        #self.midi_pubsub.subscribe('note_off', self.on_note_off)
        
    def set_drill(self, drill):
        """
        """
        self._drill = drill
        
    def start(self):
        """
        
        """
        #TODO
        self._start_time = time.time()
        #TODO start with the drill
        pass
        
    def stop(self):
        """
        """
        #TODO
        self._stop_time = time.time()
        pass
        
    def reset(self):
        """
        resets stats
        """
        self._current_lives = self._max_lives
        self._current_points = 0
        self._play_time = 0
        
    def on_mistake(self, event, expected):
        """
        Called when there is a mistake
        event: is the event that arrived
        expected: is the expected status 
        """
        #TODO mark the mistake ... somehow 
        #TODO discount life  
        #if life not ended:
        #   repeat up to this same point
        #else:
        #   end exercise and present results
        pass
        
    def on_correct_event(event, expected):
        """
        """
        #TODO
        pass
        
    def on_note_on(self, event):
        """
        """
        #TODO
        #evaluate if the note is correct (WARNING this might get difficult with chords or parallel rythms)
        #if so, on note correct
        #else on mistake
        #
        pass
        
    def on_note_off(self, event):
        """
        """
        #TODO
        pass
        
    
