# -*- coding: utf-8 -*-
"""
This file contains :
midi id, number id, name id (number), associated color id, x, y, width, height

x,y,width and height are given in 
"""


NAMES_ENGLISH = {
    0:['C'],
    1:['C#','Db'],
    2:['D'],
    3:['D#','Eb'],
    4:['E'],
    5:['F'],
    6:['F#','Gb'],
    7:['G'],
    8:['G#','Ab'],
    9:['A'],
    10:['A#','Bb'],
    11:['B'], 
    }
    

NAMES_GERMAN = {
    0:['C'],
    1:['C#','Db'],
    2:['D'],
    3:['D#','Eb'],
    4:['E'],
    5:['F'],
    6:['F#','Gb'],
    7:['G'],
    8:['G#','Ab'],
    9:['A'],
    10:['A#','Hb'],
    11:['H'], 
    }


NAMES_LATIN = {
    0:['DO'],
    1:['DO#','REb'],
    2:['RE'],
    3:['RE#','MIb'],
    4:['MI'],
    5:['FA'],
    6:['FA#','SOLb'],
    7:['SOL'],
    8:['SOL#','LAb'],
    9:['LA'],
    10:['LA#','SIb'],
    11:['SI'],
    }


def get_octave(midi_id):
    return int(midi_id / 12)

    
def get_note_name(midi_id, lang='latin'):
    if lang == 'english':
        return NAMES_ENGLISH[midi_id]
    elif lang == 'german':
        return NAMES_GERMAN[midi_id]
    #by default asume note names are in latin
    return NAMES_LATIN[midi_id]

        
keyboard_map = {

}
