#!/usr/bin/env python

import sys

import pygame
from pygame.locals import *

from keyboard import *

pygame.init()
screen = pygame.display.set_mode((1060, 800), RESIZABLE)

clock = pygame.time.Clock() # create a clock object for timing

def setup():
    """
    sets up many things needed previous the game starting
    """
    pass


def teardown():
    """
    finishes everything that has to be ended before game exit
    """
    pass


def process_event(event):
    """
    process pygame events (keyboard, mouse and other events)
    """
    pass
    
    
def main():
    
    done = False
    
    #######################
    keyboard = Keyboard()
    
    #######################
    while not done:
        #process events
        for event in pygame.event.get():
            #check if finish
            if event.type == pygame.QUIT:
                        done = True
            #
            process_event(event)
            
        keyboard.update()
        keyboard.draw(screen)
        
        
        pygame.display.flip()
        clock.tick(120)
    

if __name__=="__main__":
    setup()
    main()
    teardown()
    pygame.quit()
    sys.exit()

