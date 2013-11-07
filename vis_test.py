#Based on http://pythonvision.org/basic-tutorial

import numpy as np
import scipy
import pylab
import pymorph
import mahotas
from scipy import ndimage
import argparse

parser = argparse.ArgumentParser(description='Import data from an image')
parser.add_argument('-i', dest = 'input_file', help='the image to import', default='data/sample_chart.png')
args = vars(parser.parse_args())
input_file = args["input_file"]

image=mahotas.imread(input_file)

print 'shape:', image.shape
print 'data type:', image.dtype
print 'max:', image.max()
print 'min:', image.min()

pylab.imshow(image)
pylab.show()
