import color


class Pixel(object):
    """A pixel in an image with a color and an x and y location."""

    def __init__(self, pixels, x, y):
        """Create a Pixel object representing the pixel
         at coordinates (x, y) in the PixelAccess object pixels."""

        self.x = x
        self.y = y

        # This is intended for a PixelAccess object implemented in C
        # It is a two-dimensional array (e.g. self.pixels[x, y])
        # used to access color tuples.
        self.pixels = pixels

        # This is a trick to raise an IndexError if out of bounds.
        self.pixels[x, y]

    def __str__(self):
        """Return a str with location and color information
         for this Pixel."""

        return "Pixel (%d, %d): color=%s" % (self.x, self.y,
                                            repr(self.get_color()))

    def set_red(self, r):
        """Set the red value of this Pixel to int r."""

        if 0 <= r <= 255:
            self.pixels[self.x, self.y] = \
                (r,
                 self.pixels[self.x, self.y][1],
                 self.pixels[self.x, self.y][2])
        else:
            raise ValueError('Invalid red value specified.')

    def set_green(self, g):
        """Set the green value of this Pixel to int g."""

        if 0 <= g <= 255:
            self.pixels[self.x, self.y] = \
                (self.pixels[self.x, self.y][0],
                 g,
                 self.pixels[self.x, self.y][2])
        else:
            raise ValueError('Invalid green value specified.')

    def set_blue(self, b):
        """Set the blue value of this Pixel to int b."""

        if 0 <= b <= 255:
            self.pixels[self.x, self.y] = \
                (self.pixels[self.x, self.y][0],
                 self.pixels[self.x, self.y][1],
                 b)
        else:
            raise ValueError('Invalid blue value specified.')

    def get_red(self):
        """Return the red value of this Pixel."""

        return self.pixels[self.x, self.y][0]

    def get_green(self):
        """Return the green value of this Pixel."""

        return self.pixels[self.x, self.y][1]

    def get_blue(self):
        """Return the blue value of this Pixel."""

        return self.pixels[self.x, self.y][2]

    def get_color(self):
        """Return a Color object representing the color of this Pixel."""

        return color.Color(self.get_red(), self.get_green(), self.get_blue())

    def set_color(self, color):
        """Set the color values of this Pixel to those of Color object
        color."""

        self.set_red(color.get_red())
        self.set_green(color.get_green())
        self.set_blue(color.get_blue())

    def get_x(self):
        """Return the x value of this Pixel."""

        return self.x

    def get_y(self):
        """Return the y value of this Pixel."""

        return self.y
