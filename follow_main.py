#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

import pygame
import pygame.midi

import pygame.fastevent

#follow game
from follow_game import FollowGameEngine

#file loading:
from file_loader import *
######MIDI

from  midi_connection import MIDIPubSub
####

###Setup screen size automagically
import pygame.display


class FollowGameTest(object):
    """
    """
    def __init__(self, fpath=os.path.join("assets","midi") , fname="mary"):
        """
        """
        self._fname=fname
        #Setup video system with current video settings
        display_info = pygame.display.Info()
        self.scene_width, self.scene_height = display_info.current_w, display_info.current_h
        self.screen = pygame.display.set_mode((320, 240))
        #self.screen = pygame.display.set_mode((self.scene_width * 8/10, self.scene_height * 8/10))
        #self.screen = pygame.display.set_mode((self.scene_width * 5/10, self.scene_height * 5/10))

        pygame.display.set_caption("Follow Game Engine Test")

        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()

        #Setup Midi
        
        self.setup_midi()
        self._partitions = load_file(fpath, fname)
        
        #create drill (hardcoded for the moment)
        partition = self._partitions._partitions[0]
        song = self._partitions._song
        metronome_ticks = self._partitions._metronome_ticks
        measure_ticks = self._partitions._measure_ticks
        ticks_per_measure = self._partitions._ticks_per_measure
        
        drill = DrillInfo.create_drill(partition, song, metronome_ticks, measure_ticks, ticks_per_measure)
        
        self._game = FollowGameEngine(self.midi_pubsub, drill)
        
    def setup_midi(self):
        """
        """
        self.midi_pubsub = MIDIPubSub()
        #self.midi_active = False
        self.midi_active = True

    def loop(self):
        """
        Game loop
        """
        print "press SPACE to start or stop"
        #time = self.clock.tick(100)
        while not self.quit_flag:
            #time = self.clock.tick(200)
            time = self.clock.tick(100)
            
            # EXIT process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
			            self.quit()
                    elif event.key == pygame.K_SPACE:
                        self._game.toggle()
	            #scene event handling (has to be here because loop over events empties the queue
                self._game.on_event(event)

            #            
            self._game.update()
            self._game.draw()
            
            pygame.display.flip()

    def quit(self):
        self.quit_flag = True


def setup():
    """
    sets up many things needed previous the game starting
    """
    # setup mixer to avoid sound lag
    pygame.mixer.pre_init(44100, -16, 2, 2048) 
    #pygame
    pygame.init()
    #time.sleep(0.2) #just in case ... ?
    pygame.fastevent.init()
    #midi
    pygame.midi.init()
    #sound
    #pygame.mixer.init()


def teardown():
    """
    finishes everything that has to be ended before game exit
    """
    #print "ending application"
    #print "quit midi"
    pygame.midi.quit()
    #print "quit display"
    #pygame.display.quit()
    #print "quitting pygame"
    pygame.quit()
    #print "c'est fini"
    #print "____"
    

def process_event(event):
    """
    process pygame events (keyboard, mouse and other events)
    """
    pass
    
def main():
    game = FollowGameTest()
    
    #dir.change_scene_by_name("home_scene"), not needed now that the scenes are managed by name and there is an initial scene
    game.loop()


if __name__=="__main__":
    setup()
    main()
    teardown()
    sys.exit(0)
