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
        for x in xrange(0, width):
            for y in xrange(0, height):
                self.open_slots[(x, y)] = True

    def get(self, x, y):
        if (x, y) in self.open_slots:
            return None
        return self.colors[x][y]

    def set(self, x, y, color):
        adjacent = self.get_adjacent(x, y)
        for point in adjacent:
            if point in self.open_slots:
                self.adjacent_and_open.add(point)

        del self.open_slots[(x, y)]
        self.adjacent_and_open.remove((x, y))

        row = self.colors.get(x)
        if row is None:
            row = {}
            self.colors[x] = row
        row[y] = color

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

    def find_blank_nearby_opt(self, x, y):
        min_dist = 10000000000
        argmin = None
        for point in self.adjacent_and_open:
            dist = self.distance((x, y), point)
            if dist < min_dist:
                min_dist = dist
                argmin = point

        return argmin

        coords = (
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1))
        res = self._check_coords(coords)
        if res is not None:
            return res

        coords = (
            (x+1, y+1),
            (x+1, y-1),
            (x-1, y+1),
            (x+1, y-1))

        res = self._check_coords(coords)
        if res is not None:
            return res

        print 'falling back'
        return self._find_nearest(x, y)

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

    def save(self, filename):
        image = numpy.zeros((self.width, self.height, 3), 'uint8')
        for x, row in self.colors.iteritems():
            for y, color in row.iteritems():
                image[x, y, :] = color.get_24bit_tuple()

        Image.fromarray(image).save(filename)

diffs = (
    (-1, 0, 1),
    (-1, 1, 0),
    (0, -1, 1),
    (0, 1, -1),
    (1, 0, -1),
    (1, -1, 0))

if __name__ == '__main__':
    c = Canvas(4, 4)
    c.set(2, 1, (2, 40, 3))
    print c.get(2, 1)



