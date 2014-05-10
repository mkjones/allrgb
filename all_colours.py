import numpy
from PIL import Image
import math
import random
import time
from color import Color
from canvas import Canvas

all_colors = {}
bits = 6
print 'making colors'
max_color = int(math.pow(2, bits))
for r in xrange(0, max_color):
    for g in xrange(0, max_color):
        for b in xrange(0, max_color):
            all_colors[Color(r, g, b, bits)] = True

width = int(math.sqrt(len(all_colors)))
height = width + 1

i = 0
color_list = all_colors.keys()
random.shuffle(color_list)
canvas = Canvas(width, height)

print 'making image'
for col in color_list:
    x = i / height
    y = i % height
    canvas.set(x, y, col.get_24bit_tuple())
    i = i + 1

name = '/tmp/colors.%d.%d.png' % (bits, int(time.time()))
canvas.save(name)
print name

