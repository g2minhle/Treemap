import pygame
import stdlib


class Control:

    def __init__(self, position, size):
        '''(Control, stdlib.Point, stdlib.Point) -> NoneType

        Construct a basic control structure

        self : the control
        position : the relative position of the control
        size : the size of the control
        '''

        # the absolute position of the control
        # user for drawing it on the screen
        self.abs_position = None
        self._text = None
        self.parent = None
        # the relative position of the control to its parent
        self.position = stdlib.Point(position.x, position.y)
        self.screen = None
        self.size = stdlib.Point(size.x, size.y)

    def calculate_real_position(self):
        '''(Control) -> tuple

        Return the absolute position of the control

        self : the control
        '''

        if not self.abs_position:
            # get the absolute position of the control's parent
            parent_pos = self.parent.calculate_real_position()
            self.abs_position = stdlib.Point(self.position.x + parent_pos.x, \
                                             self.position.y + parent_pos.y)
        x = self.abs_position.x
        y = self.abs_position.y
        return stdlib.Point(x, y)

    def dump_function(self, lst):
        '''(Object) -> NoneType

        Do nothing

        self : the control
        '''

        pass

    def draw(self):
        '''(Control) -> NoneType

        Draw the control

        self : the control
        '''

        # get the screen for drawing
        self.screen = self.parent.screen

    def mouse_event(self, event):
        '''(Control, pygame.Event) -> [function, list]

        Handle any mouse event on the control
        Return the right function(will be indicate later) for an event with
        its agurments in another list

        self : the control
        event : the event having information to handle
        '''

        return [self.dump_function, []]

    def key_event(self, event):
        '''(Control, pygame.Event) -> [function, list]

        Handle any key event on the control
        Return the right function(will be indicate later) for an event with its
        agurments in another list

        self : the control
        event : the event having information to handle
        '''

        return [self.dump_function, []]
