# -*- coding: utf-8 -*-
"""
MIDI recorder.
Records a sequence of MIDI events.
Mainly cares about note_on and note_off events, the others might be registered or not.
Meta information has to be provided by the user of the API

"""

import os
import pygame

import time

#from file_loader import is_note_on, is_note_off
#from file_loader import ticks2sec, ticks2ms
#from file_loader import sec2ticks, ms2ticks
#from file_loader import SongMetaInfo # for meta information on the song
#from file_loader import MidiInfo  # for associating events after the recording ... needed ??

from file_loader import *
from midi_connection import pygame_event2python_midi


class SimpleMIDIRecorder(object):
    """
    This simple midi recorder creates a single track recording of note_on and note_off
    events, nothing else.
    """
    def __init__(self, midi_pubsub, bpm=60, resolution=220):
        """
        midi_pubsub: the midi pubsub object
        """
        self.midi_pubsub = midi_pubsub
        
        self._meta = SongMetaInfo()
        self.bpm = bpm  #TODO unduplicate it. This information is in the SongMetaInfo (or should be)
        self.resolution = resolution



        #current state
        self._recording = False
        self.start_on_event = False #if the recording should start when a midi event arrives
        self._init_time = 0
        self._current_time = 0
        self._end_time = 0
        
        self._in_progress = [None for i in range(128)]
        self._record = [] #(AssociatedEvents list, needs to be ordered before returning it
        #self._event_history = []
        ############################
        #register function callbacks
        self.midi_pubsub.subscribe('note_on', self.on_note_on)
        self.midi_pubsub.subscribe('note_off', self.on_note_off)
        
    def reset(self):
        """
        """
        self._init_time = time.time()
        self._current_time = 0
        self._end_time = 0
        self._recording = False
        self._in_progress = [None for i in range(128)]
        self._record = []
        self._event_history = []

    def record(self):
        """
        """
        self.reset() 
        self._recording = True
        
    def stop(self):
        """
        stops the recording and returns the result of the recording plus the meta information
        """
        self._recording = False
        self._end_time = time.time()
        #sort events
        self._record.sort(key=lambda x: x.get_init_tick())
        return (self._meta, self._record)
        
    def on_note_on(self, event):
        """
        """
        
        if not self._recording:
            if not self.start_on_event:
                return
            self.record()

        self._current_time = time.time() - self._init_time
        curr_tick = sec2ticks(self._current_time, self.bpm, self.resolution)
        #IMPORTANT translate from pygame event to python_midi event
        event = pygame_event2python_midi(event)
        print event
        #self._event_history.append(event)
        #add the note on event to the current playing events
        if self._in_progress[event.pitch] is not None:
            print "Double NoteOnEvent without NoteOffEvent: %s .discarding old event %s." %(self._in_progress[event.pitch].note_on, event)
        #create new association and leave it incomplete
        ae = AssociatedEvents()
        ae.note_on = event
        #modify time as the one that comes from the midi capture is relative to some unknown
        ae.note_on.tick = curr_tick
        self._in_progress[event.pitch] = ae

    def on_note_off(self, event):
        """
        """
        if not self._recording:
            return
            
        self._current_time = time.time() - self._init_time
        curr_tick = sec2ticks(self._current_time, self.bpm, self.resolution)
        #translate from pygame event to python_midi event
        event = pygame_event2python_midi(event)
        print event
        #self._event_history.append(event)
        #search for the pairing event
        if self._in_progress[event.pitch] is None:
            print "NoteOffEvent without previous NoteOnEvent: ", event
        else:
            ae = self._in_progress[event.pitch]
            try:
                ae.note_off = event
                ae.note_off.tick = curr_tick
                self._record.append(ae)
                self._in_progress[event.pitch] = None
            except Exception as e:
                print e
    
    def on_event(self, event):
        """
        """
        pass
        
    def update(self):
        """
        """
        self._current_time = time.time()
        pass
