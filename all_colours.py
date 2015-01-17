import numpy
from PIL import Image
import math
import random
import time
from color import Color
from canvas import Canvas
from colorset import Colorset
import sys
import filler

# constants to configure how we're making things!

# how many bits should we use per channel?  "normal" 24-bit color
# uses 8 bits per channel, but will take a very long time to generate
# a full image.  Image size = # colors = 2^(3 * bits)
bits = 4

# How many pixels do we start by randomly filling in?  This is only
# relevant for the "find the best place for a color" approach, rather
# than the "find the best color for a place" approach.
starting_pixels = 3

# This is just a seed for the random number generator so we can do
# things like performance testing deterministically
seed = 27

print 'initializing'

random.seed(seed)
colorset = Colorset(bits)
# This is technically only correct for an even number of bits, but
# it rounds down for an odd number of bits, and there are simply some colors
# that we never use.  Shrug.
height = width = int(math.sqrt(colorset.size()))
canvas = Canvas(width, height)

# Grab some random starting colors just by making a randomly-sorted
# list of all the colors and taking the first few.
# Not the most efficient, but doesn't really matter.
colors = [x for x in colorset.iterate()]
random.shuffle(colors)

# Choose random starting colors and place them randomly on the canvas
last_y = 0
last_x = 0
for i in xrange(width/10):
    starting_color = colorset.get_nearest(colors[i])
    last_x = i * 10 # TODO why not randomize this?
    canvas.set(last_x, last_y, starting_color)

start_time = time.time()
last_save_time = time.time()
time_color = 0.0
time_point = 0.0


print ('last_x before', last_x)
filler = filler.ByColorFiller(canvas, colorset, starting_pixels)
#filler = filler.ByWalkFiller(canvas, colorset, starting_pixels)
filler.go()

