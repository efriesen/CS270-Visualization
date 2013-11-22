import numpy as np
import scipy
from scipy import ndimage

debug=False

def interpret_feature(image, image_labels, feature_index, feature_type):
    if feature_type=='data_point':
        return interpret_data_point(image, image_labels, feature_index)
    elif feature_type == 'axis':
        return interpret_axis(feature, feature_index)

def interpret_data_point(image, image_labels, feature_index):
    if debug: print 'interpret_data_point'
    center = ndimage.center_of_mass(image, image_labels, feature_index)
    return center

def interpret_axis(feature):
    pass
