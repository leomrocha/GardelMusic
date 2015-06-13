# -*- coding: utf-8 -*-
"""
I don't know where to put this so I write it down here

This file contains the mappings for the notes according to the following format:

midi_id, pos
"""

import keyboard_mappings

#number of spaces in the sheet
N_SPACES = 28
#number of lines in the sheet
N_LINES = 27
#position of the Central Do note
C_POS = 24
#number of positions
NATURAL_POS = 57 ## == spaces * 2 + 1 counting the zero and max position


def _generate_pos(start=21, end=108):
    """
    generates the dict containing the positions for midi_ids in the following order:
    is a dict of dicts:
    midi_id: ('natural': pos, 'b': pos, '#': pos)
    """
    # first generate the position for the white keys
    counter = 1
    pos_dict = {}
    for mid in range(start, end+1):
        kc = keyboard_mappings.get_key_color_from_midi(mid)
        #print 'mid = %d, kc = %s, pos = %d' % (mid, kc, counter)
        if kc is 'white':
            pos_dict[mid] = (counter, counter, counter)
            counter+=1
        if kc is 'black':
            pos_dict[mid] = (-1, counter, counter+1)
    # now generate the positions for the black keys
    #for mid in range(start, end+1):
    #    kc = keyboard_mappings.get_key_color_from_midi(mid)
    #    if kc is 'black':
    #        pos_dict[mid] = (-1, pos_dict[mid-1][0], pos_dict[mid+1][0])
    return pos_dict
    
NOTE_RANGE = (21,108)
NOTES_POS = _generate_pos()

print NOTES_POS

def get_note_pos(midi_id, accidental="natural"):
    """
    Return position of the given midi_id note accordingto the accidental
    Accidentals can be: natural: ('' or 'natural'), flat 'b', sharp '#', 
    if accidental length > 1 for the moment is ignored but TODO add support for multiple accidentals
    if it is a white key note (Do, Re, Mi, Fa, Sol, La, Si) it'll take nothing as natural and no modification will be done
    if it is a black note, an accidental MUST be given or it'll assume is a sharp
    """
    #initialization just in case:
    #global NOTE_RANGE
    #global NOTES_POS
    #if NOTES_POS is None:
    #    NOTES_POS = _generate_pos()
    #assert rante, TODO change for a dynamic value
    assert midi_id >= NOTE_RANGE[0]
    assert midi_id <= NOTE_RANGE[1]
    #
    if accidental == 'b':
        return NOTES_POS[midi_id][1]
    elif accidental == '#':
        return NOTES_POS[midi_id][2]
    # if is not flat or sharp, then assume is natural
    #if accidental == '' or accidental == 'natural':
    kc = keyboard_mappings.get_key_color_from_midi(midi_id)
    if kc == 'white':
        return NOTES_POS[midi_id][0]
    elif kc == 'black':
        #assume that the note is a sharp
        return NOTES_POS[midi_id][2]
    #TODO raise an exception
    return None
