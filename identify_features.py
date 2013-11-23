import numpy as np
from scipy import ndimage

def identify_features(image):
    #Project part #1: identify features
    #"nongrayscale" is a placeholder with weaknesses we have identified
    #So a new algorithm goes here
    nongrayscale_image=nongrayscale_raw(image)
    image_labels, feature_count = ndimage.label(nongrayscale_image)
    return image_labels, feature_count

#Take a numpy array imported from an image
#Return an array with 1 where the color is not grayscale and 0 where the color is grayscale
def nongrayscale_raw(image, threshold=3):
    col_count = len(image)
    row_count = len(image[0])
    nongrayscale_image=np.zeros([col_count,row_count])
    for i in xrange(col_count):
        for j in xrange(row_count):
            if not is_grayscale_raw(image[i][j][:3], threshold):
                nongrayscale_image[i][j]=1
    return nongrayscale_image

def is_grayscale_raw(rgb,threshold):
    #By default, the rgb array can only hold values from 0-255.
    #That makes it difficult to compare values, so we convert it to int.
    rgb_int = np.int_(rgb)
    if abs(rgb_int[0]-rgb_int[1])>threshold:
        #print rgb,
        return False
    if abs(rgb_int[0]-rgb_int[2])>threshold:
        #print rgb,
        return False
    if abs(rgb_int[1]-rgb_int[2])>threshold:
        #print rgb,
        return False
    return True

def identify_feature_types(image, image_labels, feature_count):
    #Project part #1: Identify feature types
    feature_types = []
    for i in xrange(feature_count):
        #do magic here
        feature_types.append('todo')
    return feature_types