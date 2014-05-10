import numpy
from PIL import Image
import collections
import random

class Canvas(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = collections.defaultdict(collections.defaultdict)

    def get(self, x, y):
        try:
            return self.colors[x][y]
        except KeyError:
            return None

    def set(self, x, y, color):
        self.colors[x][y] = color

    def find_blank_nearby(self, x, y):
        for i in xrange(-1, 1):
            newx = x+i
            if newx >= self.width or newx < 0:
                continue
            for j in xrange(-1, 1):
                newy = y+j
                if newy >= self.height or newy < 0:
                    continue
                if self.get(newx, newy) is None:
                    return (newx, newy)

        newx = random.choice((x-1, x+1, x+2))
        newy = random.choice((y-1, y+1, y+2))
        if newx >= self.width or newx < 0:
            newx = x
        if newy > self.height or newy < 0:
            newy = y
        return self.find_blank_nearby(newx, newy)

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



