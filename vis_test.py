#Based on http://pythonvision.org/basic-tutorial

import numpy as np
import scipy
import pylab
import pymorph
import mahotas
from scipy import ndimage
import argparse

parser = argparse.ArgumentParser(description='Import data from an image')
parser.add_argument('-i', dest = 'input_file', help='the image to import', default='data/sample_chart_easy.png')
args = vars(parser.parse_args())
input_file = args["input_file"]

image=mahotas.imread(input_file)

#http://ms.physics.ucdavis.edu/~bradshaw/Python%20Image%20Reduction.pdf
threshold = image.mean()
#print threshold
labels, num = ndimage.label(image > threshold)
#print labels
centers = ndimage.center_of_mass(image, labels, range(1,num+1))
pylab.imshow(centers)
pylab.show()
#print centers
x = np.array(centers)[:,0]
y = np.array(centers)[:,1]

print x
print y

"""
Print the array to file
outputfile=open('temp.txt','w+')
for col in image:
    for pixel in col:
        outputfile.write('({0},{1},{2}), '.format(pixel[0], pixel[1], pixel[2]))
    outputfile.write('\n')
"""

#print len(image[0])
"""
print 'shape:', image.shape
print 'data type:', image.dtype
print 'max:', image.max()
print 'min:', image.min()


pylab.imshow(image)
pylab.show()"""

