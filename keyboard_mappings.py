# -*- coding: utf-8 -*-
"""
This module is dedicated to create the numeric representation of the keyboard in a dict with the params

midi_id, 
name id (number), 
color(white|black) ,
associated synesthesia color id, 
pos (x, y)
size (width, height)

"""

import synesthesia

#Key codes associated with the note name

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

white_key_codes = [0,2,4,5,7,9,11]
black_key_codes = [1,3,6,8,10]


def get_octave(midi_id):
    return int(midi_id / 12)


def get_key_id(midi_id):
    return midi_id%12


def get_note_name(midi_id, lang='latin'):
    if lang == 'english':
        return NAMES_ENGLISH[midi_id]
    elif lang == 'german':
        return NAMES_GERMAN[midi_id]
    #by default asume note names are in latin
    return NAMES_LATIN[midi_id]


def get_key_color(key_code):
    """
    gets the key color (white/black) according to the key code in the octave
    """
    if key_code in black_key_codes:
        return 'black'
    return 'white'


def get_key_color_from_midi(midi_id):
    """
    gets the key color (white/black) according to the midi_id 
    """
    kc = midi_id  % 12
    return get_key_color(kc)
    
    
#padding is from where the keyboard starts in pixels in the plain_keyboard.svg file
#all other numbers can be calculated according to these figures
ref_keyboard_padding = {
    'left': 10,
    'right': 10,
    'top': 12.5,
    'bottom': 7.5,
    'bottom_black': 47.5,
}


#key size, IDEM previous dict, size are in pixels in plain_keybord.svg file
#all key proportions be calculated according to these figures
ref_key_size = {
    'white': (20,100),
    'black': (15,60),
}


##Reference keyboard size
ref_width = 1060
ref_height = 120

keyboard_range=(21,95)

#current_mappings = {}
def get_height(width):
    return ref_height * width / ref_width
    
#def generate_keyboard_map(key_range=(21,95), synesthesia_colors=synesthesia.current_colors, width=1060, height=120, padding=(10,10,12.5,7.5)):
#def generate_keyboard_map(key_range=(21,95), synesthesia_colors=synesthesia.current_colors, width=1060, height=120):
def generate_keyboard_map(key_range=(21,95), synesthesia_colors=synesthesia.current_colors, width=1060, max_height=300):
    """
    
    generates the keyboard map 
    
    Al size recalculations are done based on the given width and are proportional to the base image
    
    key_range = (initial, end) -- WARNING, the first and last key MUST be white or the generation WILL FAIL
    synesthesia_colors = array with RGB colors of every midi_id
    width = of the keyboard
    max_height  -> height is the MAX height that will be allowed on the keyboard
    ##padding = (left, right, top, bottom)   -> not implemented yet
    
    WARNING
    given positions are RELATIVE to the bottom left corner, to correctly possition them on screen 
    
    
    returns: 
        ret = {
        'keyboard_map': keyboard_map,
        'padding': {left, right, top, bottom, bottom_black }, 
        'size': (w,h)
        'key_size': {'white':(w,h), 'black':(w,h), }
    }
    Where keyboard_map is an array containing secuentially all the informations about all the keys in the keyboard:
         {
            'midi_id': i,
            'key_id': 0-11,
            'octave': Number,
            'color': white|black,
            'synesthesia': color in the synesthesia scheme
            'pos': position relative to the bottom left corner
            'size': size of the key
        }
        and information about this keyboard
    """
    keyboard_map = []
    
    #size recalculation
    
    #TODO verify that the first and last keys are white or change it by force (eliminate)
        
    
    height = get_height(width)
    padding_left = ref_keyboard_padding['left'] * width / ref_width
    padding_right = ref_keyboard_padding['right'] * width / ref_width
    padding_top = ref_keyboard_padding['top'] * width / ref_width
    padding_bottom = ref_keyboard_padding['bottom'] * width / ref_width
    padding_bottom_black = ref_keyboard_padding['bottom_black'] * width / ref_width
    
    avail_w = width - padding_left - padding_right  #available width
    avail_h = height - padding_top - padding_bottom  #available height
    
    #keys size recalculations:
    #need to count white keys
    total_whites = 0
    total_blacks = 0
    #this is not so efficient as we do it twice
    for i in range(key_range[0],key_range[1]+1):
        if get_key_color(i%12) == 'white':
            total_whites +=1
        else:
            total_blacks +=1
    
    #key size by color
    white_width = avail_w / total_whites
    white_height = ref_key_size['white'][1] * white_width / ref_key_size['white'][0]
    #cap height
    #print white_height, height, max_height
    #print avail_w
    #print total_whites, total_blacks
    white_height = min(white_height, max_height)
    white_dim = (white_width, white_height)
    
    black_width = white_width * 3 / 4
    black_height = ref_key_size['black'][1] * black_width/ ref_key_size['black'][0]
    #cap height
    black_height = min(black_height, max_height)
    black_dim = (black_width, black_height)
    
    #keep track of the state of things to be able to create a nice keybard
    
    #count_whites = 0
    #count_blacks = 0
    #assume we start from a white key
    last_key_pos = (padding_left - white_width,0)
    
    for i in range(key_range[0],key_range[1]+1):
        
        key_color = get_key_color(i%12)
        if key_color == 'black':
            x = last_key_pos[0] + white_width - black_width/2
            y = padding_bottom_black
        else:
            x = last_key_pos[0] + white_width
            y = padding_bottom
            
        pos = (x,y)
        
        dim = white_dim
        if key_color == 'black':
            dim = black_dim
        else:
            last_key_pos = pos
        key = {
                'midi_id': i,
                'key_id': get_key_id(i),
                'octave': get_octave(i),
                'color': key_color,
                'synesthesia': synesthesia_colors[i],
                'pos': pos,
                'size': dim
            }
        
        
        keyboard_map.append(key)
    
    #now create all the other reference dimension containers to return:
        
    padding = {
        'left': padding_left,
        'right': padding_right,
        'top': padding_top,
        'bottom': padding_bottom,
        'bottom_black': padding_bottom_black,
        }
    size = (width, height)
    key_size = {
        'white': (white_width, white_height),
        'black': (black_width, black_height),
    }
    
    #print keyboard_map
    #print size
    #print key_size
    #print padding
    
    ret = {
        'keyboard_map': keyboard_map,
        'padding': padding,
        'size': size,
        'key_size': key_size
    }
    #current_mappings = ret
    return ret
    
def get_key_at(pos):
    """
    returns the midi_id of the key at the given position (intersection)
    this function is to avoid checking for a click event to all the keys 
    """
    #TODO
    pass
        
