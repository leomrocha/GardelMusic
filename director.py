# -*- encoding: utf-8 -*-

"""
Game Director class for handling Scenes and Scene class
Original version taken from: http://razonartificial.com/2010/08/gestionando-escenas-con-pygame/

Modifications according to need
"""

import pygame
import sys

####
#import all the scenes
import home_scene
import play_scene
####

###Setup screen size automagically
import pygame.display

class Director:
    """Representa el objeto principal del juego.

    El objeto Director mantiene en funcionamiento el juego, se
    encarga de actualizar, dibuja y propagar eventos.

    Tiene que utilizar este objeto en conjunto con objetos
    derivados de Scene."""
    scene_width, scene_height = None, None

    screen = None
    #dictionary containing all the scenes
    scenes = {}
    
    
    def __init__(self, start_scene="home_scene"):

        #Setup video system
        display_info = pygame.display.Info()
        self.scene_width, self.scene_height = display_info.current_w, display_info.current_h

        #self.screen = pygame.display.set_mode((self.scene_width, self.scene_height))
        self.screen = pygame.display.set_mode((self.scene_width * 9/10, self.scene_height * 9/10))

        #self.screen = pygame.display.set_mode((1600, 900), RESIZABLE)
        #self.screen = pygame.display.set_mode((1600, 900))



        pygame.display.set_caption("Piano Challenge")

        clock = pygame.time.Clock() # create a clock object for timing
        self.start_scene = start_scene
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        
        self.setup_scenes()
        
    def setup_scenes(self):
        """
        setups the main scenes that might be needed, at least the start one
        """
        #Home scene
        self.scenes["home_scene"] = home_scene.HomeScene(self)
        #Settings
        
        #Game Menu
        
        #play scene
        self.scenes["play"] = play_scene.PlayScene(self)
        #Set start screen
        self.set_scene(self.start_scene)

    def display_fps(self):
        #TODO refactor and create a widget that does this and can be added by a configuration variable
        """
        FPS display
        """
        #TODO add timer for updating only ever X ms and not in every frame
        font=pygame.font.Font(None,20)
        try:
            self.fps_txt.fill((255,255,240))
            self.screen.blit(self.fps_txt, (10, 10))
        except:
            pass
        self.fps_txt=font.render("FPS:"+str(int(self.clock.get_fps())), 1,(100,100,100))
        
        self.screen.blit(self.fps_txt, (10, 10))

    def loop(self):
        "Pone en funcionamiento el juego."

        while not self.quit_flag:
            time = self.clock.tick(100)
            
            # Eventos de Salida
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
			            self.quit()
	            #scene event handling (has to be here because loop over events empties the queue
                self.scene.on_event(event)
            # detecta eventos
            #self.scene.on_event()

            # actualiza la escena
            self.scene.on_update()

            # dibuja la pantalla
            #self.scene.on_draw(self.screen)
            self.scene.on_draw()
            
            self.display_fps()
            pygame.display.flip()

    def _set_scene(self, scene):
        "Changes the current scene to the one given by OBJECT"
        #print "setting scene"
        self.scene = scene
        #marks the scene as dirty for the scene to force the update
        self.scene.dirty = True

    def set_scene(self, scene_name):
        """
        sets the new scene to the given name
        """
        if scene_name in self.scenes:
            #print scene_name, self.scenes[scene_name]
            self._set_scene(self.scenes[scene_name])
        else:
            ##TODO make a log here
            print "Scene '%s' not found, could not be changed" % scene_name

    def quit(self):
        self.quit_flag = True


