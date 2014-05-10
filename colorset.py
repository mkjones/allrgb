import math
from color import Color

class Colorset(object):

    def __init__(self, bits):
        self.bits = bits
        max_color = int(math.pow(2, bits))
        self.colorset = {}
        for r in xrange(0, max_color):
            for g in xrange(0, max_color):
                for b in xrange(0, max_color):
                    color = Color(r, g, b, bits)
                    self.colorset[color] = True

    def get_nearest(self, desired):
        thresh = 20
        nearest = [1000000000000, None]
        for color, _ in self.colorset.iteritems():
            distance = color.distance(desired)
            if distance <= thresh:
                del self.colorset[color]
                return color
            if distance < nearest[0]:
                nearest[0] = distance
                nearest[1] = color
        color = nearest[1]
        del self.colorset[color]
        return color

    def iterate(self):
        for color, _ in self.colorset.iteritems():
            yield color

    def size(self):
        return len(self.colorset)
