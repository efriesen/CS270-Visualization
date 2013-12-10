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
    scaled_data=None

    x_domain = list()
    x_range = list()
    y_domain = list()
    y_range = list()

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
            elif feature_types[i]=='axis_line':
                axis_line_indexes.append(i)
            elif feature_types[i]=='axis_label':
                axis_label_indexes.append(i)

        self.data_centers = util.calculate_feature_centers(image, image_labeled, data_point_indexes)
        self.interpret_axis_lines(axis_line_indexes)
        self.interpret_axis_labels(axis_label_indexes)
        #We now have the domains and ranges, so x_scale and y_scale work 
        

    def interpret_axis_lines(self, axis_line_indexes):
        for i in axis_line_indexes:
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
                #note that top is 0 and the bottom is the max
                self.y_domain[0]=box[1]
                self.y_domain[0]=box[3]

    """
    Find two x labels and two y labels
    Determine their coordinates (ideally by tick marks; for now, by center)
    OCR them to get the values those coordinates represent
    Stretch the distance between the two labels found to match the axis length
    This will determine x_range and y_range
    """
    def interpret_axis_labels(self, axis_label_indexes):
        x_coords=list()
        x_label_ocr=list()
        y_coords=list()
        y_label_ocr=list()
        for i in axis_label_indexes:
            box = self.bounding_boxes[i]
            x_center = box[2]-box[0]
            y_center = box[3]-box[1]
            """
            If the label lies to the right of the y=x line that passes through
            the bottom left corner of the graph, it is for the x axis.
            Otherwise it is for the y axis.
            We calculate this by decreasing the x center for every y that it is
            below the bottom of the graph.
            """
            x_center_adjusted = x_center-(y_center-self.y_domain[1])
            x_len = len(x_label_ocr)
            y_len = len(y_label_ocr)
            #stop if we have found two labels for both axes
            if x_len>=2 and y_len>=2:
                break
            if x_center_adjusted>x_domain[0]:
                #potential problem: out of order coord_spread. is that dangerous?
                if x_len==0:
                    x_coords.append(x_center)
                    x_label_ocr.append(float(util.ocr_cropped(self.image, box)))
                elif x_len==1:
                    x_coords.append(x_center)
                    x_label_ocr.append(float(util.ocr_cropped(self.image, box)))
                else:
                    #the x labels have already been found
                    pass

            else:
                if y_len==0:
                    y_coords.append(y_center)
                    y_label_ocr.append(float(util.ocr_cropped(self.image, box)))
                elif y_len==1:
                    y_coords.append(y_center)
                    y_label_ocr.append(float(util.ocr_cropped(self.image, box)))
                else:
                    #the y labels have already been found
                    pass

        #Make sure we have the x and y labels and label spreads
        if len(x_coords)>=2 and len(y_coords>=2):
            self.x_range.append(util.scale(x_label_ocr[0], 
                x_coords, self.x_domain))
            self.x_range.append(util.scale(x_label_ocr[1], 
                x_coords, self.x_domain))
            self.y_range.append(util.scale(y_label_ocr[0], 
                y_coords, self.y_domain))
            self.y_range.append(util.scale(y_label_ocr[1], 
                y_coords, self.y_domain))

    #Assume x lies within the domain
    def x_scale(self, x):
        return util.scale(x, self.x_domain, self.x_range)

    #Assume y lies within the domain
    def y_scale(self, y):
        return util.scale(y, self.y_domain, self.y_range)

    #Save a cropped section of the bounding box associated with a given index to file
    def save_bbox_index(self, index, file_name='temp.png'):
        region = self.pil_image.crop(self.bounding_boxes[index])
        region.save(file_name)
