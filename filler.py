import time
import math
import random

from canvas import Canvas
from colorset import Colorset

class Filler(object):
    def __init__(self, bits, starting_pixel_count):
        self.colorset = Colorset(bits)

        # This is technically only correct for an even number of bits, but
        # it rounds down for an odd number of bits, and there are simply some colors
        # that we never use.  Shrug.

        height = width = int(math.sqrt(self.colorset.size()))
        self.canvas = Canvas(width, height)

        self.starting_pixel_count = starting_pixel_count
        self.add_starting_pixels()
        self.start_time = time.time()
        self.last_save_time = time.time()

        self.time_color = 0.0
        self.time_point = 0.0

    def add_starting_pixels(self):
        # Grab some random starting colors just by making a randomly-sorted
        # list of all the colors and taking the first few.
        # Not the most efficient, but doesn't really matter.
        colors = [x for x in self.colorset.iterate()]
        random.shuffle(colors)
        height = width = self.canvas.height
        self.starting_pixel_list = []
        for i in range(self.starting_pixel_count):
            starting_color = self.colorset.get_nearest(colors[i])
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            self.starting_pixel_list.append((x, y))
            self.canvas.set(x, y, starting_color)

    def write_image(self, i):
        bits = self.colorset.bits
        name = '/tmp/colors-%s.%d.%d.%d.png' % (self.__class__.__name__,
                                                bits,
                                                self.starting_pixel_count,
                                                i)
        avg_rate = i / (time.time() - self.start_time)
        print((name,
               time.time() - self.last_save_time,
               int(avg_rate),
               int(self.time_color),
               int(self.time_point)))
        self.canvas.save(name)
        self.last_save_time = time.time()

class ByColorFiller(Filler):
    def go(self):
        i = 0
        # For each color generated, find the pixel where it fits "best"
        # (i.e. the pixel where the average of the filled-in pixels surrounding it
        # is closest to this color)
        for color in self.colorset.iterate():
            # TODO: just check if canvas is full first?
            point = self.canvas.find_pixel_with_average_near(color)
            if point is None:
                # it is possible we have more colors than pixels (since the canvas
                # is a square, but the number of colors is not a perfect square if
                # bits is odd)
                break
            (x, y) = point
            self.canvas.set(x, y, color)
            if i % 1000 == 0:
                self.write_image(i)

            i += 1

        self.write_image(i)

class ByWalkFiller(Filler):

    def go(self):
        (last_x, last_y) = self.starting_pixel_list[-1]
        i = 0
        while self.colorset.size() > 0:
            get_nearby_start = time.time()

            # find the open pixel nearest the last one we filled in
            nearby = self.canvas.find_blank_nearby_opt(last_x, last_y)
            if nearby is None:
                break
            (x, y) = nearby
            diff = time.time() - get_nearby_start
            self.time_point += diff

            # figure out what the "average" color is of all the pixels
            # around the open pixel we found
            avg_col = self.canvas.get_avg_color(x, y)

            # now find the color closest to that average
            get_nearest_start = time.time()
            new_col = self.colorset.get_nearest(avg_col)
            diff = time.time() - get_nearest_start
            self.time_color += diff

            self.canvas.set(x, y, new_col)
            last_x = x
            last_y = y

            i += 1

            if i % 1000 == 0:
                self.write_image(i)

        self.write_image(i)
