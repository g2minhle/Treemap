import control


class KeyHandler(control.Control):

    def __init__(self):
        '''(KeyHandler) -> NoneType

        Construct the key handler

        self : the key handler
        '''

        self.key_handle = self.dump_function

    def key_event(self, event):
        '''(Control, pygame.Event) -> list:[function, lst]

        Return the right function(will be indicate later) for an event with its
        agurments in another list

        self : the key handler
        event : the event having information to handle
        '''

        return [self.key_handle, [event.key]]
