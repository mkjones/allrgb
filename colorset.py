
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
        for color, _ in self.colorset.iteritems():
            if color.distance(desired) <= thresh:
                del self.colorset[color]
                return color
    def iterate(self):
        for color, _ in self.colorset.iteritems():
            yield color

    def size(self):
        return len(self.colorset)
