# -*- coding: utf-8 -*-
import pygame
import pygame.midi

import midi

def pygame_event2python_midi(event):
    """
    Transforms a Pygame Midi Event to a python_midi event.
    This should be later completed and replace directly from midi input event to python midi event and
    bypass the midis2events of pygame.
    For the moment this only transforms NoteOn and NoteOff events, TODO the others
    """
    ret = event
    if event.status == 144:
        ret = midi.events.NoteOnEvent()
        ret.tick =  event.timestamp ##UNKNOWN, here I can put a timestamp, but nothing else
        ret.pitch = event.data1
        ret.velocity = event.data2
        ret.channel = event.data3
    elif event.status == 128:
        ret = midi.events.NoteOffEvent()
        ret.tick =  event.timestamp ##UNKNOWN, here I can put a timestamp, but nothing else
        ret.pitch = event.data1
        ret.velocity = event.data2
        ret.channel = event.data3

    return ret

class MIDIPubSub(object):
    """
    Pubsub for MIDI
    This object connects the midi events between modules
    """
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    def __init__(self):
        """
        """

        #Volume (0->1)
        self.volume = 0.5

        #get number of devices
        device_count = pygame.midi.get_count()

        #self.input_id = pygame.midi.get_default_input_id()
        self.input_id = device_count -1
        self.midi_in = pygame.midi.Input( self.input_id )

        #print "midi input id = ", self.input_id
        #print "midi in = ", self.midi_in
        #print "midi in info = ", pygame.midi.get_device_info(self.input_id)
        
        #self.output_id = pygame.midi.get_default_output_id()
        self.output_id = device_count - 2
        
        self.midi_out = pygame.midi.Output( self.output_id )
        
        #print "midi output id = ", self.output_id
        #print "midi out = ", self.midi_out
        #print "midi out info = ", pygame.midi.get_device_info(self.output_id)
        
        self.note_on_subs = []
        self.note_off_subs = []

        #pedal event subscriptions, as there is no on/off, but velocity changes only this way is clan to be handled        
        self.sustain_subs = []
        
        
    def subscribe(self, midi_event, callback):
        """
        """
        
        if midi_event == 'note_on':
            self.note_on_subs.append(callback)
        elif midi_event == 'note_off':
            self.note_off_subs.append(callback)
        elif midi_event == 'sustain':
            self.sustain_subs.append(callback)
            
            
    def unsubscribe(self, midi_event, callback):
        """
        """
        if midi_event == 'note_on':
            self.note_on_subs.remove(callback)
        elif midi_event == 'note_off':
            self.note_off_subs.remove(callback)
        elif midi_event == 'sustain':
            self.sustain_subs.remove(callback)

    def publish(self, midi_event, midi_id, velocity=127, channel=0):
        """
        """
        #WARNING for the moment is only nte_on and note_off and goes to the output
        vel = int(velocity * self.volume)
        #print "publishing event: ", midi_event, midi_id, vel
        try:
            if midi_event == 'note_on':
                self.midi_out.note_on(midi_id, vel)
            elif midi_event == 'note_off':
                self.midi_out.note_off(midi_id)
                
        except Exception as e:
            print "couldn't send %s event with midi_id = %d and velocity = %d to the midi output" % (midi_event, midi_id, vel)
            print "failed with error %s" %e
        #
        pass
        
    def process_events(self, midi_events):
        """
        """
        #print "processing midi events"
        
        for e in midi_events:
            #TODO
            #print "processing midi event"
            #status = e.status ##144 == note_on, 128 == note off
            #handle note_on_ && note_off
            #midi_id = e.data1
            #velocity = e.data2
            subs = []
            if e.status == 144:
                subs = self.note_on_subs
            elif e.status == 128:
                subs = self.note_off_subs
            #TODO handle pedal correctly
            #WARNING, the sustain pedal is sending the same signal as central Mi: decimal = 64 
            #the only thing is that the pedal always sends max volume
            #the pedal sends 4 signals with status == 176,177,178,179 with velocity 127 to pedal on and velocity 0 pedal off
            ###
            elif e.status == 176:
                #print e
                subs = self.sustain_subs
            #call all the subscribers
            for cback in subs:
                cback(e)
            
    def poll(self):
        if self.midi_in.poll():
                midi_events = self.midi_in.read(10)
                        
                #print "full midi_events " + str(midi_events)
                    #print "my midi note is " + str(midi_events[0][0][1])
                # convert them into pygame events.
                #TODO FIXME change the pygame event for a python_midi event conversion here
                midi_evs = pygame.midi.midis2events(midi_events, self.midi_in.device_id)
                
                self.process_events(midi_evs)
