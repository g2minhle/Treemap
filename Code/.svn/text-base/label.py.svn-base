import control
import pygame
import stdlib


class Label(control.Control):

    def __init__(self, position, text):
        '''(Label, stdlib.Point, string) -> NoneType

        Construct the label

        self : the label
        position : the relative position of the label
        size : the size of the label
        '''

        control.Control.__init__(self, position, stdlib.Point(0, 0))
        self.text = text
        self.font = None

    def Text(self, text):
        '''(Label, string) -> NoneType

        Update the text display in for the label and redraw it

        self : the label
        text : the display text
        '''

        self.text = text
        self.draw()

    def _erase_content(self):
        '''(Control) -> NoneType

        Draw the control
        Erase the label by using parent current background color

        self : the label
        '''

        # get position of the label
        label_pos = self.calculate_real_position()
        # get full info to draw of the label
        label_info = (label_pos.x, label_pos.y, self.size.x, self.size.y)
        # erase of the background of the label using parent background color
        pygame.draw.rect(self.parent.screen,\
                        self.parent.current_color,\
                        label_info)

    def draw(self):
        '''(Label) -> NoneType

        Draw the label

        self : the label
        '''

        control.Control.draw(self)
        self._erase_content()
        # set font
        self.font = pygame.font.Font(None, 20)
        text_surface = self.font.render(self.text, 1, stdlib.BLACK)
        # get the size for future erase
        text_size = self.font.size(self.text)
        self.size = stdlib.Point(text_size[0], text_size[1])
        pos = self.calculate_real_position()
        # change into tuple
        pos = (pos.x, pos.y)
        self.screen.blit(text_surface, pos)
