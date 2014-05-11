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

print 'initializing'
width = int(math.sqrt(colorset.size()))
height = width + 1

i = 0
canvas = Canvas(width, height)

colors = [x for x in colorset.iterate()]
random.shuffle(colors)

print 'making image'
starting_color = colors[0]

last_x = random.randrange(width)
last_y = random.randrange(height)

canvas.set(last_x, last_y, starting_color)

i = 0
last_save_time = time.time()
while colorset.size() > 0:
    last_col = canvas.get(last_x, last_y)
    new_col = colorset.get_nearest(last_col)
    (x, y) = canvas.find_blank_nearby(last_x, last_y)
    canvas.set(x, y, new_col)
    last_x = x
    last_y = y
    i = i + 1

    if i % 1000 == 0:
        name = '/tmp/colors.%d.%d.png' % (bits, i)
        print (name, time.time() - last_save_time)
        last_save_time = time.time()
        canvas.save(name)


for col in colorset.iterate():

    x = i / height
    y = i % height
    canvas.set(x, y, col.get_24bit_tuple())
    i = i + 1

print name

