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

from file_loader import is_note_on, is_note_off
from file_loader import ticks2sec, ticks2ms
from file_loader import sec2ticks, ms2ticks

class FollowGameEngine(object):
    """
    """
    def __init__(self, midi_pubsub, drill=None, max_lives=3, difficulty=1, use_velocity=False, respect_tempo=False, ignore_note_off=True):
        """
        drill: the drill for the game engine to play
        max_lives=3, 
        difficulty=1, delta time tolerance (denominator) multiplication factor (not implemented yet)
        use_velocity=False, if velicity must be corrected or not (not implemented yet)
        respect_tempo=False, if time based correction must happen or not (not implemented yet)
        ignore_note_off=True, if note off events should also be corrected or not, default Ignore
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
        
        #
        self._ignore_note_off = ignore_note_off
        ############################
        #game state:
        ######
        #time state
        self._play_time = 0
        #self._begin_time = 0
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
        self._begin_time = 0
        self._begin_tick = 0
        self._current_tick = 0
        
        #list of AssociatedEvents that are being played and are waiting for note_off
        self._playing_events = []
        #list of events to play (buffer, will get empty)
        self._events2play = []
        #the reverted events2play (copied in new lists) for being able to correct the user as a queue
        #and without empty elements
        self._stage_events = []
        #array of arrays containig the events in order, this takes in account the delta tolerance
        # and is ordered in buckets
        self._follow_sequence = []
        #bucket index that points to the current progress on the drill
        self._bucket_index = 0
        
        #history of user input
        self._history = []
        #user current active notes
        self._user_notes_on = []
        #user_playing
        self._user_playing = True
        
        ############################
        #register function callbacks
        self.midi_pubsub.subscribe('note_on', self.on_note_on)
        self.midi_pubsub.subscribe('note_off', self.on_note_off)
        
    def set_drill(self, drill):
        """
        """
        self._drill = drill
        #drill.bucketize_midi_events(ignore_note_off=self._ignore_note_off)
        drill.bucketize_events()
        #self._buckets = drill.buckets()
        self._bucket_index = -1

    def toggle(self):
        """
        toggles game state between playing and stopped
        """
        if self._state == 'stopped':
            self.start()
        else:
            self.stop()
            
    def start(self):
        """
        
        """
        print "starting game"
        #TODO
        self._begin_time = time.time()
        self._begin_time
        self._state = 'showing'
        
        self._bucket_index = -1
        
        self._set_next_stage()
        
    def stop(self):
        """
        """
        print "stopping game"
        #TODO
        self._stop_time = time.time()
        self._state = 'stopped'
        pass
        
    def reset(self):
        """
        resets stats
        """
        #TODO send stop to all the elements
        self._current_lives = self._max_lives
        self._current_points = 0
        self._play_time = 0
        
        
    def _reset_stage(self):
        """
        first it will stop any playing note, then
        then resets all the stage variables
        """
        for ae in self._playing_events:
            note_off = ae.data[1]
            self.midi_pubsub.publish('note_off', note_off.pitch)

        self._playing = False
        #self._state = 'stopped' # ['stopped', 'showing', 'waiting']
        self._wait_timeout = 0
        self._current_timeout_left = 0
        self._total_timeout = 0 
        self._current_time = 0
        self._begin_time = time.time()
        self._begin_tick = self._drill._tick_begin
        self._current_tick = self._drill._tick_begin
        self._playing_events = []
        self._events2play = []
        self._stage_events = []
        self._follow_sequence = []
        
    def _set_next_stage(self):
        """
        sets the next stage to play:
        resets first the stage, to have a clean slate for the next one
        it will setup the set of elements to play,
        cleanup
        """
        self._reset_stage()
        #search next index with data and set the current bucket index
        i = self._bucket_index
        buckets = self._drill.buckets
        #print "buckets = ", buckets
        buckets_len = len(buckets)
        while True:
            i+=1
            if buckets_len>=i and len(buckets[i]) > 0 :
                self._bucket_index=i
                break
        if buckets_len>=i:
            print "Drill finished, no more to do"
            self.on_finish()
        #load all the buckets to play here
        #MUST make a copy of each internal array of the buckets or it will be erased later
        self._events2play = [b[:] for b in buckets[:self._bucket_index+1]]
        self._stage_events = [b[:] for b in buckets[:self._bucket_index+1] if len(b) > 0]
        self._stage_events.reverse()
        #?? set current max tick time
        #self._max_tick = (self._bucket_index+1) * self._drill._bucket_resolution
        #print "self._events2play = ", self._events2play
        # Try this .. 
        #self._state == 'showing'
        #self._begin_time = time.time()
        
    def on_finish(self):
        """
        Finishes the game
        """
        #TODO
        pass
        
    def on_win(self):
        """
        Congratulates the user
        Presents the user with the statistics
        Presents the chance to go on
        """
        #TODO
        pass
        
    def _on_stage_finish(self):
        """
        """
        self._set_next_stage()
        self._state = 'showing'
        self._begin_time = time.time()
        
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

    def _evaluate_event(self, event):
        """
        checks that the input event was an expected, 
        returns True if is correct, False if it is not
        """
        #TODO
        self._playing_events = []
        print "self._stage_events ", self._stage_events
        if len(self._stage_events):
            bucket = self._stage_events[-1]
            correct = False
            t_event = None
            for ae in bucket:
                print event
                #WARNING both types of events are different, left one is pygame and right one is an abstraction over python_midi
                #TODO FIXME those events should be the same type
                if event.data1 == ae.get_pitch():
                    t_event = ae
                    correct = True
                    break
            if t_event is not None:
                bucket.remove(t_event)
            #if mistake or bucket now is empty, pop and go to next bucket (this bucket failed already)
            if not correct or len(bucket) == 0:
                self._stage_events.pop()
            return correct
        #if len(self._stage_events) <= 0:
        #    print "sequence completed, congratulations!"
        #    #go to next stage
        #    self._on_stage_finish()
        
    def on_note_on(self, event):
        """
        """
        print "note on event = ", event
        #TODO
        #evaluate if the note is correct (WARNING this might get difficult with chords or parallel rythms)
        #if so, on note correct
        #else on mistake
        #append event to user history
        self._history.append(event) ##FIXME WARNING this event should be a python_midi event not a pygame event
        self._playing_events.append(event) ##FIXME WARNING this event should be a python_midi event not a pygame event
        evaluation = self._evaluate_event(event)
        print "evaluation = ", evaluation, event
        #correct

        
    def on_note_off(self, event):
        """
        """
        #Clear out the event from the playing events
        ev = None
        for e in self._playing_events:
            if event.data1 == e.data1:  ##FIXME WARNING this events should be python_midi events not a pygame event
                ev = e
        if ev is not None:
            self._playing_events.remove(ev)
        
        #TODO
        if len(self._stage_events) <= 0 and len(self._playing_events) <= 0:
            print "sequence completed, congratulations!"
            #go to next stage
            self._on_stage_finish()
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
        
    def _update_showing_state(self):
        """
        """
        #TODO
        #print "updating player"
        #increment time counter
        self._current_time = curr_time = time.time() - self._begin_time
        self._current_tick = curr_tick = sec2ticks(curr_time, self._drill.bpm, self._drill.resolution) + self._drill._tick_begin #(tick begin is because ticks are relative to this point)
        #print curr_time, curr_tick
        #See if any note has to be turned off
        buff_erase = [] #temp buffer because we can't erase elements from an iterator, it will break it
        for ae in self._playing_events:
            #print "playing events: ", self._playing_events
            enoff = ae.data[1] #note off
            if enoff.tick <= curr_tick:
                print "playing note off: ", enoff, curr_time, curr_tick
                self.midi_pubsub.publish('note_off', enoff.pitch, 0)
                buff_erase.append(ae)
            
        for e in buff_erase:
            self._playing_events.remove(e)
        #see if any note has to be turned on            
        for bucket in self._events2play:
            #print "events to play = ", bucket
            #TODO limit to the max current bucket, to do this use curr_time and curr_tick and bucket resolution (for performance on long drills)
            buff_erase = []
            for ae in bucket:
                #print "lala, ae", ae
                enon = ae.data[0] #note on
                #print enon, enon.tick

                if enon.tick <= curr_tick:
                    print "playing note on: ", enon, curr_time, curr_tick
                    self.midi_pubsub.publish('note_on', enon.pitch, enon.velocity)
                    #add to playing events
                    self._playing_events.append(ae)
                    #set for deletion in the current bucket
                    buff_erase.append(ae)
            for e in buff_erase:
                bucket.remove(e)
             
        #cleanup empty buckets
        self._events2play = [ b for b in self._events2play if len(b)>0]
        #when there are no more events to play, pass to another state
        if len(self._events2play) == 0 and len(self._playing_events) == 0:
            print "playing finished, now is your turn!"
            self._state = 'waiting'
        
    def update(self):
        """
        """
        #TODO
        if self._state == 'showing':
            self._update_showing_state()
        elif self._state == 'waiting':
            self._update_waiting_state()
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
        
        ############temp logic to see if playing works
        
        if self._state == 'waiting':
            self._set_next_stage()
            self._state = 'showing'
            self._begin_time = time.time()
        ##################
        pass
