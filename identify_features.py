import numpy as np
from scipy import ndimage
import util
import pylab

GRAYSCALE=3
HORIZONTAL_REACH=4
VERTICAL_REACH=1

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

def non_white(image):
    filter_function = lambda x: not is_white(x)
    return filter_image(image, filter_function)

def nongrayscale_raw(image, threshold=GRAYSCALE):
    #1 if the pixel is not grayscale, 0 if it is grayscale
    filter_function = lambda x: not is_grayscale_raw(x,threshold)
    return filter_image(image, filter_function)

def identify_features(image):
    #Project part #1: identify features
    #"nongrayscale" is a placeholder with weaknesses we have identified
    #So a new algorithm goes here

    filtered_image=nongrayscale_raw(image)
    #filtered_image = non_white(image)
    #util.display_graph(filtered_image)
    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.measurements.label.html
    #structure=[[1,1,1],[1,1,1],[1,1,1]]
    image_labeled, feature_count = ndimage.label(filtered_image)
    #util.display_graph(image_labeled)
    return image_labeled, feature_count

def boxes_overlap(box1, box2):
    if box2[0]<box1[0] and box1[0]<box2[2]+HORIZONTAL_REACH and box2[1]<box1[1] and box1[1]<box2[3]+VERTICAL_REACH:
        return True
    elif box1[0]<box2[0] and box2[0]<box1[2]+HORIZONTAL_REACH and box2[0]<box1[0] and box1[1]<box2[3]+VERTICAL_REACH:
        return True
    elif box1[0]<box2[0] and box2[0]<box1[2]+HORIZONTAL_REACH and box1[1]<box2[1] and box2[1]<box1[3]+VERTICAL_REACH:
        return True
    elif box2[0]<box1[0] and box1[0]<box2[2]+HORIZONTAL_REACH and box1[1]<box2[1] and box2[1]<box1[3]+VERTICAL_REACH:
        return True
    return False

def relabel_feature(image_labeled, meta_box, new_label):
    box = meta_box[0]
    for row in xrange(box[1], box[3]):
        for col in xrange(box[0], box[2]):
            if image_labeled[row][col] != 0:
                image_labeled[row][col] = new_label
    #meta_box[2] = 'axis_label'

def merge_boxes(image_labeled, meta_box1, meta_box2, meta_boxes):
    true_id1, true_id2 = min([meta_boxes[index-1][3] for index in list(meta_box1[4])]), min([meta_boxes[index-1][3] for index in list(meta_box2[4])])
    unified_id = min(true_id1, true_id2)
    meta_box1[3]=unified_id
    meta_box2[3]=unified_id
    if unified_id == true_id1:
        #update meta_box2's pixels' labels
        for meta_box in [meta_boxes[index-1] for index in list(meta_box2[4])]:
            relabel_feature(image_labeled, meta_box, unified_id)
    else:
        #update meta_box1's pixels' labels
        for meta_box in [meta_boxes[index-1] for index in list(meta_box1[4])]:
            relabel_feature(image_labeled, meta_box, unified_id)
    meta_box1[2] = 'axis_label'
    meta_box2[2] = 'axis_label'
    merged_set=meta_box1[4]|meta_box2[4]
    meta_box1[4]=merged_set
    meta_box2[4]=merged_set

def identify_feature_types(image, image_labeled, feature_count):
    #Project part #1: Identify feature types
    #do magic here
    util.write_array('image_labeled_premerge.txt',image_labeled)
    object_slices=util.generate_object_slices(image_labeled)
    #print object_slices
    bounding_boxes=util.generate_bounding_boxes(object_slices)
    #meta_box:=(box_boundaries, cluster_id, cluster_type, true_id, family_member)
    #e.g. ((0,0,3,3), 2, 'data_point', 1, {1,2,5,7}
    #note that cluster_id's start at 1, not 0
    meta_boxes=[[box,id+1,'data_point',id+1,set([id+1])] for id,box in enumerate(bounding_boxes)]
    #print meta_boxes
    for i in xrange(len(meta_boxes)-1):
        meta_box1=meta_boxes[i]
        for j in xrange(i+1,len(meta_boxes)):
            meta_box2=meta_boxes[j]
            if boxes_overlap(meta_box1[0], meta_box2[0]):
                print 'Boxes {0} and {1} overlap!'.format(meta_box1[1], meta_box2[1])
                merge_boxes(image_labeled, meta_box1, meta_box2, meta_boxes)
    feature_types = [meta_box[2] for meta_box in meta_boxes]
    #There should be 40 data_point's and 
    print "{0} axis_labels; {1} data_points".format(feature_types.count('axis_label'),feature_types.count('data_point'))
    print meta_boxes
    util.write_array('image_labeled_merged.txt',image_labeled)
    #magic done

    return feature_types

def identify_axes_box(image):
    filtered_image = non_white(image)
    image_labeled, feature_count = ndimage.label(filtered_image)
    util.write_array('temp.txt',image_labeled)
    object_slices=util.generate_object_slices(image_labeled)
    bounding_boxes=util.generate_bounding_boxes(object_slices)
    graph_bounds = identify_largest_bounding_box(bounding_boxes)
    return graph_bounds

def identify_largest_bounding_box(bounding_boxes):
    max_area= 0
    max_box= None
    for box in bounding_boxes:
        area = (box[2]-box[0])*(box[3]-box[1])
        if area>max_area:
            max_box=box
            max_area=area
    return max_box

