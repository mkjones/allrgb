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
bits = 3

# How many pixels do we start by randomly filling in?  This is only
# relevant for the "find the best place for a color" approach, rather
# than the "find the best color for a place" approach.
starting_pixels = 3

# This is just a seed for the random number generator so we can do
# things like performance testing deterministically
seed = 29

print('initializing')

random.seed(seed)

filler = filler.ByColorFiller(bits, starting_pixels)
#filler = filler.ByWalkFiller(bits, starting_pixels)
filler.go()

