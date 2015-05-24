# -*- encoding: utf-8 -*-

import pygame

from scene import Scene


class HomeScene(Scene):
    """Escena inicial del juego, esta es la primera que se carga cuando inicia"""
    
    def __init__(self, director):
        Scene.__init__(self, director)
        #super(HomeScene, self).__init__(self, director)
        self.director = director
        self.screen = director.screen
        self.w, self.h = director.screen.get_size()

        #Start Image
        self.play_normal = pygame.image.load("assets/images/icons/ic_play_circle_normal_o.png").convert_alpha()
        self.play_pressed = pygame.image.load("assets/images/icons/ic_play_circle_pressed_o.png").convert_alpha()
        #bx, by, bw,bh = rect = self.play_normal.get_rect() 
        
        self.current_play_button = self.play_normal
        
        #if screen is dirty
        self.dirty = True
                
       
    def on_update(self):
        if self.dirty:
            self.on_draw()
        self.dirty = False
        pass

    def on_event(self, event):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #TODO check that the click collides with the button
                self.current_play_button = self.play_pressed
                self.dirty = True
            if event.type == pygame.MOUSEBUTTONUP:
                #TODO check that the click collides with the button
                self.current_play_button = self.play_normal
                self.dirty = True
            

    def on_draw(self, screen):
        if self.dirty:
            self.screen.fill((120,200,230))
            bx, by, bw,bh = rect = self.play_normal.get_rect() 
            self.screen.blit(self.current_play_button, (self.w/2 - bw/2, self.h/2 - bh/2))
            self.dirty = False
