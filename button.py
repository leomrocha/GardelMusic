# -*- encoding: utf-8 -*-
"""
Implements a button class
"""

import os

import pygame


class ButtonStates(object):
    passive = "passive"
    hover = "hover"    
    pressed = "pressed"

class Button(pygame.sprite.Sprite):
    """
    Button
    
    """
    def __init__(self, screen, 
                       on_press_callback=None,
                       on_hover_callback=None,
                       on_release_callback=None,
                       size=(50,50), pos=(0,0), 
                       image_passive=os.path.join("assets","images","icons","ic_play_circle_big_normal_o.png"),
                       image_hover=os.path.join("assets","images","icons","ic_play_circle_normal_o.png"),
                       image_active=os.path.join("assets","images","icons","ic_play_circle_pressed_o.png"),
                       text=None):
        """
        screen
        on_press_callback= callback for on press,
        on_hover_callback= callback when hover,
        on_release_callback= callback when release,
        size=(50,50), pos=(0,0), 
        image_passive= image that will be shown on button passive
        image_hover= image that will be shown on button hover
        image_active= image that will be shown on button active
        text to display on top of the image: NOT IMPLEMENTED YET
        """
        self.screen = screen
        self.on_press_callback = on_press_callback
        self.on_hover_callback = on_hover_callback
        self.on_release_callback = on_release_callback
        self.pos = pos
        self.size = size

        #Start Image
        self.img_passive = pygame.image.load(image_passive).convert_alpha()
        self.img_hover = pygame.image.load(image_hover).convert_alpha()
        self.img_pressed = pygame.image.load(image_active).convert_alpha()
        
        self.img_passive = pygame.transform.scale(self.img_passive, size)
        self.img_hover = pygame.transform.scale(self.img_hover, size)
        self.img_pressed = pygame.transform.scale(self.img_pressed, size)
        
        self.rect = self.img_passive.get_rect() # use image extent values
        self.rect.topleft = pos
        
        self.current_button = self.img_passive
        
        #states
            
        #button state:
        self.current_state = ButtonStates.passive
        
        #if screen is dirty
        self.dirty = True
                
       
    def on_update(self):
        """
        """
        if self.dirty:
            self.on_draw()
        self.dirty = False
        pass

    def on_event(self, event):
        #print pygame.mouse.get_pos()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #print "mouse over"
            if self.current_state == ButtonStates.passive:
                self.current_button = self.img_hover
                self.current_state = ButtonStates.hover
                print "callback ?? ",self.on_hover_callback
                if self.on_hover_callback:
                    print "calling hover callback"
                    self.on_hover_callback()
                self.dirty = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print "mouse button pressed"
                self.current_button = self.img_pressed
                self.current_state = ButtonStates.pressed
                print "callback ?? ",self.on_press_callback
                if self.on_press_callback:
                    print "calling press callback"
                    self.on_press_callback()
                self.dirty = True
                
            elif event.type == pygame.MOUSEBUTTONUP:
                #print "mouse button released"
                self.current_button = self.img_passive
                print "callback ?? ",self.on_release_callback
                if self.on_release_callback:
                    print "calling release callback"
                    self.on_release_callback()
                self.dirty = True
                
        elif self.current_state != ButtonStates.passive:
            self.current_button = self.img_passive
            self.current_state = ButtonStates.passive
            self.dirty = True

    def on_draw(self, screen=None):
        if not screen:
            screen = self.screen
        if self.dirty:
            #print "drawing screen"
            screen.blit(self.current_button, self.pos)
            self.dirty = False

