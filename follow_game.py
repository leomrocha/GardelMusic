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
    def __init__(self, midi_pubsub, drill=None, max_lives=3, difficulty=1, use_velocity=False, respect_tempo=False):
        """
        drill: the drill for the game engine to play
        max_lives=3, 
        difficulty=1, delta time tolerance (denominator) multiplication factor (not implemented yet)
        use_velocity=False, if velicity must be corrected or not (not implemented yet)
        respect_tempo=False, if time based correction must happen or not (not implemented yet)
        """
        ############################
        #pubsub for user interaction and music playing
        self.midi_pubsub = midi_pubsub
        #drill that will be presented to the player
        self._drill = None
        self.set_drill(drill)
        
        #multiplication factor for the delta tolerance on time issues
        #self._difficulty = difficulty  #TODO
        #self._user_velocity = use_velocity  #TODO
        #self._respect_time = respect_time  #TODO
        
        ############################
        #game stats
        self._max_lives = max_lives
        self._current_lives = max_lives
        self._current_points = 0
        
        
        ############################
        #game state:
        ######
        #time state
        self._play_time = 0
        self._start_time = 0
        self._stop_time = 0
        #playing ?
        self._playing = False
        #the state represents what the user or game are doing
        self._state = 'stopped' # ['stopped', 'showing', 'waiting']
        #wait timeout is the time the game will wait without user input
        self._wait_timeout = 0
        self._current_timeout_left = 0
        #total timeout is the max time for the particular sub-drill (the sequence to follow at the moment)
        # this time is the total time the user has to fulfill the current 
        self._total_timeout = 0 
        self._current_time = 0
        
        #array of arrays containig the events in order, this takes in account the delta tolerance
        self._follow_sequence = []
        #current notes to be played
        self._current_notes = []
        
        #history of user input
        self._history = []
        
        
        ############################
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
        
    def on_win(self):
        """
        Congratulates the user
        Presents the user with the statistics
        Presents the chance to go on
        """
        #TODO
        pass
        
    def on_lose(self):
        """
        Pity the user
        Present the user the statistics
        Present the user the chance to redo the level
        """
        #TODO
        pass
        
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
        
    def _update_waiting_state(self):
        """
        """
        #TODO
        #increment time counter
        #decrement from timeout left
        #if timeout:
        #lose life
        #pass to showing state
        #return
        pass
        
    def _showing_state(self):
        """
        """
        #TODO
        #increment time counter
        #increment pointer
        #if a sound has to be started
        #    send midi signal
        #   push to stack of notes active (track for any stop case)
        #if a sound has to be stopped, send midi signal
        
    def update(self):
        """
        """
        #TODO
        pass
        
    def draw(self, screen=None):
        """
        """
        #TODO
        pass
        
    def on_event(self, event):
        """
        """
        #TODO
        pass
