import numpy as np
from scipy import ndimage
import util
import pylab

GRAYSCALE=3

def is_white(rgb):
    if rgb[0]<250:
        return False
    if rgb[1]<250:
        return False
    if rgb[2]<250:
        return False
    return True

def is_grayscale_raw(rgb, threshold):
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

def filter_image(image, filter_function):
    #Take a numpy array imported from an image and a filtering function
    #Return an array with 1 where the pixel matches the filtering function
    # and 0 where it does not
    col_count = len(image)
    row_count = len(image[0])
    filtered_image=np.zeros([col_count,row_count])
    for i in xrange(col_count):
        for j in xrange(row_count):
            if filter_function(image[i][j][:3]):
                filtered_image[i][j]=1
    return filtered_image

def nongrayscale_raw(image, threshold=GRAYSCALE):
    #1 if the pixel is not grayscale, 0 if it is grayscale
    filter_function = lambda x: not is_grayscale_raw(x,threshold)
    return filter_image(image, filter_function)

def non_white(image):
    filter_function = lambda x: not is_white(x)
    return filter_image(image, filter_function)

def identify_features(image):
    #Project part #1: identify features
    #"nongrayscale" is a placeholder with weaknesses we have identified
    #So a new algorithm goes here

    filtered_image=nongrayscale_raw(image)
    #filtered_image = non_white(image)
    #util.display_graph(filtered_image)
    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.measurements.label.html
    image_labeled, feature_count = ndimage.label(filtered_image)
    util.display_graph(image_labeled)
    return image_labeled, feature_count

def identify_feature_types(image, image_labeled, feature_count):
    #Project part #1: Identify feature types
    feature_types = []
    for i in xrange(feature_count):
        #do magic here
        feature_types.append('data_point')
    return feature_types
