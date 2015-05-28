# -*- encoding: utf-8 -*-
"""
Controls, for game play
"""

from button import ToggleButton

################################################################################
#Abstract Menu
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



