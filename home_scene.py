# -*- encoding: utf-8 -*-
import os

import pygame

from scene import Scene
from button import Button

#TODO refactor the image elements for the play button to a button sprite object

class HomeScene(Scene):
    """Home Scene, the one where user can do things"""
    
    def __init__(self, director):
        Scene.__init__(self, director)
        #super(HomeScene, self).__init__(self, director)
        self.director = director
        self.screen = director.screen
        self.w, self.h = director.screen.get_size()

        self.menu_group = pygame.sprite.Group()
        
        self.play_button = Button(
                                self.screen, 
                                on_press_callback=self.on_button_press,
                                on_hover_callback=self.on_button_hover,
                                on_release_callback=self.on_button_release,
                                size=(250,250), 
                                pos=(self.w/2 - 125, self.h/4 - 125),
                                image_passive=os.path.join("assets","images","icons","ic_play_circle_big_normal_o.png"),
                                image_hover=os.path.join("assets","images","icons","ic_play_circle_normal_o.png"),
                                image_active=os.path.join("assets","images","icons","ic_play_circle_pressed_o.png"),
                                )
                                
        self.follow_button = Button(
                                self.screen, 
                                on_press_callback=self.on_follow_press,
                                on_hover_callback=self.on_follow_hover,
                                on_release_callback=self.on_follow_release,
                                size=(250,250), 
                                pos=(self.w/2 - 125, self.h*3/4 - 125),
                                image_passive=os.path.join("assets","images","icons","ic_light_orange_circle_big_normal_o.png"),
                                image_hover=os.path.join("assets","images","icons","ic_light_green_circle_big_normal_o.png"),
                                image_active=os.path.join("assets","images","icons","ic_light_green_circle_big_normal_o.png"),
                                )
                                
        self.menu_group.add(self.play_button)
        self.menu_group.add(self.follow_button)
        self.dirty = True

    def on_follow_press(self):
        #print "button press follow called"
        self.dirty = True
        
    def on_follow_hover(self):
        #print "button hover follow called"
        self.dirty = True
        
    def on_follow_release(self):
        #print "button release follow called"
        self.director.set_scene("follow")
        
    def on_button_press(self):
        #print "button press called"
        self.dirty = True
        
    def on_button_hover(self):
        #print "button hover called"
        self.dirty = True
        
    def on_button_release(self):
        #print "button release called"
        self.director.set_scene("play")
        
    def on_update(self):
        """
        """
        self.menu_group.update()
        #self.play_button.on_update()
        if self.dirty:
            self.on_draw()
        self.dirty = False
        pass

    def on_event(self, event):
        """
        """
        self.play_button.on_event(event)
        self.follow_button.on_event(event)
        

    def on_draw(self, screen=None):
        """
        """
        
        if not screen:
            screen = self.screen
        if self.dirty:
            #print "drawing screen"
            #self.screen.fill((120,200,230))
            self.screen.fill((255, 255, 240))
            #self.play_button.dirty = True
            #self.play_button.on_draw(screen)
            self.menu_group.draw(self.screen)
            self.dirty = False

