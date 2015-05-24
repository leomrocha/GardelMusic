#!/usr/bin/env python

import sys

import pygame
from pygame.locals import *

from keyboard import *

pygame.init()
screen = pygame.display.set_mode((1200, 800), RESIZABLE)

clock = pygame.time.Clock() # create a clock object for timing


def main():
    
    done = False
    while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        keyboard = Keyboard()
        clock.tick(120)
        pygame.display.flip()
        

if __name__=="__main__":
    main()
    pygame.quit()
    sys.exit()

