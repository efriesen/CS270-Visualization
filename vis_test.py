#Based on http://pythonvision.org/basic-tutorial

import numpy as np
import scipy
import pylab
import pymorph
import mahotas
from scipy import ndimage
from colour import Color
import argparse
import math

parser = argparse.ArgumentParser(description='Import data from an image')
parser.add_argument('-i', dest = 'input_file', help='the image to import', default='data/sample_chart_small.png')
args = vars(parser.parse_args())
input_file = args["input_file"]

#Convert a 0-255 color list into a 0-1 color list
#Round to three decimal places to prevent strange color errors
def color_ratio(rgb_big):
    return [round(x*1000.0/255.0)/1000.0 for x in rgb_big]

def make_color_array(input_array):
    new_array=np.array(np.zeros([len(input_array),len(input_array[0])]),dtype=Color)
    for i in xrange(len(input_array)):
        for j in xrange(len(input_array[0])):
            #Take only the first 3 values; there can be more digits
            #to represent transparency with some formats
            color =Color(rgb=color_ratio(input_array[i][j][:3]))  
            new_array[i][j]=color
    return new_array

#Write the image array to file
def output_image(image, output_file_name):
    output_file=open(output_file_name,'w+')
    for col in image:
        for pixel in col:
            output_file.write('(')
            for val in pixel:
                output_file.write('{0},'.format(val))
            output_file.write(')')
        output_file.write('\n')

def output_array(color_image, output_file_name):
    output_file=open(output_file_name,'w+')
    for col in color_image:
        for pixel in col:
            output_file.write('{0}, '.format(pixel))
        output_file.write('\n')
    print 'array written to',output_file_name

def is_grayscale_color(color,threshold):
    return is_grayscale_raw(color.rgb, threshold)

def is_grayscale_raw(rgb,threshold):
    #By default, the rgb array can only hold values from 0-255.
    #That makes it difficult to compare values, so we convert it to int.
    rgb_int = np.int_(rgb)
    if abs(rgb_int[0]-rgb_int[1])>threshold:
        return False
    if abs(rgb_int[0]-rgb_int[2])>threshold:
        return False
    if abs(rgb_int[1]-rgb_int[2])>threshold:
        return False
    return True

#Take an array of Color objects corresponding to an image
#Return an array with a Color object where the color is not grayscale and 0 where the color is grayscale
#Where grayscale is defined as having all three rgb values within (threshold) of each other
def nongrayscale_color(color_image, threshold=0.01):
    col_count = len(color_image)
    row_count = len(color_image[0])
    nongrayscale_image = np.zeros([col_count,row_count], dtype=Color)
    for i in xrange(col_count):
        for j in xrange(row_count):
            if not is_grayscale_color(color_image[i][j], threshold):
                nongrayscale_image[i][j]=color_image[i][j]
    return nongrayscale_image

#Take a numpy array imported from an image
#Return an array with 1 where the color is not grayscale and 0 where the color is grayscale
def nongrayscale_raw(image, threshold=3):
    col_count = len(image)
    row_count = len(image[0])
    nongrayscale_array=np.zeros([col_count,row_count])
    for i in xrange(col_count):
        for j in xrange(row_count):
            if not is_grayscale_raw(image[i][j][:3], threshold):
                nongrayscale_array[i][j]=1
    return nongrayscale_array

image=mahotas.imread(input_file)
nongrayscale_array=nongrayscale_raw(image)


#output_array(nongrayscale_array,'nongrayscale.txt')

#output_image(image, 'temp.txt')
#color_image = make_color_array(image)

#print color_image[0][0]
#print is_grayscale_color(color_image[0][0], 0.01)

"""
temp = nongrayscale(color_image)
print color_image[0][0]
print 'temp', temp[0][0]
output_array(temp, 'nongrayscale.txt')
"""
#output_image(image, 'temp.txt')
#output_array(make_color_array(image),'temp_color.txt')
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
#explains label function: http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.measurements.label.html
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

