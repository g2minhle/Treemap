import control
import stdlib
import label
import pygame


class Button(control.Control):

    def __init__(self, \
                 position, \
                 text = "", \
                 size = stdlib.STANDARD_BUTTON_SIZE, \
                 background_color = stdlib.STANDARD_GRAY_BUTTON, \
                 is_label = True, \
                 is_border = True, \
                 is_soiled = True,
                 border_size = 3):
        '''(Button, stdlib.Point, string
        [, stdlib.Point, tuple, boolean, boolean, boolean, int] ) -> NoneType

        Construct the button

        self : the button
        position : the relative position of the button
        size : the size of the button
        background_color : the background
        is_label : if the button will be labeld
        Is_border : if the button has border
        is_soiled : if the button is soiled
        border_size : the size of the border
        '''

        control.Control.__init__(self, position, size)
        self.background_color = background_color
        self.current_color = background_color

        self.border = is_border
        self.border_color = stdlib.BLACK
        self.border_size = border_size

        self.soiled = is_soiled
        self.condition = stdlib.NORMAL
        # setup label
        if is_label:
            self.label = label.Label(stdlib.Point(0, 0), text)
            self.label.parent = self
        else:
            self.label = None
        # setup event bahaivour function
        self.mouse_click = self.dump_function
        self.mouse_down = self.dump_function
        self.mouse_hover = self.dump_function
        self.no_focus = self.dump_function

    def _set_up_label(self):
        '''(Button) -> NoneType

        Setup the size and position of the label

        self : the button
        '''

        # setup font
        self.label.font = pygame.font.Font(None, 20)
        text_size = self.label.font.size(self.label.text)
        self.label.size = stdlib.Point(text_size[0], text_size[1])
        # calculate the position of the label
        # make the text be the center of the button
        x = (self.size.x - self.label.size.x) / 2
        y = (self.size.y - self.label.size.y) / 2
        self.label.position = stdlib.Point(x, y)

    def _draw(self):
        '''(Button) -> NoneType

        Draw the button

        self : the button
        '''

        control.Control.draw(self)
        # get full info to draw of the button
        button_pos = self.calculate_real_position()
        button_info = (button_pos.x, button_pos.y, self.size.x, self.size.y)
        # draw of the button
        if self.soiled:
            pygame.draw.rect(self.screen, self.current_color, button_info)
        # adjust the postion of the border of the best display
        button_info = (button_pos.x + 1, \
                       button_pos.y + 1, \
                       self.size.x - 2, \
                       self.size.y - 2)
        # draw of the outline of the button
        if self.border:
            pygame.draw.rect(self.screen, \
                             self.border_color, \
                             button_info, self.border_size)
        # draw the label if there is any
        if self.label:
            self._set_up_label()
            self.label.draw()

    def draw(self):
        '''(Button) -> NoneType

        Setup the color depend on the condition and Draw the button

        self : the button
        '''

        self.current_color = self.background_color
        # if mouse is hovering on it
        if self.condition == stdlib.HOVER:
            self.current_color = (self.background_color[0], \
                     self.background_color[1], \
                     min(self.background_color[2] + 40, 255))
        # if mouse is being clicked down on it
        elif self.condition == stdlib.CLICK:
            self.current_color = (self.background_color[0] / 2, \
                     self.background_color[1] / 2, \
                     self.background_color[2] / 2)
        self._draw()

    def local_act_mouse_hover(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process mouse hover event for internal repsond(only affect the button)
        Return the external respond(will be indicate later) and its arguments

        self : the button
        event : the event having information to handle
        '''

        self.condition = stdlib.HOVER
        self.draw()
        return [self.mouse_hover, []]

    def local_act_mouse_down(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process mouse down event for internal repsond(only affect the button)
        Return the external respond(will be indicate later) and its arguments

        self : the button
        event : the event having information to handle
        '''

        self.condition = stdlib.CLICK
        self.draw()
        return [self.mouse_down, []]

    def local_act_mouse_up(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process mouse up event for internal repsond(only affect the button)
        Return the external respond(will be indicate later) and its argument

        self : the button
        event : the event having information to handle
        '''

        # if the currently down
        if self.condition == stdlib.CLICK:
            # then set it back to normal
            self.condition = stdlib.NORMAL
            # redraw it
            self.draw()
            # and annouce click event
            return [self.mouse_click, []]
        # otherwise do nothing
        return [self.dump_function, []]

    def local_act_no_interaction(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process when there is no event on the button
        for internal repsond(only affect the button)
        Return the external respond(will be indicate later) and its arguments

        self : the button
        event : the event having information to handle
        '''

        # because there is no interaction
        if self.condition != stdlib.NORMAL:
            # then set it back to normal
            self.condition = stdlib.NORMAL
            # and redraw it
            self.draw()
        return [self.no_focus, []]

    def mouse_event(self, event):
        '''(Button, pygame.Event) -> list:[function, lst]

        Handle any mouse event on the control
        Return the external respond (will be indicate later) for an event with
        its agurments in another list

        self : the button
        event : the event having information to handle
        '''

        # get the mouse position
        mouse_pos = stdlib.Point(event.pos[0], event.pos[1])
        result = [self.dump_function, []]
        # check if the mouse is inside the button
        if mouse_pos.inside(self.abs_position, self.size):
            if event.type == pygame.MOUSEMOTION:
                # mouse hover event
                result = self.local_act_mouse_hover(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse down event
                result = self.local_act_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                # mouse up event
                result = self.local_act_mouse_up(event)
        else:
            # if there is no interation
            result = self.local_act_no_interaction(event)
        return result
