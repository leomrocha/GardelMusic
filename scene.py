# -*- encoding: utf-8 -*-

"""
Scene base class
Original version taken from: http://razonartificial.com/2010/08/gestionando-escenas-con-pygame/

"""
class Scene(object):
    """
    """

    def __init__(self, director):
        """
        """
        self.director = director
        self.dirty = True

    def on_update(self):
        """
        """
        raise NotImplemented("Must implement the method on_update.")

    def on_event(self, event):
        """
        """
        raise NotImplemented("Must implement the method on_event.")

    def on_draw(self, screen):
        """
        """
        raise NotImplemented("Must implement the method on_draw.")
        

