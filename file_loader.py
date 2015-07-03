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
import json

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


def ticksPerMeasure(numerator, denominator, resolution):
    """
    Ticks in a measure
    """
    #TODO find out if there is the need to calculate it better, I don't trust my calculations yet ... :/
    #return (numerator * resolution)  / (4/denominator)
    return numerator * resolution
    

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
        """
        """
        # midi event [note_on, not_off]
        self.data = [None, None]
        # play_hint  = [hand/foot, "right/left", finger id if needed or None]
        #TODO this is useful for piano and drums, extend for guitar and other instruments later
        #TODO hand = h, foot = f, left = l, right = r
        self.__play_hint = ["hand", "right", 1]
        
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
            raise ValueError('Event Error; Not a valid NoteOffEvent: %s' % str(event))
        elif event.tick < self.data[0].tick:
            raise ValueError('Tick Error; Not a valid tick time for NoteOffEvent (tick < NoteOnEvent.tick')
        elif event.pitch < self.data[0].pitch:
            raise ValueError('Pitch Error; NoteOfEvent.pitch is NOT the same as NoteOnEvent.pitch')
        #validation completed, now save the event
        elif event.channel != self.data[0].channel:
            raise ValueError('Channel Error; NoteOfEvent.channel is NOT the same as NoteOnEvent.channel')
        self.data[1] = event

    note_off = property(get_note_off, set_note_off)

    def set_hint(self, hint):
        """
        hint = (hand/foot, right/left, finger id) # 3 item iterable
        if one of the values is None, that value will NOT be set. Only non None values will be set
        """
        for i in range(3):
            if hint[i] is not None:
                #TODO verify value is valid
                self.__play_hint[i] = hint[i]

    def get_hint(self):
        """
        """
        return self.__play_hint

    play_hint = property(get_hint, set_hint)

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

    def to_dict(self):
        """
        Returns the information of the object in a dict (for serialization to json for example)
        """
        ret = { ## TODO note_on = on; note_off = off; hint = ??
              "note_on": { ## tick = t; pitch = p; velocity = v
                        "tick": self.data[0].tick,
                        #"channel": self.data[0].channel,
                        "pitch": self.data[0].pitch,
                        "velocity": self.data[0].velocity
                    },
              
              "note_off": {
                        "tick": self.data[1].tick,
                        #"channel": self.data[0].channel,
                        "pitch": self.data[1].pitch,
                        "velocity": self.data[1].velocity
                    },
              #channel should be the same for both, note_on and note_off
              "channel": self.data[0].channel,
              #"duration"
              "hint": self.__play_hint
        }
        
        return ret

    @classmethod
    def from_dict(cls, event_dict):
        """
        Create an instance from a dict containing the information
        """        
        ret = cls()
        note_on = midi.events.NoteOnEvent()
        note_on.tick = event_dict["note_on"]["tick"]
        note_on.pitch = event_dict["note_on"]["pitch"]
        note_on.velocity = event_dict["note_on"]["velocity"]
        note_on.channel = event_dict["channel"]

        note_off = midi.events.NoteOnEvent()
        note_off.tick = event_dict["note_off"]["tick"]
        note_off.pitch = event_dict["note_off"]["pitch"]
        note_off.velocity = event_dict["note_off"]["velocity"]
        note_off.channel = event_dict["channel"]
        
        
        ret.note_on = note_on
        ret.note_off = note_off
        ret.hint = event_dict["note_off"]["hint"]
        return ret

    @classmethod
    def from_JSON_string(cls, json_string):
        """
        Load
        """
        data_dict = json.loads(json_string)
        ret = AssociatedEvents.from_dict(data_dict)
        return ret

    @classmethod
    def from_JSON_file(cls, fpath):
        """
        Load
        """
        data_dict = json.loads(fpath)
        ret = cls.from_dict(data_dict)
        return ret

    def to_JSON(self):
        """
        returns JSON string representing this object
        """
        return json.dumps(self.to_dict())


class TrackMetaInfo(object):
    """
    Meta Information about a track
    """
    #TODO 
    pass


class TrackInfo(object):
    """
    Information about a track
    Meta information about the track
    the track itself is an ordered list of AssociatedEvents, ordered by note_on time
    """
    
    def __init__(self):
        """
        """
        #TODO implement this as a sorted list or a btree or some tree that keeps things in inorder
        self._events = []
        #self._meta = MetaInfo()
        
    def __sort(self):
        """
        Sorts the AssociatedEvents by 
        """
        self._events.sort(key=lambda x: x.get_init_tick())
        
    def add_event(self, event):
        """
        Adds an AssociatedEvent to the given
        """
        self._events.append(event)
        self.__sort()
    
    def add_events(self, events):
        """
        Adds an AssociatedEvent list to the current track
        """
        if type(events) is list:
            self._events.extend(events)
        else:
            #asume iterable
            for e in events:
                self._events.append(e)
        #sort the events
        self.__sort()
        #TODO make this more efficient, but for the moment, it doesn't matter
        
    def get_events(self):
        """
        """
        return self._events
        
    def set_meta(self, meta):
        """
        sets the meta information about the track
        """
        #TODO 
        pass
        
    def to_dict(self):
        """
        """
        ret = {
            "events": [e.to_dict() for e in self._events],
            #TODO track meta info ... future when needed
            #"meta": self._meta.to_dict()
        }
        return ret

    @classmethod
    def from_dict(cls, event_dict):
        """
        Create an instance from a dict containing the information
        """        
        ret = cls()
        #TODO
        events = [AssociatedEvent.from_dict(e) for e in event_dict["events"]]
        ret.add_events(events)
        return ret

    @classmethod
    def from_JSON_string(cls, json_string):
        """
        Load
        """
        data_dict = json.loads(json_string)
        ret = cls.from_dict(data_dict)
        return ret

    @classmethod
    def from_JSON_file(cls, fpath):
        """
        Load
        """
        data_dict = json.loads(fpath)
        ret = cls.from_dict(data_dict)
        return ret

    def to_JSON(self):
        """
        returns JSON string representing this object
        """
        return json.dumps(self.to_dict())


class SongInfo(object):
    """
    Represents a musical piece or song
    contains a list of tracks, each track contains a certain information
    Tracks can be separated by
    """
    def __init__(self):
        """
        """
        self._meta = {} 
        self._tracks = []
        
    def add_track(self, track, pos=None):
        """
        """
        if pos is None:
            pos = len(self._tracks)
        self._tracks.append(pos, track)

    def add_tracks(self, tracks):
        """
        """
        self._tracks.extend(tracks)

    def add_track(self, track):
        """
        """
        #TODO verify type
        self._tracks.append(track)

    def get_tracks(self):
        """
        """
        return self._tracks

    def set_meta(self, meta):
        """
        """
        #TODO make some more things test and verify data, etc
        self._meta = meta
    
    def get_meta(self):
        """
        """
        return self._meta

    meta = property(get_meta, set_meta)
    
    def to_dict(self):
        """
        """
        ret = {
            "meta" : self._meta, #WARNING, this with midi events might not work ... see how to fix this
            "tracks": [t.to_dict() for t in self._tracks]
        }
        return ret

    @classmethod
    def from_dict(cls, song_dict):
        """
        Create an instance from a dict containing the information
        """        
        ret = cls()
        tracks = [TrackInfo.from_dict(t) for t in song_dict["tracks"]]
        meta = song_dict["meta"] #WARNING this will not work correctly
        ret.add_tracks(tracks)
        ret.meta = meta
        return ret

    @classmethod
    def from_JSON_string(cls, json_string):
        """
        Load
        """
        data_dict = json.loads(json_string)
        ret = cls.from_dict(data_dict)
        return ret

    @classmethod
    def from_JSON_file(cls, fpath):
        """
        Load
        """
        data_dict = json.loads(fpath)
        ret = cls.from_dict(data_dict)
        return ret

    def to_JSON(self):
        """
        returns JSON string representing this object
        """
        return json.dumps(self.to_dict())


class DrillSetInfo(object):
    """
    Contains the information for a single drill set of the song
    A drill set will be used to generate the following drills:
        - rithm drill
        - auditive memory drill
        - reading drill
    """

    #def __init__(self, name, content, dependencies, measure_ticks=None, metronome_ticks=None, song_info=None)
    def __init__(self, name, content, dependencies):
        """
        """
        #intrinsec values, the ones that give identity to this drill set
        self._name = name
        self._content = content
        self._dependencies = dependencies
        self._deps_ids = [d.name for d in dependencies]
        #reference to tempo and song information
        #ticks list containing the ticks for each mesure
        #self.measure_ticks = measure_ticks
        #ticks for the metronome
        #self.metronome_ticks = metronome_ticks
        #song information (all the notes and hints
        #self._song_info = song_info

    def to_dict(self):
        """
        Note nor tempo nor song information are serialized.
        This is because if so, it'll duplicate data that in reality accompanies a list of drills (or a tree)
        """
        return {'name':self._name, 'content':self._content, 'deps':self._dependencies.to_dict()} #TODO fix this, will break if deps are not objects ...

    def from_dict(self, data_dict):
        """
        """
        #TODO validte that all the data is correct!!
        self._name = data_dict['name']
        self._content = data_dict['content']
        self._deps_ids = data_dict['deps']
        #self._dependencies = data_dict['...']
        
    def to_JSON(self):
        """
        """
        return json.dumps(self.to_dict())

    def from_JSON(self, json_str):
        """
        """
        return from_dict(json.loads(json_str))

class PartitionedSongInfo(object):
    """
    Contains the Song and details about the partitions that'll form the levels
    A song can be partitioned in different sections/paragraphs, 
    these paragraphs contain different information (keys, tempo, and so on, TODO not implemented in this first version)
    The partitions form a Tree, this tree contains information on how logically the creator of this partition
    thinks is better. This tree goes from simple elements on the song to the complete song
    An automated partitioner is provided, this will partition the song with the given parameters
    Partitioner available:
     - per measure (given the BPM data), will partition per measure and then will start joining contiguous measures
     
    """
    def __init__(self):
        """
        """
        self._song = None
        self._partitions = []
        self._measure_ticks = []
        self._metronome_ticks = []

    @staticmethod
    def tree_trasversal(tree):
        """
        ???
        """
        #TODO
        pass
        
    @staticmethod
    def tree_reversal(tree):
        """
        Returns the reversed tree, ... TODO
        """
        #TODO
        pass
        
    @staticmethod
    def flatten_tree(object):
        """
        Flattens a tree giving back an array, the dependencies are changed for names instead of direct object
        
        """
        #TODO
        pass

    @staticmethod
    #def array_to_tree(arr, measure_ticks, metronome_ticks, song_info):
    def array_to_tree(arr):
        """
        Recursive tree generation, this is a simple case for level generation
        The tree nodes are DrillSetInfo nodes
        ##the tree has nodes with structure: {'name':[first_node, last_node] | node, 'content':arr, 'deps':[LIST OF DEPS]}
        """
        l = len(arr)
        if l<=1:
            #return DrillSetInfo(name=arr, content=arr, dependencies = (), measure_ticks, metronome_ticks, song_info)
            return DrillSetInfo(name=arr, content=arr, dependencies = ())
        #drill = DrillSetInfo(name=[arr[0], arr[l-1]], content=arr, dependencies = (part(arr[:l/2]),part(arr[l/2:])), measure_ticks, metronome_ticks, song_info)
        drill = DrillSetInfo(name=[arr[0], arr[l-1]], content=arr, dependencies = (part(arr[:l/2]),part(arr[l/2:])))
        return drill

    @staticmethod
    def array_to_dict_tree(arr):
        """
        Recursive tree generation, this is a simple case for level generation
        the tree has nodes with structure: {'name':[first_node, last_node] | node, 'content':arr, 'deps':[LIST OF DEPS]}
        """
        l = len(arr)
        if l<=1:
            return {'name':arr, 'content':arr, 'deps':()}
        drill = {'name':[arr[0], arr[l-1]], 'content':arr, 'deps':(part(arr[:l/2]),part(arr[l/2:]))}
        return drill

    @staticmethod
    def get_song_duration(song_info):
        """
        Calculates the duration of the song in ticks and time
        returns ticks_begin, ticks_end
        """
        #TODO make this algorithm more efficient, for the moment it takes linear time and this is NOT good
        #This is the WORST possible algorithm for douing this, but the problem is that the last note to start might not be the last to end
        #start is always zero
        #start = 0
        #begin is the beginning of the first note
        begin = 0
        #end is the end of the last note
        end = 0
        for t in song_info.get_tracks():
            for e in t.get_events():
                tk = e.note_on.tick
                if tk < begin:
                    begin = tk
                tk = e.note_off.tick
                if tk > end:
                    end = tk
        return (begin, end)
        
    #TODO
    @classmethod
    def measure_partition(cls, song_info):
        """
        """
        #TODO this measure partition DOES NOT consider that the tempo can change
        #also, multiple tempos for right and left hand might not be well handled ... I don't know about this
        start_tick = 0
        #get song duration, starting note and end note. start_tick is always 0 begin_tick is the tick of start of the first note played
        begin_tick, end_tick = PartitionedSongInfo.get_song_duration(song_info)
        #get BPM
        print "meta"
        print song_info.meta
        
        bpm = song_info.meta['tempo'].bpm

        #get tempo signature to know how many beats per measure we'll have
        time_signature = song_info.meta['time_signature']
        ppq = song_info.meta['resolution'] # ticks per quarter note
        num = time_signature.numerator
        den = time_signature.denominator
        tpm = ticksPerMeasure(num, den, ppq)
        #generate the metronome beat array 
        metronome_ticks = range(0, end+1, tpm)
        #generate the measure marks
        measure_ticks = metronome_ticks[::num]
        #measure ids
        measure_ids = range(len(measure_ticks))
        #Generate dependency tree (array_to_tree ...)?
        #partitions = PartitionedSongInfo.array_to_tree(measure_ids, measure_ticks, metronome_ticks, song_info)
        partitions = PartitionedSongInfo.array_to_tree(measure_ids)
        
        ret = cls()
        ret._song_info = song_info
        ret._partitions = partitions
        ret._metronome_ticks = metronome_ticks
        ret._measure_ticks = measure_ticks
        
        return ret
        
    #@classmethod
    #def notes_partition(cls, song_info)
    #    """
    #    """
    #    #TODO
    #    pass


class MidiInfo(object):
    """
    * the pattern object
    * a dict containing all the metainfo of the file
    * a list of tracks
       - each track contains a list of events
       - the events are ordered by time|tick
       - the tick time is absolute

    for practical purposes:
        - track 0 is considered right hand
        - track 1 is considered left hand
    
    """
    #TODO REFACTOR this object is quite AWFUL, it started as a test and now is something bigger
    #TODO REFACTOR to make it better
    
    def __init__(self, fname):
        """
        fname: the file path to read
        """
        self.pattern = midi.read_midifile(fname)
        #TODO check that the pattern is valid
        self.info_dict = self.extract_meta(self.pattern[0])
        self.info_dict["resolution"] = self.get_resolution()
        
        self.tracks = []
        #make the track analysis
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

    def to_song(self):
        """
        Returns a SongInfo object with the information in the current object
        """
        #TODO 
        song = SongInfo()
        song.meta = self.info_dict
        for i in range(len(self.tracks)):
            #assume track number: :0 = right hand; 1 = left hand; 2 = right foot; 3 = left foot
            #assume finger number = 1
            hint = ["right","hand",1]
            if i == 1:
                hint = ["left","hand",1]
            elif i == 2:
                hint = ["right","foot",1]
            elif i == 3:
                hint = ["left","foot",1]
            track = TrackInfo()            
            #set the hints by default as they come from midi file tracks
            for ae in self.tracks[i]:
                ae.play_hint = hint
            track.add_events(self.tracks[i])
            song.add_track(track)

        return song


def load_midi2song(fpath):
    """
    Loads a MIDI file into a SongInfo object
    """
    midi_info = MidiInfo(fpath)
    song = midi_info.to_song()
    return song


def load_midi2partition(fpath):
    """
    Loads a MIDI file into a song and creates the partition automatically (measure partition method)
    """
    midi_info = MidiInfo(fpath)
    song = midi_info.to_song()
    partition = PartitionedSongInfo.measure_partition(song)
    return partition


#####
#midi file writer
#####

#TODO


