import numpy as np
import pylab
from scipy import ndimage
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

def find_all_centers(image, image_labeled, feature_count):
    return ndimage.center_of_mass(image, image_labeled, range(1,feature_count+1))

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
    #display_graph(image)
    image = np.uint8(image,mode='rgb')
    return Image.fromarray(image)

def pil_to_numpy(image):
    return numpy.array(image)

#Writes array to file as an integer. Useful for image_labeled
def write_array(file_name,numpy_array):
    np.savetxt(file_name,numpy_array, fmt='%i')

#return a series of slices corresponding to each separate object
# as defined by image_labeled
def generate_object_slices(image_labeled):
    return ndimage.find_objects(image_labeled)

#return the bounding boxes corresponding to each slice
def generate_bounding_boxes(object_slices):
    bounding_boxes = list()
    for i in xrange(len(object_slices)):
        bounding_boxes.append(slice_to_box(object_slices[i]))
    return bounding_boxes

def slice_to_box(input_slice):
    corners = get_corners(input_slice)
    top = int(corners[0][0])
    bottom = int(corners[0][1])
    left = int(corners[1][0])
    right = int(corners[1][1])
    box = (left, top, right, bottom)
    print input_slice, corners, box
    return box

#http://stackoverflow.com/questions/17750974/how-to-get-coordinates-from-a-numpy-slice-object
def get_corners(input_slice):
    return [(sl.start, sl.stop) for sl in input_slice]

#http://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
def scale(x, input_domain, input_range):
    domain_diff = input_domain[1]-input_domain[0]
    range_diff = input_domain[1]-input_domain[0]
    return (((x-input_domain[0]) *range_diff) / domain_diff) + input_range[0]
    
def calculate_feature_centers(image, image_labeled, data_point_indexes):
    return ndimage.center_of_mass(image, image_labeled, data_point_indexes)
