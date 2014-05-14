import math
from color import Color
import random
from finder import Finder

class Colorset(object):

    def __init__(self, bits):
        self.bits = bits
        max_color = int(math.pow(2, bits))
        self.colors = []
        for r in xrange(0, max_color):
            for g in xrange(0, max_color):
                for b in xrange(0, max_color):
                    color = Color(r, g, b, bits)
                    self.colors.append(color)

        random.shuffle(self.colors)
        self.rgb2color = {x.rgb: x for x in self.colors}
        rgbs = map(lambda x: x.rgb, self.colors)

        self.finder = Finder(rgbs)

    def get_nearest(self, desired):
        if desired.bits != self.bits:
            raise Exception('wrong number of bits')
        res = self.finder.find_nearest(desired.rgb)

        return self.rgb2color[res]

    def iterate(self):
        for (r, g, b) in self.finder.iterate():
            yield Color(r, g, b, self.bits)

    def size(self):
        return self.finder.size()
