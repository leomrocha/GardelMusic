# -*- encoding: utf-8 -*-

import pygame

from scene import Scene


#TODO refactor the image elements for the play button to a button sprite object

class HomeScene(Scene):
    """Home Scene, the one where user can do things"""
    
    def __init__(self, director):
        Scene.__init__(self, director)
        #super(HomeScene, self).__init__(self, director)
        self.director = director
        self.screen = director.screen
        self.w, self.h = director.screen.get_size()

        #Start Image
        #TODO make sure that all the images are the same size (by code)
        self.play_normal = pygame.image.load("assets/images/icons/ic_play_circle_big_normal_o.png").convert_alpha()
        self.play_over = pygame.image.load("assets/images/icons/ic_play_circle_normal_o.png").convert_alpha()
        self.play_pressed = pygame.image.load("assets/images/icons/ic_play_circle_pressed_o.png").convert_alpha()
        #bx, by, bw,bh = rect = self.play_normal.get_rect() 
        
        bx, by, bw,bh = self.play_rect = self.play_normal.get_rect() 
        self.play_rect.x = self.w/2 - bw/2
        self.play_rect.y =  self.h/2 - bh/2
        
        self.current_play_button = self.play_normal
        
        #button state:
        self.play_state = "normal"
        #if screen is dirty
        self.dirty = True
                
       
    def on_update(self):
        if self.dirty:
            self.on_draw()
        self.dirty = False
        pass

    def on_event(self, event):
        #play_r = self.current_play_button.get_rect()
        #print "event handling"
        #print play_r
        #print self.play_rect
        #print pygame.mouse.get_pos()
        if self.play_rect.collidepoint(pygame.mouse.get_pos()):
            #print "mouse over"
            if self.play_state == "normal":
                self.current_play_button = self.play_over
                self.play_state = "over"
                self.dirty = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print "mouse button pressed"
                self.current_play_button = self.play_pressed
                self.play_state = "down"
                self.dirty = True
            if event.type == pygame.MOUSEBUTTONUP:
                #print "mouse button released"
                self.current_play_button = self.play_over
                self.dirty = True
                #TODO play pressed, go to the play screen!!
                #self.director.set_screen("play_menu")
                self.director.set_scene("play")
                
        elif self.play_state != "normal":
            self.current_play_button = self.play_normal
            self.dirty = True
        

    def on_draw(self, screen=None):
        if not screen:
            screen = self.screen
        if self.dirty:
            #print "drawing screen"
            self.screen.fill((120,200,230))
            bx, by, bw,bh = rect = self.play_normal.get_rect() 
            self.button_rect = (self.w/2 - bw/2, self.h/2 - bh/2)
            screen.blit(self.current_play_button, (self.w/2 - bw/2, self.h/2 - bh/2))
            self.dirty = False
