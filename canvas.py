import numpy
from PIL import Image
import collections
import random
import math

class Canvas(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = collections.defaultdict(collections.defaultdict)
        self.open_slots = {}
        for x in xrange(0, width):
            for y in xrange(0, height):
                self.open_slots[(x, y)] = True

    def get(self, x, y):
        try:
            return self.colors[x][y]
        except KeyError:
            return None

    def set(self, x, y, color):
        #print (x, y, color.rgb)
        del self.open_slots[(x, y)]
        self.colors[x][y] = color

    def find_blank_nearby(self, x, y):
        x_diffs = [1, -1, 2, -2]
        random.shuffle(x_diffs)
        y_diffs = [1, -1, 2, -2]
        random.shuffle(y_diffs)

        for i in x_diffs:
            newx = x+i
            if newx >= self.width or newx < 0:
                continue
            for j in y_diffs:
                newy = y+j
                if newy >= self.height or newy < 0:
                    continue
                if self.get(newx, newy) is None:
                    return (newx, newy)

        min_spot = (0, 0)
        min_distance = 1000000000
        for (i, j), _ in self.open_slots.iteritems():
            distance = int(math.pow((i-x), 2) + math.pow((j-y), 2))
            if distance < min_distance:
                min_distance = distance
                min_spot = (i, j)
        return min_spot


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



