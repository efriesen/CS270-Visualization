#Based on http://pythonvision.org/basic-tutorial

import numpy as np
import scipy
import pylab
import pymorph
import mahotas
from scipy import ndimage
from colour import Color
import argparse

#Convert a 0-255 color list into a 0-1 color list
def color_ratio(rgb_big):
    return rgb_big/255.0

def make_color_array(input_array):
    new_array=np.array(np.zeros([len(input_array),len(input_array[0])]),dtype=Color)
    for i in xrange(len(input_array)):
        for j in xrange(len(input_array[0])):
            color =Color(rgb=color_ratio(input_array[i][j])) 
            new_array[i][j]=color
    return new_array

#Write the image array to file
def output_image(image, output_file_name):
    output_file=open(output_file_name,'w+')
    for col in image:
        for pixel in col:
            output_file.write('({0},{1},{2}), '.format(pixel[0], pixel[1], pixel[2]))
        output_file.write('\n')

def output_color_image(color_image, output_file_name):
    output_file=open(output_file_name,'w+')
    for col in color_image:
        for pixel in col:
            output_file.write('{0}, '.format(pixel.hex))
        output_file.write('\n')

parser = argparse.ArgumentParser(description='Import data from an image')
parser.add_argument('-i', dest = 'input_file', help='the image to import', default='data/sample_chart_easy.png')
args = vars(parser.parse_args())
input_file = args["input_file"]

image=mahotas.imread(input_file)
output_image(image, 'temp.txt')
output_color_image(make_color_array(image),'temp_color.txt')
"""
print image[0]
print image[0][0]
print color_scale(image[0][0])
print Color(rgb=color_ratio(image[0][0]))
"""
"""
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


#print len(image[0])
"""
print 'shape:', image.shape
print 'data type:', image.dtype
print 'max:', image.max()
print 'min:', image.min()


pylab.imshow(image)
pylab.show()"""

