# -*- coding: utf-8 -*-
"""
Keyboard Widget
"""
import os
import math
import pygame

import keyboard_mappings
from button import ButtonStates


#make this global so they don't load many times (has o
black_key_image = None
white_key_image = None

    
class KeyColorBar(pygame.sprite.Sprite):
    """shows a small upper bar with the representative synesthesia color"""
    def __init__(self, boss, synesthesia=(250,250,240), height=7):
        #pygame.sprite.Sprite.__init__(self,self.groups())  #is not working. I don't get it ...
        #pygame.sprite.Sprite.__init__(self)
        super(KeyColorBar, self).__init__()
        self.boss = boss
        
        self.image = pygame.Surface((self.boss.rect.width,height))
        self.image.set_colorkey((26,26,26)) # black transparent
        pygame.draw.rect(self.image, synesthesia, (0,0,self.boss.rect.width,height))
        self.rect = self.image.get_rect()
        self.rect.x = self.boss.rect.x
        self.rect.y = self.boss.rect.y - height
        #print "keycolorbar initialized: ", self.boss.midi_id, self.rect

    #def update(self):
    #    """
    #    """
    #    #nothing for the moment, later should update if the key is being played or not
    #    pass


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
        
        
        #print synesthesia
        self.rect = pygame.Rect(self.image.get_rect())
        #create and append the pressed image with the same size as the background image
        self.pressed_image = pygame.Surface([self.rect.width, self.rect.height], pygame.HWSURFACE, 32)
        self.pressed_image.set_alpha(255)
        self.pressed_image.fill(self.synesthesia)
        
        self.images.append(self.pressed_image)

        #current image index
        self.image_index = 0
        #start showing the passive image
        self.image = self.images[self.image_index]
        
        #update key position
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
        #key state # from ButtonStates ('rest' | 'pressed')
        self.state = ButtonStates.passive
        self.dirty = True
        
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
        
        
    def on_note_on(self, velocity=128):
        """
        Key activation
        """
        #print "note on id: %d with velocity: %d" %(self.midi_id, velocity)
        #draw the colored overlay
        self.state = ButtonStates.pressed
        self.image_index = 1
        #make only a few ranges in velocity transparency, this helps visualization
        #Note, max velocity = 128, but alpha is 255, so do a transformation, also do it for a few values...
        #use 127 as base number to have a minimum nice base solor, eliminate all non-int part
        #velocity = 63 + int(math.ceil((vel) / 8.)) * 12 # this makes 12 ranges of transparency
        vel = 63 + int(math.ceil((velocity) / 4.)) * 6 # this makes 6 ranges of transparency
        #print "velocity = ", vel
        self.pressed_image.set_alpha(vel)
        #print velocity
        #self.pressed_image.fill(self.synesthesia)
        #TODO WARNING, see how this should be updated ... not sure if here
        self.dirty = True
        self.on_update()
        
    def on_note_off(self):
        """
        """
        self.state = ButtonStates.passive
        self.image_index = 0
        #TODO WARNING, see how this should be updated ... not sure if here
        self.dirty = True
        self.on_update()
        
        
    def on_update(self):
        """
        """
        if self.dirty:
            #print "calling on_update", self.image_index
            self.image = self.images[self.image_index]
            self.dirty = False
        
        
    def on_event(self, event=None):
        """
        """
        #activate on key events
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #print "mouse_pressed = ", pygame.mouse.get_pressed(), event
            #print "mouse over"
            #press key if any mouse button is pressed
            #if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == ButtonStates.passive and 1 in pygame.mouse.get_pressed():
                #print "mouse button pressed"
                self.on_key_press()
            elif self.state == ButtonStates.pressed and  event.type == pygame.MOUSEBUTTONUP:
                #print "mouse button released"
                self.on_key_release()
            self.on_update()
        #FIXME TODO-> this following check causes the flickering on mouse move when the key is 
        # activated through MIDI signal!!!!!!!! -> find out how to solve it
        #mouse is gone from the key 
        elif self.state == ButtonStates.pressed:
            self.on_key_release()
            self.on_update()
        
    def on_draw(self):
        """
        """
        pass
        
class Keyboard(object):
    """
    Complete keyboard implementation
    """
    #TODO some nice thingies for the keys :
    #   - sustain pedals
    #   - top rect with synesthesia for each key
    #   - finger number and hand indication, localized (i18n) example: right1 = r1 , left2 = l2; gauche1 = g1, droite3 = d3
    #   - central Do mark (a red dot below the key will be nice for example)
    def __init__(self, screen, midi_pubsub, pos=(0,0), width=1060):
        """
        screen: the parent screen
        midi_pubsub
        pos 
        width 
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
        self.white_keys_colorbar_group = pygame.sprite.Group()
        
        self.black_keys_group = pygame.sprite.Group()
        self.black_keys_colorbar_group = pygame.sprite.Group()
        
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
        velocity = event.data2
        index = note - self.KEY_RANGE[0]
        key = self.keys[index]
        key.on_note_on(velocity)
        
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
        cb_height = int(0.04 * kb_height)
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
            
            cb = KeyColorBar(ks, k['synesthesia'], cb_height)
            if k['color'] == 'black':
                self.black_keys_group.add(ks)
                self.black_keys_colorbar_group.add(cb)
            else:
                self.white_keys_group.add(ks)
                self.white_keys_colorbar_group.add(cb)
                #background

        #General background of all the keyboard
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.Surface((kb_width, kb_height))
        self.background.image.fill((26,26,26))     # fill black
        #self.background.image.fill((250,250,250))     # fill white ->should make a white background behind the keys for the transparency to work well, but black behind it to fill the borders in black
        self.background.rect = self.background.image.get_rect()
        self.background.rect.x = pos[0]
        self.background.rect.y = pos[1]
        self.rect = self.background.rect
        self.allgroups.add(self.background)
        #background of the keys (to be able to handle transparency correctly
        self.kb_background = pygame.sprite.Sprite()
        self.kb_background.image = pygame.Surface((kb_width - padding['left'] - padding['right'],kb_height - padding['top'] - padding['bottom']))
        #self.kb_background.fill((26,26,26))     # fill black
        self.kb_background.image.fill((230,230,240))     # fill white
        self.kb_background.rect = self.kb_background.image.get_rect()
        self.kb_background.rect.x = pos[0] + padding['left']
        self.kb_background.rect.y = pos[1] + padding['top']
        self.allgroups.add(self.kb_background)
    
    def on_update(self):
        #super(Keyboard, self).update()
        pass
    
    def on_draw(self, screen):
        self.allgroups.clear(screen, self.background.image)
        self.allgroups.update()
        self.allgroups.draw(screen)

        #display
        
        
        #keys
        #self.white_keys_group.clear(screen, self.kb_background)
        self.white_keys_group.update()
        self.white_keys_group.draw(screen)

        self.white_keys_colorbar_group.update()
        self.white_keys_colorbar_group.draw(screen)
        
        
        #self.black_keys_group.clear(screen, self.kb_background)
        self.black_keys_group.update()
        self.black_keys_group.draw(screen)
        self.black_keys_colorbar_group.update()
        self.black_keys_colorbar_group.draw(screen)
        #self.allkeys.draw(screen)
        #self.allgroups.draw(screen)
        pass
        
    def on_event(self, event):
    
        #check if it touches the keyboard at least
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #print "collides event: ", event
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

