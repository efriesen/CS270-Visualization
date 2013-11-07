#Based on http://pythonvision.org/basic-tutorial

import numpy as np
import scipy
import pylab
import pymorph
import mahotas
from scipy import ndimage

chart = mahotas.imread('sample_chart.png');
dna = mahotas.imread('dna.jpeg');

print chart.shape
print chart.dtype
print chart.max()
print chart.min()

pylab.imshow(chart)
pylab.show()
