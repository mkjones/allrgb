import numpy
from PIL import Image
import math
import random
import time
from color import Color
from canvas import Canvas
from colorset import Colorset

bits = 6
print 'making colors'
colorset = Colorset(bits)
size = colorset.size()

width = int(math.sqrt(colorset))
height = width + 1

i = 0
canvas = Canvas(width, height)

print 'making image'
for col in colorset.iterate():
    x = i / height
    y = i % height
    canvas.set(x, y, col.get_24bit_tuple())
    i = i + 1

name = '/tmp/colors.%d.%d.png' % (bits, int(time.time()))
canvas.save(name)
print name

