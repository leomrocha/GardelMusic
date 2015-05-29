# -*- encoding: utf-8 -*-
"""
Controls, for game play
"""

import pygame
from button import *

################################################################################
#Abstract Menus
################################################################################

class AbstractMenu(object):
    """
    """
    #TODO
    pass


class ToggleMenu(AbstractMenu):
    """
    """
    #TODO
    pass
################################################################################
#Playback Control Bar
################################################################################
    
class PlaybackControlBar(object):
    """
    """
    def __init__(self, screen, pos, size, on_backwards_callback=None, on_play_toggle_callback=None, on_stop_callback=None, on_forward_callback=None):
        """
        screen,
        pos, 
        size, 
        on_play_toggle_callback, (acts as play/pause button)
        on_stop_callback, 
        on_forward_callback, 
        on_backwards_callback
        """
        #
        self.screen = screen
        self.pos = pos
        self.size = size
        #calculate button size:
        bh = size[1]
        bw = min( size[0] / 4, bh)
        bsize = (bw,bh)
        #gruops
        self.bkg_group = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()
        #here the background
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.Surface(size)
        self.background.image.fill((61,61,61))     # fill black
        #self.background.image.fill((250,250,250))     # fill white ->should make a white background behind the keys for the transparency to work well, but black behind it to fill the borders in black
        self.background.rect = self.background.image.get_rect()
        self.background.rect.x = pos[0]
        self.background.rect.y = pos[1]
        self.rect = self.background.rect
        self.bkg_group.add(self.background)
        #here the buttons
        self.back = Button(
                            self.screen, 
                            on_release_callback=on_backwards_callback,
                            size=bsize, 
                            pos=(pos[0], pos[1]),
                            image_passive=os.path.join("assets","images","icons","ic_backward_circle_big_normal_o.png"),
                            image_hover=os.path.join("assets","images","icons","ic_backward_circle_big_normal_o.png"),
                            image_active=os.path.join("assets","images","icons","ic_backward_circle_big_pressed_o.png"),
                            )
        self.play_pause = ToggleButton(
                            self.screen, 
                            on_toggle_callback=on_play_toggle_callback,
                            size=bsize, 
                            pos=(pos[0] + bw, pos[1]),
                            image_passive=os.path.join("assets","images","icons","ic_play_circle_big_normal_o.png"),
                            image_active=os.path.join("assets","images","icons","ic_pause_circle_big_normal_o.png"),
                            )
        self.stop = Button(
                            self.screen, 
                            on_release_callback=on_stop_callback,
                            size=bsize, 
                            pos=(pos[0] + 2 * bw, pos[1]),
                            image_passive=os.path.join("assets","images","icons","ic_stop_circle_normal_w.png"),
                            image_hover=os.path.join("assets","images","icons","ic_stop_circle_normal_w.png"),
                            image_active=os.path.join("assets","images","icons","ic_stop_circle_pressed_w.png"),
                            )

        self.forward = Button(
                            self.screen, 
                            on_release_callback=on_forward_callback,
                            size=bsize, 
                            pos=(pos[0] + 3* bw, pos[1]),
                            image_passive=os.path.join("assets","images","icons","ic_forward_circle_big_normal_o.png"),
                            image_hover=os.path.join("assets","images","icons","ic_forward_circle_big_normal_o.png"),
                            image_active=os.path.join("assets","images","icons","ic_forward_circle_big_pressed_o.png"),
                            )
        
        self.button_group.add(self.back)
        self.button_group.add(self.play_pause)
        self.button_group.add(self.stop)
        self.button_group.add(self.forward)
        
        self.playing = False
        self.dirty = True

    def on_draw(self, screen=None):
        """
        """
        #self.white_keys_group.clear(screen, self.kb_background)
        if screen is None:
            screen = self.screen

        self.bkg_group.draw(screen)

        self.button_group.draw(screen)

    def on_event(self, event):
        """
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #print "called on_event control at: ", time.clock()
            #print "group: ", self.button_group
            #print "sprites: ", self.button_group.sprites
            #print "sprites dict: ", self.button_group.spritedict
            #for b in self.button_group.sprites():
            for b in self.button_group.sprites():
                b.on_event(event)
        pass
    
    def on_update(self):
        """
        """
        self.bkg_group.update()
        self.button_group.update()
        #for b in self.button_group:
        #    b.on_update()
        pass
################################################################################
#Display Selection
################################################################################
class DisplaySelect(ToggleMenu):
    """
    Contains the buttons fo rdisplay selection
    """
    def __init__(self, screen, size, pos, on_display_select_callback, display_list):
        """
        size
        pos
        on_display_select_callback = callback to call when display is selected
        display_list = [ {'display_name': ,
                          'img_active': path,
                          'img_hover': path
                          'img_passive':path
                          },
                          ...
                        ]
        """
        #TODO
        pass
        

class DefaultDisplaySelect(DisplaySelect):
    """
    A default display selection tool that contains 3 types of displays:
    Vertical
    Horizontal
    Pseudo Sheet Music (sheet but with rectangles)
    """
    
    def __init__(self, screen, size, pos, on_display_select_callback):
        """
        """
        display_list = [
                    #TODO complete this
                    ]
        super(DefaultDisplaySelect, self).__init__(screen,size, pos, on_display_select_callback, display_list)
        
################################################################################
#Instrument Selection
################################################################################


