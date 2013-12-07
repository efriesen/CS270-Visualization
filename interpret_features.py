import numpy as np
import scipy
from scipy import ndimage

class analyzer:
    data_centers=list()
    image=None
    image_labels=None
    feature_types=None

    def __init__(self, image, image_labels, feature_types):
        self.image=image
        self.image_labels = image_labels
        self.feature_types = feature_types
        data_point_indexes = list()
        axis_label_indexes = list()
        axis_line_indexes = list()
        for i in xrange(0, len(feature_types)):
            if feature_types[i]=='data_point':
                data_point_indexes.append(i+1)
            elif feature_types[i]=='axis_label':
                axis_label_indexes.append(i)
            elif feature_types[i]=='axis_line':
                axis_line_indexes.append(i)
        self.data_centers = calculate_data_centers(image, image_labels, data_point_indexes)

    def get_data_centers(self):
        return self.data_centers

    def get_objects(self):
        return ndimage.find_objects(self.image_labels)

def calculate_data_centers(image, image_labels, data_point_indexes):
    return ndimage.center_of_mass(image, image_labels, data_point_indexes)

def interpret_axis(image, image_labels, feature_index):
    pass

def interpret_axis_label(image, image_labels, feature_index):
    pass

def interpret_axis_line(image, image_labels, feature_index):
    pass
