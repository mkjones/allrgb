import math
from color import Color
import random
from finder import Finder

# Represents the set of colors from which we can choose.
# Starts out with all colors of the given bit depth, and
# returns them either in random order (with iterate())
# or by finding the nearest one to a given color
class Colorset(object):

    def __init__(self, bits):
        self.bits = bits
        max_color = int(math.pow(2, bits))

        # list of Color objects in this set
        self.colors = []
        for r in range(0, max_color):
            for g in range(0, max_color):
                for b in range(0, max_color):
                    color = Color(r, g, b, bits)
                    self.colors.append(color)

        random.shuffle(self.colors)

        # mapping from the actual (r,g,b) tuple of a color to its object
        self.rgb2color = {x.rgb: x for x in self.colors}
        rgbs = [x.rgb for x in self.colors]

        # does the work of finding the nearest color for a query
        self.finder = Finder(rgbs)

    # find the color that is "closest" to the given Color object
    # in (naive) euclidean space.  Remove it from the colorset and
    # return it.
    def get_nearest(self, desired):
        if desired.bits != self.bits:
            raise Exception('wrong number of bits')
        res = self.finder.find_nearest(desired.rgb)

        return self.rgb2color[res]

    # Yields each color in the set.  Does not remove them.
    def iterate(self):
        for (r, g, b) in self.finder.iterate():
            yield Color(r, g, b, self.bits)

    def size(self):
        return self.finder.size()
