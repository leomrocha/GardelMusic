# -*- encoding: utf-8 -*-
"""
MIDI file loader and translator.
.SYNTHESYA file loader and translator.

can obtain out the (music challenge file format) file from the other formats


uses python-midi library to analyse midi files and 
associate note_on and note_off events


A single level consists of:
    - the MIDI file (mandatory)
    - the .meta file containing metadata about the midi file
    - .level file containing extra information
    - all the images, icons and other elements to show for the level
    
All level files are preferably in their own folder, and even better, compressed, the folder structure:

./this-level/mylevel.midi
./this-level/mylevel.meta
./this-level/mylevel.level
./this-level/mylevel.[mp3|ogg|wav]      - (optional, for real sound support instead of midi file)
./this-level/images/icon.png            - (optional)
./this-level/images/button_active.png   - (optional)
./this-level/images/button_hover.png    - (optional)
./this-level/images/button_passive.png  - (optional)
./this-level/images/backgorund.png      - (optional)



Meta file will be automatically created from  midi file if the .meta file does not exists

The .meta file format (based on the synthesia file format for compatibility):
    Title : string
    Subtitle : string
    Rating : integer [0-100]
    Difficulty : integer [0-100]
    BackgroundImage : string (relative path from this metadata file to an image)
    ButtonPassive : string (relative path from this metadata file to an image ) - image on button pressed, for the button selection of the level
    ButtonHover : string (relative path from this metadata file to an image ) - image on button pressed, for the button selection of the level
    ButtonActive : string (relative path from this metadata file to an image ) - image on button pressed, for the button selection of the level
    Icon: (relative path from this metadata file to an image) - icon to show 
    Composer : string
    Arranger : string
    Copyright : string
    License : string
    MadeFamousBy : string
    FingerHints : string
    HandParts : string
    Tags : list of free-form string descriptor tags.
    Bookmarks : list of pairs: ( an integer (1 or greater) measure number, optionally followed free-form string description.)
    

TODO think this more ......

The .level file format

Contains a description of the exercises of the level:



TODO add musicxml support
"""

import os

import pygame

#python-midi library
import midi

from file_loader import *

class Level(object):
    """
    """
    pass
