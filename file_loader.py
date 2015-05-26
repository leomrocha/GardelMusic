# -*- encoding: utf-8 -*-
"""
MIDI file loader and translator.
TODO - .SYNTHESYA file loader and translator.
TODO - MUSICXML file loader and translator

loading a file returns:
    a pygame midi object ready to play
    a dict containing the metadata of the file (name, KeySignature, TempoSignature, etc...)
    a list containing all the events, events are in relative ticks

"""

import os

import pygame

#python-midi library
import midi

################################################################################
#Time transformations

def ticks2sec(ticks, BPM, resolution):
    """
    """
    # micro seconds per beat
    muspb = 60. * 1000000 /  BPM
    sec = muspb / resolution
    return sec
    
def ticks2ms(ticks, BPM, resolution):
    """
    """
    return ticks2sec(ticks, BPM, resolution) * 1000
    

################################################################################

#####
# loading midi file to be able to play it
#####

def load_midi_to_play(fname):
    """
    loads the given fname file and returns the mixer object
    """
    return pygame.mixer.music.load(fname)

#####
#midi file analyzer
#####
def analyse_midi(fname):
    """
    Loads and analyses the given file creating a description of the file with:
    * the pattern object
    * a dict containing all the metainfo of the file
    * a list of tracks
       - each track contains a list of events
       - the events are ordered by time|tick
       - the tick time is absolute
    """
    #TODO
    pattern = midi.read_midifile("../../tests_midi/python-midi/mary.mid")
    info_dict = {}
    tracks = []
    #TODO make the analysis
    return (pattern, info_dict, tracks)
    

class AssociatedEvents(object):
    """
    Contains a NoteOn and NoteOff event
    """
    
    def __init__(self):
        self.data = [None, None]
    
    def get_note_on(self):
        return self.data[0]
    def set_note_on(self, event):
        if not isinstance(event, midi.NoteOnEvent):
            raise ValueError('Not a valid NoteOnEvent')
        self.data[0] = event
    
    note_on = property(get_note_on, set_note_on)

    def get_note_off(self):
        return self.data[1]
    def set_note_off(self, event):
        #validate
        if self.data[0] is None:
            raise ValueError("NoteOnEvent not set, can't set NoteOffEvent")
        elif not isinstance(event, midi.NoteOffEvent):
            raise ValueError('Not a valid NoteOffEvent')
        elif event.tick < self.data[0].tick:
            raise ValueError('Not a valid tick time for NoteOfEvent (tick < NoteOnEvent.tick')
        elif event.pitch < self.data[0].pitch:
            raise ValueError('NoteOfEvent.pitch is NOT the same as NoteOnEvent.pitch')
        #validation completed, now save the event
        self.data[1] = event
        

    note_off = property(get_note_off, set_note_off)

    def is_complete(self):
        """
        returns True if contains a note_on and a note_off event 
        where note_off 
        """

def is_note_on(event):
    """
    checks if is instance of note on event
    shortcut to avoid writing isinstance code
    """
    ret = isinstance(event, midi.NoteOnEvent)
    return ret

def is_note_off(event):
    """
    checks if is instance of note of or if is note on and has velocity 0
    """
    ret = isinstance(event, midi.NoteOffEvent) or (isinstance(event, midi.NoteOnEvent) and event.velocity == 0)
    return ret

def associate_events(track):
    """
    for the given track (as output from analyse_midi) creates pairs of associated events (note_on, note_off)
    returns an ordered (by tick|time) list of the associated events
    """
    #all the associations    
    associations = []
    #associations in progress of being built
    in_progress = [None for i in range(128)]
    
    for e in track:
        #print e
        if is_note_off(e):
            if in_progress[e.pitch] is None:
                print "NoteOffEvent without previous NoteOnEvent"
                print e
            else:
                ae = in_progress[e.pitch]
                try:
                    ae.note_off = e
                    associations.append(ae)
                    in_progress[e.pitch] = None
                except Exception as e:
                    print e
                    
        elif is_note_on(e):
            #verify that the note is already OFF, (no note should be activated Twice without being turned off ... TODO check this assumption
            if in_progress[e.pitch] is not None:
                print "Double NoteOnEvent without NoteOffEvent ... what to do ...?"
                print in_progress[e.pitch], e
            #create new association
            ae = AssociatedEvents()
            ae.note_on = e
            in_progress[e.pitch] = ae
        else:
            #print "is NOT a note event: ", e
            pass
    
    #TODO order by initial tick time (the result of the algorithm is note off time ..)
    
    
    #verify that all the events are matched
    for i in in_progress:
        if i is not None:
            print "ERROR, there are missing associations: ", i 
        
    return associations


#####
#midi file writer
#####


