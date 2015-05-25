
import pygame
import pygame.midi

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

        self.input_id = pygame.midi.get_default_input_id()
        self.midi_in = pygame.midi.Input( self.input_id )

        print "midi input id = ", self.input_id
        print "midi in = ", self.midi_in
        
        self.output_id = pygame.midi.get_default_output_id()
        self.midi_out = pygame.midi.Output( self.output_id )
        
        print "midi output id = ", self.output_id
        print "midi out = ", self.midi_out
        
        self.note_on_subs = []
        self.note_off_subs = []
        
    def subscribe(self, midi_event, callback):
        """
        """
        
        if midi_event == 'note_on':
            self.note_on_subs.append(callback)
        if midi_event == 'note_off':
            self.note_off_subs.append(callback)
        
    def unsubscribe(self, midi_event, callback):
        """
        """
        if midi_event == 'note_on':
            self.note_on_subs.remove(callback)
        if midi_event == 'note_off':
            self.note_off_subs.remove(callback)

    def publish(self, midi_event, midi_id, velocity=127, channel=0):
        """
        """
        #WARNING for the moment is only nte_on and note_off and goes to the output
        vel = velocity * self.volume
        print "publishing event: ", midi_event, midi_id, vel
        try:
            if midi_event == 'note_on':
                self.midi_out.note_on(midi_id, vel)
            elif midi_event == 'note_off':
                self.midi_out.note_off(midi_id)
                
        except:
            print "couldn't send %s event to the midi output" % midi_event
        #
        pass
        
    def process_events(self, midi_events):
        """
        """
        print "processing midi events"
        
        for e in midi_events:
            #TODO
            print e
            
    def poll(self):
        if self.midi_in.poll():
                midi_events = i.read(10)
                        
                #print "full midi_events " + str(midi_events)
                    #print "my midi note is " + str(midi_events[0][0][1])
                # convert them into pygame events.
                midi_evs = pygame.midi.midis2events(midi_events, self.midi_in.device_id)
                
                self.process_events(midi_evs)
