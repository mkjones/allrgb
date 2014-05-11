import numpy
from PIL import Image
import math
import random
import time
from color import Color
from canvas import Canvas
from colorset import Colorset

bits = 7
seed = 42
random.seed(seed)
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
start_time = last_save_time = time.time()
time_color = 0.0
time_point = 0.0
while colorset.size() > 0:
    last_col = canvas.get_avg_color(last_x, last_y)

    get_nearest_start = time.time()
    new_col = colorset.get_nearest(last_col)
    diff = time.time() - get_nearest_start
    time_color += diff

    get_nearby_start = time.time()
    (x, y) = canvas.find_blank_nearby(last_x, last_y)
    diff = time.time() - get_nearby_start
    time_point += diff

    canvas.set(x, y, new_col)
    last_x = x
    last_y = y
    i = i + 1

    if i % 1000 == 0:
        name = '/tmp/colors.%d.%d.png' % (bits, i)
        avg_rate = i / (time.time() - start_time)
        print (name, time.time() - last_save_time, int(avg_rate), int(time_color), int(time_point))
        last_save_time = time.time()
        canvas.save(name)

