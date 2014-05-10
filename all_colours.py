import numpy
from PIL import Image
import math
import random
import time

def int2col(integer):
    mask = int(math.pow(2, bits)) - 1
    b = integer & mask
    g = (integer >> bits) & mask
    r = (integer >> 2 * bits) & mask
    return (r, g, b)

def col2int(r, g, b):
    return r << 2 * bits | g << bits | b


all_colors = {}
bits = 6
max_color = int(math.pow(2, bits))
for r in xrange(0, max_color):
    for g in xrange(0, max_color):
        for b in xrange(0, max_color):
            all_colors[col2int(r, g, b)] = True

width = int(math.sqrt(len(all_colors)))
height = width + 1

final_image = numpy.zeros((width, height, 3), 'uint8')

i = 0
color_list = all_colors.keys()
random.shuffle(color_list)
color_list = sorted(color_list, key=lambda x: int2col(x)[0])
for col in color_list:
    rgb = int2col(col)
    scalar = int(math.pow(2, 8 - bits))
    scaled = map(lambda x: x * scalar, rgb)
    x = i / height
    y = i % height
    final_image[x, y, :] = scaled
    i = i + 1

Image.fromarray(final_image).save('/tmp/colors.%d.%d.png' % (bits, int(time.time())))

