import numpy as np
import scipy
from scipy import ndimage
import util

class analyzer:
    data_centers=list()
    image=None
    pil_image=None
    image_labeled=None
    object_slices=None
    bounding_boxes=None
    feature_types=None

    def __init__(self, image, image_labeled, feature_types):
        self.image=image
        self.pil_image = util.numpy_to_pil(image)
        self.image_labeled = image_labeled
        self.feature_types = feature_types
        data_point_indexes = list()
        axis_label_indexes = list()
        axis_line_indexes = list()
        self.object_slices = util.generate_object_slices(self.image_labeled)
        self.bounding_boxes = util.generate_bounding_boxes(self.object_slices)
        for i in xrange(0, len(feature_types)):
            if feature_types[i]=='data_point':
                data_point_indexes.append(i+1)
            elif feature_types[i]=='axis_label':
                axis_label_indexes.append(i)
            elif feature_types[i]=='axis_line':
                axis_line_indexes.append(i)
        self.data_centers = calculate_data_centers(image, image_labeled, data_point_indexes)


    #Save a cropped section of the bounding box associated with a given index to file
    def save_bbox_index(self, index, file_name='temp.png'):
        region = self.pil_image.crop(self.bounding_boxes[index])
        region.save(file_name)
        
def calculate_data_centers(image, image_labeled, data_point_indexes):
    return ndimage.center_of_mass(image, image_labeled, data_point_indexes)

def interpret_axis(image, image_labeled, feature_index):
    pass

def interpret_axis_label(image, image_labeled, feature_index):
    pass

def interpret_axis_line(image, image_labeled, feature_index):
    pass
