import button
import stdlib
import random


class DisplayUnit(button.Button):

    def __init__(self, position, size, parent, file_list):
        '''(DisplayUnit, stdlib.Point, stdlib.Point, Object, list)
                                                                  ->NoneType
        Construct a display unit

        self : the display unit
        size : the size of the unit
        parent : the parant of the unit
        file_list : list of all file of the unit
        '''
        button.Button.__init__(self, position, "", size, \
                               self._get_random_color(), \
                               False, False, False)
        self.parent = parent
        self.file_list = file_list
        self.left = None
        self.right = None
        self.typ = stdlib.SECTION
        self.file_system_info = None
        # if there is only 1 file or directory
        if len(file_list) == 1:
            # get the file or directory
            self.file_system_info = file_list[0]
            file_list[0].display_unit = self
            if self.file_system_info.typ == stdlib.FILE:
                self.typ = stdlib.FILE
                self.list_info = None
                self.soiled = True
            else:
                # if it is a directory, start to look at children
                self.typ = stdlib.DIRECTORY
                self.file_list = self.file_system_info.children
                self.list_info = stdlib.Point(0, len(self.file_list) - 1)
        # start to construct  children
        self._divide()

    def _divide(self):
        '''(DisplayUnit) -> NoneType

        Construct the children (left and right)

        self : the display unit
        '''

        # only do this if we have a section or a directory
        if self.typ != stdlib.FILE:
            index, percent, total = self._partition()
            # if the size is 0 then we do nothing
            if total == 0:
                return
            # determine children should be draw from left to right or top down
            drawing_direction = self.size.x > self.size.y
            first_half = self.file_list[:index]
            second_half = self.file_list[index:]
            # if fisrt halft is empty then there will be only second half
            if not first_half:
                first_half = second_half
                second_half = None
                percent = 1
            # draw 2 half
            self.left = self._create_child(percent, drawing_direction, \
                      first_half, \
                      self._first_children_pos, self._first_children_size)
            self.right = self._create_child(percent, drawing_direction, \
                      second_half, \
                      self._second_children_pos, self._second_children_size)

    def _create_child(self, percent, drawing_direction, \
                      file_list, pos_function, size_function):
        '''(DisplayUnit, float, boolean, list, stdlib.Point, stdlib.Point)
                                                              -> DisplayUnit
        Return display unit construted from the percent, drawing_direction,
        file list and 2 function
        Two function will compute the possition and size of the unit

        self : the display unit
        percent : the percentage of the children
        drawing_direction : indicating how to draw the unit
        file_list : the list of file of children
        pos_function : function to calculate the child position
        size_function : function to calculate the child size
        '''

        if file_list:
            pos = pos_function(percent, drawing_direction)
            size = size_function(percent, drawing_direction)
            return DisplayUnit(pos, size, self, file_list)

    def _first_children_pos(self, percent, drawing_direction):
        '''(DisplayUnit, float, boolean) -> stdlib.Point

        Return the position of first children base on the percentage,
        drawing direction

        self : the display unit
        percent : the percentage of the children
        drawing_direction : indicating how to draw the unit
        '''

        return stdlib.Point(0, 0)

    def _first_children_size(self, percent, drawing_direction):
        '''(DisplayUnit, float, boolean) -> stdlib.Point

        Return the size of first children base on the percentage,
        drawing direction

        self : the display unit
        percent : the percentage of the children
        drawing_direction : indicating how to draw the unit
        '''

        percent = stdlib.Point(percent, 1)
        if not drawing_direction:
            percent = stdlib.Point(1, percent.x)
        x = int(float(self.size.x) * percent.x)
        y = int(float(self.size.y) * percent.y)
        return stdlib.Point(x, y)

    def _second_children_pos(self, percent, drawing_direction):
        '''(DisplayUnit, float, boolean) -> stdlib.Point

        Return the position of second children base on the percentage,
        drawing direction

        self : the display unit
        percent : the percentage of the children
        drawing_direction : indicating how to draw the unit
        '''

        x = self.left.size.x * drawing_direction
        y = self.left.size.y * (not drawing_direction)
        return stdlib.Point(x, y)

    def _second_children_size(self, percent, drawing_direction):
        '''(DisplayUnit, float, boolean) -> stdlib.Point

        Return the size of second children base on the percentage,
        drawing direction

        self : the display unit
        percent : the percentage of the children
        drawing_direction : indicating how to draw the unit
        '''

        x = self.size.x \
          - self.left.size.x * drawing_direction
        y = self.size.y \
          - self.left.size.y * (not drawing_direction)
        return stdlib.Point(x, y)

    def _partition(self):
        '''DisplayUnit -> int, float, int

        Return the pivot index, the percentage of the first partition and
        the total size of data
        Precondition : self.file_list is sorted

        self : the display unit
        '''

        lst = self.file_list
        total = 0
        # get the total
        for i in range(0, len(lst)):
            total += lst[i].size
        if total == 0:
            return 0, 0, 0
        else:
            s = 0
            # go add in
            for i in range(0, len(lst)):
                s += lst[i].size
                # find the pivot
                if s * 2 > total:
                    break
            s -= lst[i].size
            return i, float(s) / float(total), total

    def draw(self):
        '''(DisplayUnit) -> NoneType

        Draw everything - including children

        self : the display unit
        '''

        button.Button.draw(self)
        if self.left:
            self.left.draw()
        if self.right:
            self.right.draw()
        button.Button._draw(self)

    def _get_random_color(self):
        '''(DisplayUnit) -> tuple

        Return the tuple containing red, green, blue value of a random color

        self : the display unit
        '''

        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)
        return (r, g, b)

    def _return_right_event(self, event, return_function):
        '''(DisplayUnit, pygame.Event, function) -> [function, list]

        Process any mouse event for internal repsond(only affect the children
        of the unit)
        Return the external respond(will be indicate later) and its arguments

        self : the display unit
        event : the event having information to handle
        return_function : a function to be called
        '''

        result_right = [[], []]
        result_left = [[], []]
        if self.left:
            result_left = self.left.mouse_event(event)
        if self.right:
            result_right = self.right.mouse_event(event)
        # if have data back from left child
        if result_right[1]:
            return [return_function, result_right[1]]
        # if have data back from right child
        elif result_left[1]:
            # if have no data back from any child
            return [return_function, result_left[1]]
        else:
            return [self.dump_function, []]

    def _draw_refresh(self):
        '''(DisplayUnit) -> NoneType

        Set the condtion back to nomarl condtion and redraw everything,
        including children

        self : the display unit
        '''

        # set back to normal stage
        self.condition = stdlib.NORMAL
        # if it is a file
        if self.typ == stdlib.FILE:
            # just draw it out
            self.draw()
        else:
            # draw non empty children
            if self.left:
                self.left._draw_refresh()
            if self.right:
                self.right._draw_refresh()
            # if it is a directory
            if self.typ == stdlib.DIRECTORY:
                # just draw it self
                button.Button.draw(self)

    def local_act_mouse_hover(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process mouse hover event for internal repsond(only affect the unit)
        Return the external respond(will be indicate later) and its arguments

        self : the display unit
        event : the event having information to handle
        '''

        self.condition = stdlib.HOVER
        if self.typ == stdlib.FILE:
            self.draw()
            return [self.mouse_hover, [self.file_system_info]]
        else:
            result = self._return_right_event(event, self.mouse_hover)
            button.Button._draw(self)
            return result

    def local_act_mouse_down(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process mouse down event for internal repsond(only affect the unit)
        Return the external respond(will be indicate later) and its arguments

        self : the display unit
        event : the event having information to handle
        '''

        self.condition = stdlib.CLICK
        if self.typ == stdlib.FILE:
            self.draw()
            return [self.mouse_down, [self.file_system_info]]
        else:
            result = self._return_right_event(event, self.mouse_down)
            button.Button._draw(self)
            return result

    def local_act_mouse_up(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process mouse up event for internal repsond(only affect the unit)
        Return the external respond(will be indicate later) and its argument

        self : the display unit
        event : the event having information to handle
        '''

        if self.typ == stdlib.FILE:
            if self.condition == stdlib.CLICK:
                self.condition = stdlib.NORMAL
                self.draw()
                return [self.mouse_click, [self.file_system_info]]
            return [[], []]
        else:
            result = self._return_right_event(event, self.mouse_click)
            button.Button._draw(self)
            return result

    def local_act_no_interaction(self, event):
        '''(Button, pygame.Event) -> [function, lst]

        Process when there is no event on the unit
        for internal repsond(only affect the unit)
        Return the external respond(will be indicate later) and its arguments

        self : the display unit
        event : the event having information to handle
        '''

        # because there is no interaction
        if self.condition != stdlib.NORMAL:
            # then set it back to normal
            self.condition = stdlib.NORMAL
            # and redraw it and its children
            if self.typ == stdlib.FILE:
                self.draw()
            else:
                self._draw_refresh()
        return [self.no_focus, []]
