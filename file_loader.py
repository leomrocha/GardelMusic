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


def ticks2musec(ticks, BPM, resolution):
    """
    microseconds
    """
    # micro seconds per beat
    #muspb = 60. * 1000000 /  BPM
    #micro seconds per tick
    #muspt = muspb / resolution
    #return muspt * ticks .
    return ticks * 60000000. / (BPM * resolution)
    
def ticks2ms(ticks, BPM, resolution):
    """
    milliseconds
    """
    # micro seconds per beat
    #muspb = 60. * 1000000 /  BPM
    #micro seconds per tick
    #muspt = muspb / resolution
    #return muspt * ticks / 1000.
    
    return ticks * 60000. / (BPM * resolution)


def ticks2sec(ticks, BPM, resolution):
    """
    seconds
    """
    #return ticks2ms(ticks, BPM, resolution) / 1000. ## ===
    #return (60. / BPM)/resolution ## ===
    return  ticks * 60. / (BPM * resolution)
    
    

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


class AssociatedEvents(object):
    """
    Contains one associated NoteOn with a NoteOff events
    NoteOffEvent is later than NoteOnEvent
    """
    
    def __init__(self):
        self.data = [None, None]
    
    def get_note_on(self):
        return self.data[0]
    def set_note_on(self, event):
        if not is_note_on(event):
            raise ValueError('Not a valid NoteOnEvent')
        self.data[0] = event
    
    note_on = property(get_note_on, set_note_on)

    def get_note_off(self):
        return self.data[1]
    def set_note_off(self, event):
        #validate
        if self.data[0] is None:
            raise ValueError("NoteOnEvent not set, can't set NoteOffEvent")
        elif not is_note_off(event):
            raise ValueError('Not a valid NoteOffEvent: %s' % str(event))
        elif event.tick < self.data[0].tick:
            raise ValueError('Not a valid tick time for NoteOffEvent (tick < NoteOnEvent.tick')
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
        return self.data[0] is not None and self.data[1] is not None 
    
    def get_pitch(self):
        """
        returns the pitch, or 0 if no data
        """
        if self.data[0] is not None:
            return self.data[0].pitch
        return 0
    
    def get_duration(self):
        """
        Returns the duration in ticks, or 0 if missing data
        """
        if self.data[0] is not None and self.data[1] is not None:
            return self.data[1].tick - self.data[0].tick
        return 0
    
    def get_init_tick(self):
        """
        Returns NoteOnEvent tick
        if no data available, returns -1
        """
        if self.data[0] is not None:
            return self.data[0].tick
        return -1

    def get_end_tick(self):
        """
        Returns NoteOffEvent tick
        if no data available, returns -1
        """
        if self.data[1] is not None:
            return self.data[1].tick
        return -1


class MidiInfo(object):
    """
    * the pattern object
    * a dict containing all the metainfo of the file
    * a list of tracks
       - each track contains a list of events
       - the events are ordered by time|tick
       - the tick time is absolute

    """
    def __init__(self, fname):
        """
        fname: the file path to read
        """
        self.pattern = midi.read_midifile(fname)
        #TODO check that the pattern is valid
        self.info_dict = self.extract_meta(self.pattern[0])
        self.tracks = []
        #TODO make the track analysis
        self.pattern.make_ticks_abs()
        #make ticks absolute
        for t in self.pattern[1:]:
            self.tracks.append(self.associate_events(t))

    def get_tempo(self):
        """
        returns: (bpm, mpqn)
        mpqn = milliseconds per quarter note
        """
        #default values
        ret = (120, 60 * 1000000 / 120)
        if "tempo" in self.info_dict:
            ret = (self.info_dict["tempo"].bpm, self.info_dict["tempo"].mpqn)
        return ret
    
    def get_resolution(self):
        """
        """
        return self.pattern.resolution
        
    def get_time_signature(self):
        """
        """
        #TODO
        pass
        
    @staticmethod
    def extract_meta(meta_track):
        """
        Extracts meta-information from the meta_track (normally is the first 
        track located, i.e. : the pattern[0] track
        """
        info = {}
        info["extra"] = []
        for e in meta_track:
            if isinstance(e, midi.TimeSignatureEvent):
                info["time_signature"] = e
            elif isinstance(e, midi.KeySignatureEvent):
                info["key_signature"] = e
            elif isinstance(e, midi.SetTempoEvent):
                info["tempo"] = e
            elif isinstance(e, midi.SmpteOffsetEvent):
                info["smpte_offset"] = e
            elif isinstance(e, midi.InstrumentNameEvent):
                info["instrument"] = e
            else:
                info["extra"].append(e)
        return info        
    
    @staticmethod
    def associate_events(track):
        """
        for the given track (as output from analyse_midi) creates pairs of associated events (note_on, note_off)
        
        track: an absolute tick ordered list of midi events (Track object from python-midi)
        
        returns: an ordered (by tick|time) list of the associated events
        """
        #all the associations    
        associations = []
        #associations in progress of being built
        in_progress = [None for i in range(128)]
        
        for e in track:
            #print e
            if is_note_off(e):
                if in_progress[e.pitch] is None:
                    print "NoteOffEvent without previous NoteOnEvent: ", e
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
                    print "Double NoteOnEvent without NoteOffEvent: ", in_progress[e.pitch].note_on, e
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
                print "ERROR, there are missing associations: ", i, i.note_on, i.note_off
            
        return associations

#####
#midi file writer
#####

#TODO


