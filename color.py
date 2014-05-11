import math

class Color(object):

    def __init__(self, r, g, b, bits):
        self.rgb = (r, g, b)
        self.hash = r << 2 * bits | g << bits | b
        self.bits = bits

    def __eq__(self, other):
        return self.hash == other.hash and self.bits == other.bits

    def __hash__(self):
        return self.hash

    def brightness(self):
        return sum(self.rgb)

    def distance(self, other):
        if self.bits != other.bits:
            raise Exception('cannot get distance with different bit counts')
        diffs = map(lambda x: x[0] - x[1], zip(self.rgb, other.rgb))
        return sum(map(lambda x: int(math.pow(x, 2)), diffs))

    def get_24bit_tuple(self):
        scalar = int(math.pow(2, 8 - self.bits))
        return tuple(map(lambda x: x * scalar, self.rgb))


if __name__ == '__main__':
    c1 = Color(1, 2, 3, 4)
    c1_dupe = Color(1, 2, 3, 4)
    c2 = Color(3, 2, 3, 4)

    c3 = Color(2, 4, 8, 5)

    print c1 == c1_dupe
    print c1.__hash__() == c1_dupe.__hash__()
    print c1.__hash__() != c2.__hash__()
    print c3.get_24bit_tuple() == (16, 32, 64)
    print c1.distance(c1_dupe) == 0
    print c1.distance(c2) == 4

