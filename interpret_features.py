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
    """
    the scales will be defined as functions during the program
    they take a given coordinate and return the coordinate's relative value
    according to the axis on the graph
    For example, if the axis on the graph ranges from 0 to 100
    """
    x_domain = None
    x_range = None
    y_domain = None
    y_range = None

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
        for i in axis_line_indexes:
            interpret_axis_line(self.image, self.image_labeled, i)
        for i in axis_label_indexes:
            interpret_axis_label(self.image, self.image_labeled, i)

    def interpret_axis_label(self, index):
        pass

    def interpret_axis_line(self, index):
        #First, determine whether the axis is horizontal or vertical
        box = self.bounding_boxes[index]
        width = box[2]-box[0]
        height = box[3]-box[1]
        if width>height:
            #the axis is horizontal
            self.x_domain[0]=box[0]
            self.x_domain[1]=box[2]
        else:
            #the axis is vertical
            #invert the order because the top is 0 and the bottom is the max
            self.y_domain[0]=box[3]
            self.y_domain[0]=box[1]

    #Assume x lies within the domain
    #http://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
    def x_scale(self, x):
        x_domain_diff = self.x_domain[1]-self.x_domain[0]
        x_range_diff = self.x_range[1]-self.x_range[0]
        x = (((x-self.x_domain[0]) *x_range_diff) /x_domain_diff) + self.x_range[0]
        return x

    #Assume y lies within the domain
    def y_scale(self, y):
        y_domain_diff = self.y_domain[1]-self.y_domain[0]
        y_range_diff = self.y_range[1]-self.y_range[0]
        y = (((y-self.y_domain[0]) *y_range_diff) /y_domain_diff) + self.y_range[0]
        return y

    #Save a cropped section of the bounding box associated with a given index to file
    def save_bbox_index(self, index, file_name='temp.png'):
        region = self.pil_image.crop(self.bounding_boxes[index])
        region.save(file_name)
        
def calculate_data_centers(image, image_labeled, data_point_indexes):
    return ndimage.center_of_mass(image, image_labeled, data_point_indexes)
