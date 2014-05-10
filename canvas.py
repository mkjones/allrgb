import numpy
from PIL import Image

class Canvas(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = numpy.zeros((width, height, 3), 'uint8')

    def save(self, filename):
        Image.fromarray(self.buffer).save(filename)

    def get(self, x, y):
        return self.buffer[x, y]

    def set(self, x, y, value):
        self.buffer[x, y, :] = value


if __name__ == '__main__':
    c = Canvas(4, 4)
    c.set(2, 1, (2, 40, 3))
    print c.get(2, 1)



