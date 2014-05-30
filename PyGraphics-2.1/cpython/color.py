import math


class Color(object):
    """An RGB color."""

    def __init__(self, r, g, b):
        """Create a Color object representing an RGB color
        with values (r, g, b)."""

        if 0 <= int(r) < 256 and 0 <= int(g) < 256 and 0 <= int(b) < 256:
            self.r = int(r)
            self.g = int(g)
            self.b = int(b)
        else:
            raise ValueError('Color values out of range (0, 255)')

    def __str__(self):
        """Return a str representation of this Color."""

        return "Color r=" + str(self.get_red()) + \
                    " g=" + str(self.get_green()) + \
                    " b=" + str(self.get_blue())

    def __repr__(self):
        """Return an executable str representation of this Color."""

        return "Color(" + str(self.get_red()) + ", " \
                        + str(self.get_green()) + ", "\
                        + str(self.get_blue()) + ")"

    def __sub__(self, color):
        """Return a Color object with RGB values equal to the difference
        between this Color and Color color."""

        values = [self.r - color.r, self.g - color.g, self.b - color.b]

        l = len(values)

        for idx in range(l):
            if values[idx] < 0:
                values[idx] = 0
        return Color(values[0], values[1], values[2])

    def __add__(self, color):
        """Return a Color object with RGB values equal to the sum of
        this Color and Color color."""

        values = [self.r + color.r, self.g + color.g, self.b + color.b]

        l = len(values)

        for idx in range(l):
            if values[idx] > 256:
                values[idx] = 255
        return Color(values[0], values[1], values[2])

    def __eq__(self, newcolor):
        """Return True if this Color has the same RGB values as Color
        newcolor."""

        return self.get_red() == newcolor.get_red() and self.get_green() == \
            newcolor.get_green() and self.get_blue() == newcolor.get_blue()

    def __ne__(self, newcolor):
        """Return True if this Color has different value from Color
        newcolor."""

        return not self.__eq__(newcolor)

    def copy(self):
        """Return a deep copy of this Color."""

        return Color(self.r, self.g, self.b)

    def distance(self, color):
        """Return the Euclidean distance between the RGB values of this Color
        and Color color."""

        r = pow(self.r - color.r, 2)
        g = pow(self.g - color.g, 2)
        b = pow(self.b - color.b, 2)
        return math.sqrt(r + g + b)

    def get_rgb(self):
        """Return a tuple of the RGB values of this Color."""

        return self.r, self.g, self.b

    def get_red(self):
        """Return the red value of this Color."""

        return self.r

    def get_green(self):
        """Return the green value of this Color."""

        return self.g

    def get_blue(self):
        """Return the blue value of this Color."""

        return self.b

    def set_red(self, value):
        """Set the red value of this Color to int value."""

        if 0 <= value < 256:
            self.r = int(value)
        else:
            raise ValueError('Color value %s out of range [0, 255]' % value)

    def set_green(self, value):
        """Set the green value of this Color to int value."""

        if 0 <= value < 256:
            self.g = int(value)
        else:
            raise ValueError('Color value %s out of range [0, 255]' % value)

    def set_blue(self, value):
        """Set the blue value of this Color to int value."""

        if 0 <= value < 256:
            self.b = int(value)
        else:
            raise ValueError('Color value %s out of range [0, 255]' % value)

    def make_lighter(self):
        """Increase the RGB values of this Color by about 40%.  This should
        be the inverse of make_darker, so the multiplier is (1 - .7) / .7."""

        factor = (1 - .7) / .7
        self.r = min(255, int(self.r + factor * self.r))
        self.g = min(255, int(self.g + factor * self.g))
        self.b = min(255, int(self.b + factor * self.b))

    def make_darker(self):
        """Decrease the RGB values of this Color by 30%."""

        self.r = int(self.r * .7)
        self.g = int(self.g * .7)
        self.b = int(self.b * .7)


###############################################################################
# Color Constants
##############################################################################

aliceblue = Color(240, 248, 255)
antiquewhite = Color(250, 235, 215)
aqua = Color(0, 255, 255)
aquamarine = Color(127, 255, 212)
azure = Color(240, 255, 255)
beige = Color(245, 245, 220)
bisque = Color(255, 228, 196)
black = Color(0, 0, 0)
blanchedalmond = Color(255, 235, 205)
blue = Color(0, 0, 255)
blueviolet = Color(138, 43, 226)
brown = Color(165, 42, 42)
burlywood = Color(222, 184, 135)
cadetblue = Color(95, 158, 160)
chartreuse = Color(127, 255, 0)
chocolate = Color(210, 105, 30)
coral = Color(255, 127, 80)
cornflowerblue = Color(100, 149, 237)
cornsilk = Color(255, 248, 220)
crimson = Color(220, 20, 60)
cyan = Color(0, 255, 255)
darkblue = Color(0, 0, 139)
darkcyan = Color(0, 139, 139)
darkgoldenrod = Color(184, 134, 11)
darkgray = Color(169, 169, 169)
darkgreen = Color(0, 100, 0)
darkkhaki = Color(189, 183, 107)
darkmagenta = Color(139, 0, 139)
darkolivegreen = Color(85, 107, 47)
darkorange = Color(255, 140, 0)
darkorchid = Color(153, 50, 204)
darkred = Color(139, 0, 0)
darksalmon = Color(233, 150, 122)
darkseagreen = Color(143, 188, 143)
darkslateblue = Color(72, 61, 139)
darkslategray = Color(47, 79, 79)
darkturquoise = Color(0, 206, 209)
darkviolet = Color(148, 0, 211)
deeppink = Color(255, 20, 147)
deepskyblue = Color(0, 191, 255)
dimgray = Color(105, 105, 105)
dodgerblue = Color(30, 144, 255)
firebrick = Color(178, 34, 34)
floralwhite = Color(255, 250, 240)
forestgreen = Color(34, 139, 34)
fuchsia = Color(255, 0, 255)
gainsboro = Color(220, 220, 220)
ghostwhite = Color(248, 248, 255)
gold = Color(255, 215, 0)
goldenrod = Color(218, 165, 32)
gray = Color(128, 128, 128)
green = Color(0, 255, 0)
greenyellow = Color(173, 255, 47)
honeydew = Color(240, 255, 240)
hotpink = Color(255, 105, 180)
indianred = Color(205, 92, 92)
indigo = Color(75, 0, 130)
ivory = Color(255, 255, 240)
khaki = Color(240, 230, 140)
lavender = Color(230, 230, 250)
lavenderblush = Color(255, 240, 245)
lawngreen = Color(124, 252, 0)
lemonchiffon = Color(255, 250, 205)
lightblue = Color(173, 216, 230)
lightcoral = Color(240, 128, 128)
lightcyan = Color(224, 255, 255)
lightgoldenrodyellow = Color(250, 250, 210)
lightgreen = Color(144, 238, 144)
lightgrey = Color(211, 211, 211)
lightpink = Color(255, 182, 193)
lightsalmon = Color(255, 160, 122)
lightseagreen = Color(32, 178, 170)
lightskyblue = Color(135, 206, 250)
lightslategray = Color(119, 136, 153)
lightsteelblue = Color(176, 196, 222)
lightyellow = Color(255, 255, 224)
lime = Color(0, 255, 0)
limegreen = Color(50, 205, 50)
linen = Color(250, 240, 230)
magenta = Color(255, 0, 255)
maroon = Color(128, 0, 0)
mediumaquamarine = Color(102, 205, 170)
mediumblue = Color(0, 0, 205)
mediumorchid = Color(186, 85, 211)
mediumpurple = Color(147, 112, 219)
mediumseagreen = Color(60, 179, 113)
mediumslateblue = Color(123, 104, 238)
mediumspringgreen = Color(0, 250, 154)
mediumturquoise = Color(72, 209, 204)
mediumvioletred = Color(199, 21, 133)
midnightblue = Color(25, 25, 112)
mintcream = Color(245, 255, 250)
mistyrose = Color(255, 228, 225)
moccasin = Color(255, 228, 181)
navajowhite = Color(255, 222, 173)
navy = Color(0, 0, 128)
oldlace = Color(253, 245, 230)
olive = Color(128, 128, 0)
olivedrab = Color(107, 142, 35)
orange = Color(255, 165, 0)
orangered = Color(255, 69, 0)
orchid = Color(218, 112, 214)
palegoldenrod = Color(238, 232, 170)
palegreen = Color(152, 251, 152)
paleturquoise = Color(175, 238, 238)
palevioletred = Color(219, 112, 147)
papayawhip = Color(255, 239, 213)
peachpuff = Color(255, 218, 185)
peru = Color(205, 133, 63)
pink = Color(255, 192, 203)
plum = Color(221, 160, 221)
powderblue = Color(176, 224, 230)
purple = Color(128, 0, 128)
red = Color(255, 0, 0)
rosybrown = Color(188, 143, 143)
royalblue = Color(65, 105, 225)
saddlebrown = Color(139, 69, 19)
salmon = Color(250, 128, 114)
sandybrown = Color(244, 164, 96)
seagreen = Color(46, 139, 87)
seashell = Color(255, 245, 238)
sienna = Color(160, 82, 45)
silver = Color(192, 192, 192)
skyblue = Color(135, 206, 235)
slateblue = Color(106, 90, 205)
slategray = Color(112, 128, 144)
snow = Color(255, 250, 250)
springgreen = Color(0, 255, 127)
steelblue = Color(70, 130, 180)
tan = Color(210, 180, 140)
teal = Color(0, 128, 128)
thistle = Color(216, 191, 216)
tomato = Color(255, 99, 71)
turquoise = Color(64, 224, 208)
violet = Color(238, 130, 238)
wheat = Color(245, 222, 179)
white = Color(255, 255, 255)
whitesmoke = Color(245, 245, 245)
yellow = Color(255, 255, 0)
yellowgreen = Color(154, 205, 50)
