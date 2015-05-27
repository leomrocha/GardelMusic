# -*- coding: utf-8 -*-
"""
Keyboard Widget
"""
import os
import pygame

import keyboard_mappings
from button import ButtonStates


#make this global so they don't load many times (has o
black_key_image = None
white_key_image = None


class KeySprite(pygame.sprite.DirtySprite):
    """
    Key sprite that
    """
    #TODO inherit from button.Button instead
    def __init__(self, midi_id, pos, size, color, midi_publish, synesthesia=(100,100,100)):
        """
        midi_id = midi_id of the represented key
        pos = position
        size = size of the key
        color = [white|black]
        midi_publish = function for midi pubsub call to publish a midi event
        synesthesia = the color that the key takes when activated. By default a shade of grey
        
        """
        
        #WARNING AWFUL
        #this is here to load for the first time the images as the display MUST be initialized
        try:
            if black_key_image is None or white_key_image is None:
                black_key_image = pygame.image.load(os.path.join("assets","images","keyboard","black_key.png")).convert_alpha()
                white_key_image = pygame.image.load(os.path.join("assets","images","keyboard","white_key.png")).convert_alpha()
        except:
            black_key_image = pygame.image.load(os.path.join("assets","images","keyboard","black_key.png")).convert_alpha()
            white_key_image = pygame.image.load(os.path.join("assets","images","keyboard","white_key.png")).convert_alpha()
        ##END awful
        
        super(KeySprite, self).__init__()
        
        self.images = []
        
        self.midi_id = midi_id
        self.key_id = midi_id  % 12
        self.octave = midi_id / 12
        self.key_color = color
        self.pos = pos
        self.size = size
        #self.name = name
        self.synesthesia = synesthesia
        
        ####MIDI function that allows publishing midi events
        self.midi_publish = midi_publish
        
        #if key is black
        if color == 'black':
            self.image = black_key_image = pygame.transform.scale(black_key_image, size)
        else:
            self.image = white_key_image = pygame.transform.scale(white_key_image, size)
        
        #append rest image        
        self.images.append(self.image)
        
        #current image index
        self.image_index = 0
        
        #print synesthesia
        
        
        self.rect = pygame.Rect(self.image.get_rect())
        #create and append the pressed image with the same size as the background image
        self.pressed_image = pygame.Surface([self.rect.width, self.rect.height])
        self.pressed_image.fill(self.synesthesia)
        
        self.images.append(self.pressed_image)
        
        #update key position
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
        #key state # from ButtonStates ('rest' | 'pressed')
        self.state = ButtonStates.passive
        
    def on_key_press(self):
        """
        when the key is pressed by the user on the screen
        """
        #TODO emit note on midi event
        self.midi_publish("note_on", self.midi_id)
        self.on_note_on()
        
    def on_key_release(self):
        """
        when the key is pressed by the user on the screen
        """
        self.midi_publish("note_off", self.midi_id)
        self.on_note_off()
        
    def on_note_on(self, finger=0):
        """
        Key activation
        """
        #draw the colored overlay
        
        #if finger >=1 && <=5 also overlay the finger id on the key
        self.state = ButtonStates.pressed
        self.image_index = 1
        #TODO WARNING, see how this should be updated ... not sure if here
        self.on_update()
        
    def on_note_off(self):
        """
        """
        self.state = ButtonStates.passive
        self.image_index = 0
        #TODO WARNING, see how this should be updated ... not sure if here
        self.on_update()
        
    def on_update(self):
        """
        """
        #print "calling on_update", self.image_index
        self.image = self.images[self.image_index]
        
        
    def on_event(self, event=None):
        """
        """
        #activate on key events
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #mouse_pressed = pygame.mouse.get_pressed()
            #print "mouse_pressed = ", mouse_pressed
            #print "mouse over"
            #press key if any mouse button is pressed
            #if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == ButtonStates.passive and 1 in pygame.mouse.get_pressed():
                #print "mouse button pressed"
                self.on_key_press()
            elif self.state == ButtonStates.pressed and  event.type == pygame.MOUSEBUTTONUP:
                #print "mouse button released"
                self.on_key_release()
        #mouse is gone from the key
        elif self.state == ButtonStates.pressed:
            self.on_key_release()
        
        self.on_update()
        
    def on_draw(self):
        """
        """
        pass
        

class KeyGroup(pygame.sprite.Group):
    """
    Contains the key and other elements for the interactivity
    """
    #TODO
    pass


class KeyboardSprite(pygame.sprite.Sprite):
    """
    Piano Keyboard Sprite basic romo an image, no behaviour is handled
    """
    
    def __init__(self, pos=(0,0)):
        """
        """
        #Super constructor
        #super().__init__()
        super(KeyboardSprite, self).__init__()
        #pygame.sprite.Sprite.__init__(self)
        #

        #Keyboard Image        
        self.image = pygame.image.load("assets/images/keyboard/plain_keyboard.png").convert_alpha()
        self.rect = self.image.get_rect() # use image extent values
        self.rect.topleft = pos
        
    def update(self):
        """
        """
        #print "updating keyboard sprite"
        super(KeyboardSprite, self).update()
        pass
        
    def collides_key(self, pos):
        """
        Calculates the key in the keyboard that is touched by the event position
        returns:
        midi_note (pygame event notation??? TODO decide)
        bounding box (x,y,w,h) of the element
        
        """
        #TODO
        #1 see if collides with the keyboard, else return false
        #2 if so, see what note (white) it collides, calculate also the rect containing the white note (this should be pre-calculated somewhere to make it faster)
        
        #3 if height < Ybk0 return true and note that it collides (midi notation) #Ybk0 == lower Y position of black key counted from the bottom
        
        #4 if heignt >Ybk0 see if it collides with which note (the flat or the sharp ...
        
        #5 return the nothe that it collides with, position, bounding box and midi notation
        
        pass
        

class Keyboard(object):
    """
    Complete keyboard implementation
    """
    #TODO some nice thingies for the keys :
    #   - sustain pedals
    #   - top rect with synesthesia for each key
    #   - finger number and hand indication, localized (i18n) example: right1 = r1 , left2 = l2; gauche1 = g1, droite3 = d3
    def __init__(self, screen, midi_pubsub, pos=(0,0), width=1060):
        """
        """
        self.KEY_RANGE = (21,108)
        
        self.screen  = screen
        
        #setup midi handling
        self.midi_pubsub=midi_pubsub
        
        midi_pubsub.subscribe("note_on", self.on_note_on)
        midi_pubsub.subscribe("note_off", self.on_note_off)
        midi_pubsub.subscribe("sustain", self.on_sustain)
        
        
        ###end MIDI
        #self.screen.blit(self.background, pos)
        
        #define sprite groups
        
        self.white_keys_group = pygame.sprite.Group()
        self.black_keys_group = pygame.sprite.Group()
        # LayeredUpdates instead of group to draw in correct order
        self.allgroups = pygame.sprite.Group()
        
        #KeySprite.groups = self.allkeys, self.allgroups
        KeySprite.groups = self.allgroups
        self.keys = []
        self.active_keys = [] # keep track of the currently active keys
        self._setup_keys(pos, width)
        
    def on_note_on(self, event):
        """
        """
        #print "note on received: ", event
        note = event.data1
        index = note - self.KEY_RANGE[0]
        key = self.keys[index]
        key.on_note_on()
        
    def on_note_off(self, event):
        """
        """
        #print "note off received: ", event
        note = event.data1
        index = note - self.KEY_RANGE[0]
        key = self.keys[index]
        key.on_note_off()

    def on_sustain(self, event):
        """
        """
        #TODO
        #print "sustain event received ", event
        pass
        
    #def publish_midi_event(self, event, midi_id, velocity=127):
    #    """
    #    """
    #    self.midi_pubsub.publish(event, midi_id, velocity)

    def _setup_keys(self, pos, width):
        """
        """
        #obtain 
        self.keyboard_map = keyboard_mappings.generate_keyboard_map(key_range=self.KEY_RANGE,width=width)
        key_map = self.keyboard_map['keyboard_map']
        kb_width, kb_height = self.keyboard_map['size']
        padding = self.keyboard_map['padding']
        self.kb_background = pygame.Surface((kb_width, kb_height))
        self.kb_background.fill((26,26,26))     # fill white
        self.kb_background = self.kb_background.convert()  # jpg can not have transparency
        
        self.keys = []
        
        for k in key_map:
        
            key_pos = k['pos']
            key_size = k['size']
            #key_pos = (pos[0] + key_pos[0], pos[1] - kb_height )
            #key_pos = (pos[0] + key_pos[0], pos[1] + key_pos[1])
            key_pos = (pos[0] + key_pos[0], pos[1] + padding['top'])
            
            key_color = k['color']
            
            ks = KeySprite(midi_id=k['midi_id'], pos=key_pos , size=key_size , 
                           color=key_color , midi_publish = self.midi_pubsub.publish,
                           synesthesia=k['synesthesia'] )
            self.keys.append(ks)
            if k['color'] == 'black':
                self.black_keys_group.add(ks)
            else:
                self.white_keys_group.add(ks)
                #background

        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.Surface((kb_width, kb_height))
        self.background.image.fill((26,26,26))     # fill white
        self.background.rect = self.background.image.get_rect()
        self.background.rect.x = pos[0]
        self.background.rect.y = pos[1]
        self.allgroups.add(self.background)
        
    
    def on_update(self):
        #super(Keyboard, self).update()
        pass
    
    def on_draw(self, screen):
        self.allgroups.clear(screen, self.background.image)
        self.allgroups.update()
        self.allgroups.draw(screen)

        #display
        
        
        #keys
        self.white_keys_group.clear(screen, self.kb_background)
        self.white_keys_group.update()
        self.white_keys_group.draw(screen)
        
        self.black_keys_group.clear(screen, self.kb_background)
        self.black_keys_group.update()
        self.black_keys_group.draw(screen)
        #self.allkeys.draw(screen)
        #self.allgroups.draw(screen)
        pass
        
    def on_event(self, event):
    
        #TODO make this efficient
        collitions = []
        for k in self.keys:
            if k.rect.collidepoint(pygame.mouse.get_pos()):
                collitions.append(k)
        #there should be only 2 collitions max (one white and one black)
        assert(len(collitions) >=0 and len(collitions) <=2)
        #update state of active keys - this fixes the problem on hover out while mouse button pressed
        for k in self.active_keys:
            k.on_event(event)
            #eliminate keys that have been deactivated from the active_keys
            if k.state == ButtonStates.passive:
                self.active_keys.remove(k)
        #if more than one collition, only activate the black key
        if len(collitions) > 1:
            for k in collitions:
                if k.key_color == 'black':
                    k.on_event(event)
                    #keep track of pressed keys
                    if k.state == ButtonStates.pressed:
                        self.active_keys.append(k)
        else:
            for k in collitions:
                k.on_event(event)
                if k.state == ButtonStates.pressed:
                    self.active_keys.append(k)
        
    def on_mouse_down(self, pos):
        """
        """
        pass
    
    def on_mouse_up(self, pos):
        """
        """
        pass
        
    #MIDI events
    #TODO on key on
    #TODO on key off

