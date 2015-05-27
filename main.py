#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

import pygame
import pygame.midi

import pygame.fastevent

import director

#pygame.display.set_caption("Piano Challenge")

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
    pygame.midi.quit()
    pygame.quit()
    

def process_event(event):
    """
    process pygame events (keyboard, mouse and other events)
    """
    pass
    
def main():
    dir = director.Director()
    
    #dir.change_scene_by_name("home_scene"), not needed now that the scenes are managed by name and there is an initial scene
    dir.loop()


if __name__=="__main__":
    setup()
    main()
    teardown()
    sys.exit()

