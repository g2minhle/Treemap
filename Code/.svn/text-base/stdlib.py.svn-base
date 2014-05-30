import pygame


class Point(object):
    def __init__(self, x, y):
        '''(Point, int, int) -> NoneType

        Construct Point with int i as the row co-ordinate and int j as
        the column co-ordinate.

        self : the point
        x : x
        y : y
        '''

        self.x = x
        self.y = y

    def inside(self, position, size):
        '''(Point, Point, Point) -> Boolean

        Return true in the point "self" inside the rectangle having "position"
        and "size"

        self : the point
        position : the position of the rectangle
        size : the position of the rectangle
        '''

        return (self.x <= position.x + size.x)\
               and (self.x >= position.x)\
               and (self.y >= position.y)\
               and (self.y <= position.y + size.y)


# all the constants

# button size
STANDARD_BUTTON_SIZE = Point(100, 32)
#color
STANDARD_GRAY = (212, 208, 200)
STANDARD_GRAY_BUTTON = (252, 248, 140)
BLACK = (0, 0, 0)
# button condition
NORMAL = 0
HOVER = 1
CLICK = 2
# mouse events
MOUSE_EVENT = [pygame.MOUSEBUTTONDOWN, \
               pygame.MOUSEBUTTONUP, \
               pygame.MOUSEMOTION]
# file type + load option
FILE = 3
DIRECTORY = 4
SECTION = 5
# key value
UP = [273, 8, 119]
DOWN = [274, 13, 115]
LEFT = [276, 97]
RIGHT = [275, 100]
