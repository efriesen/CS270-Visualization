import numpy as np
import pylab
import pymorph
from colour import Color
#imports look weird because my system is weird
from pytesser import pytesser
from PIL import Image
import mahotas

def imread(input_file_name):
    image = mahotas.imread(input_file_name)
    #Check if it is on a 0-255 scale
    if image[0][0][0]<1 and image[0][0][0]>0:
        image=image*255
        image = image.astype('uint8')
    return image

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

def find_all_centers(image, image_labels, feature_count):
    return ndimage.center_of_mass(image, image_labels, range(1,feature_count+1))

def display_graph(image):
    pylab.imshow(image)
    pylab.show()

def ocr(image):
    return pytesser.image_to_string(image)

#http://www.riisen.dk/dop/pil.html
def ocr_cropped(image, box):
    region = image.crop(box)
    return pytesser.image_to_string(region)

#conversion functions based on http://stackoverflow.com/questions/384759/pil-and-numpy
def numpy_to_pil(image):
    print image
    return Image.fromarray(image)

def pil_to_numpy(image):
    return numpy.array(image)

#There are only comments from here on
#The graveyard of previous code

#print nongrayscale_image
#print labeled
#print centers
#regmax = pymorph.regmax(labeled)
#print 'feature_count:', feature_count

#x = np.array(centers)[:,0]
#y = np.array(centers)[:,1]
#print x
#print y

#output_array(nongrayscale_image,'nongrayscale.txt')

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
rint color_scale(image[0][0])
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
