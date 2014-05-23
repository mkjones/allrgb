import numpy
from PIL import Image
import collections
import random
import math
from color import Color

class Canvas(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = {}
        self.open_slots = {}
        self.adjacent_and_open = set([])
        self.average_colors = {}
        for x in xrange(0, width):
            for y in xrange(0, height):
                self.open_slots[(x, y)] = True

    # Gets the current color at the position given.  Returns None if no
    # color is present.
    def get(self, x, y):
        if (x, y) in self.open_slots:
            return None
        return self.colors[x][y]

    # Sets the given color at the given position. Barfs if you try to set a color
    # at a position that already exists.
    # Does a bunch of bookkeeping around what pixels are open and eligible as well
    def set(self, x, y, color):

        # set the color!
        row = self.colors.get(x)
        if row is None:
            row = {}
            self.colors[x] = row
        row[y] = color

        # A color has been set! This pixel is no longer open.
        del self.open_slots[(x, y)]

        # If it's no longer open, it's also no longer adjacent-and-open.
        # Remove it if necessary.
        # (When we start out and set random pixels, they are not in this list,
        # so we must check for membership first)
        if (x, y) in self.adjacent_and_open:
            self.adjacent_and_open.remove((x, y))

        # Gotta do some bookkeeping about the adjacent spots
        adjacent = self.get_adjacent(x, y)
        for point in adjacent:
            if point == (x, y):
                continue
            if point in self.open_slots:
                self.adjacent_and_open.add(point)
                self.set_average(point)

    def set_average(self, point):
        (x, y) = point

        row = self.average_colors.get(x)
        if row is None:
            row = {}
            self.average_colors[x] = row
        row[y] = self.get_avg_color(x, y)

    def get_adjacent(self, x, y):
        ret = set([])
        for i in xrange(-1, 2):
            xnew = x + i
            if xnew < 0 or xnew >= self.width:
                continue
            for j in xrange(-1, 2):
                ynew = y + j
                if ynew < 0 or ynew >= self.height:
                    continue
                ret.add((xnew, ynew))
        return ret

    def get_avg_color(self, x, y):
        r = 0
        g = 0
        b = 0
        total = 0
        bits = None
        adjacent = self.get_adjacent(x, y)
        for (xnew, ynew) in adjacent:
            col = self.get(xnew, ynew)
            if col is None:
                continue
            if bits is None:
                bits = col.bits
            total += 1
            rgb = col.rgb
            r += rgb[0]
            g += rgb[1]
            b += rgb[2]
        return Color(int(r/total), int(g/total), int(b/total), bits)

    def distance(self, a, b):
        xd = a[0] - b[0]
        yd = a[1] - b[1]
        return (xd * xd) + (yd * yd)
        return sum(map(lambda x: x * x, (a[0]-b[0], a[1]-b[1])))

    # finds the open pixel with the average color closest to the target
    def find_pixel_with_average_near(self, target_color):
        min_distance = 1000000000
        pixel = None
        for (x, y) in self.adjacent_and_open:
            avg = self.average_colors[x][y]
            distance = avg.distance(target_color)
            if distance < min_distance:
                min_distance = distance
                pixel = (x, y)
        if pixel is None:
            print ('no adjacent and open?', self.adjacent_and_open, self.open_slots)

        return pixel

    def find_next_available(self):
        for x in self.adjacent_and_open:
            return x

    def find_blank_nearby_opt(self, x, y):
        coords = self.get_adjacent(x, y)

        res = self._check_coords(coords)
        if res is not None:
            return res

        closest_adjacent = self._find_closest((x, y), self.adjacent_and_open)
        if closest_adjacent is not None:
            return closest_adjacent

        print ('nothing left in adj and open?', self.adjacent_and_open)
        closest = self._find_closest((x, y), self.open_slots)
        if closest is not None:
            return closest

    def _find_closest(self, desired_point, list_of_points):
        min_dist = 100000000000000
        argmin = None
        for point in list_of_points:
            dist = self.distance(desired_point, point)
            if dist < min_dist:
                min_dist = dist
                argmin = point
        return argmin

    def _check_coords(self, coords):
        matches = []
        for check in coords:
            if check in self.open_slots:
                matches.append(check)
        if len(matches) > 0:
            return random.choice(matches)
        return None

    def _find_nearest(self, x, y):
        min_spot = (0, 0)
        min_distance = 1000000000
        for (i, j), _ in self.open_slots.iteritems():
            distance = int(math.pow((i-x), 2) + math.pow((j-y), 2))
            if distance < min_distance:
                min_distance = distance
                min_spot = (i, j)
        return min_spot

    def find_blank_nearby(self, x, y):
        x_diffs = random.choice(diffs)
        y_diffs = random.choice(diffs)

        for i in x_diffs:
            newx = x+i
            if newx >= self.width or newx < 0:
                continue
            for j in y_diffs:
                newy = y+j
                if newy >= self.height or newy < 0:
                    continue
                if newx == x and newy == y:
                    continue
                if self.get(newx, newy) is None:
                    return (newx, newy)

        return self._find_nearest(x, y)

    # Saves the current canvas to disk as a file with the given filename
    def save(self, filename):
        image = numpy.zeros((self.width, self.height, 3), 'uint8')
        for x, row in self.colors.iteritems():
            for y, color in row.iteritems():
                image[x, y, :] = color.get_24bit_tuple()

        Image.fromarray(image).save(filename)

if __name__ == '__main__':
    c = Canvas(4, 4)
    c.set(2, 1, (2, 40, 3))
    print c.get(2, 1)



