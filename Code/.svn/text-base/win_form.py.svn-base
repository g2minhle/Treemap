import stdlib
import label
import pygame


class WinForm:

    def __init__(self, size, background_color = stdlib.STANDARD_GRAY):
        '''(WinForm, stdlib.Point[, tuple]) -> NoneType

        Return a WinForm with size and background color

        self : the form
        size : the size of the form
        background_color : the background color of the form
        '''

        self.current_color = background_color
        self.controls = []
        self.position = stdlib.Point(0, 0)
        self.running = True
        self.screen = None
        self.size = stdlib.Point(size.x, size.y)

    def add_control(self, control):
        '''(WinForm, control.Control) -> NoneType

        Add "control" into list of control of the form and make the form
        become the parent of the control

        self : the form
        control : the new control
        '''

        control.parent = self
        self.controls.append(control)

    def _draw(self):
        '''(WinForm) -> NoneType

        Draw all the controls

        self : the form
        '''

        for i in range(0, len(self.controls)):
            self.controls[i].draw()

    def _handle_event(self):
        '''(WinForm) -> Boolean

        Handle all kind of event happened

        self : the form
        '''

        # get the event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
                self.running = False
                return
        # find the right control which the event apply to
        for i in range(0, len(self.controls)):
            # if a mouse event
            command = [self.controls[i].dump_function, []]
            if event.type in stdlib.MOUSE_EVENT:
                # get back the function and its argument in a list
                command = self.controls[i].mouse_event(event)
            # if a keyboard
            elif event.type == pygame.KEYUP:
                # get back the function and its argument in a list
                command = self.controls[i].key_event(event)
                print event.key
            # execute the function and its argument
            command[0](command[1])
        return

    def show_dialog(self):
        '''(WinForm) -> NoneType

        Show up the working form

        self : the form
        '''

        pygame.init()
        self.screen = pygame.display.set_mode((self.size.x, self.size.y))
        self.screen.fill(self.current_color)
        self._draw()
        while self.running:
            # get and handle event
            self._handle_event()
            # redraw if anything has changed
            pygame.display.flip()
        pygame.quit()

    def set_up_GUI(self):
        '''(WinForm) -> NoneType

        Set up all the controls of the form

        self : the form
        '''
        pass

    def close(self):
        '''(WinForm) -> NoneType

        Close the form

        self : the form
        '''

        self.running = False

    def calculate_real_position(self):
        '''(WinForm) -> stdlib.NoneType

        Return the absolute position of the form

        self : the form
        '''

        return stdlib.Point(0, 0)
