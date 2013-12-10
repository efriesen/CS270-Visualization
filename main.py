#Based on http://pythonvision.org/basic-tutorial

import argparse
import interpret_features as interpret
import identify_features as identify
import util
from PIL import Image

#Return the arguments
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Import data from an image')
    parser.add_argument('-i', dest = 'input_file', 
            help='the image to import', default='data/sample_chart_easy.png')
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = initialize_argument_parser()
    input_file = args["input_file"]
    image=util.imread(input_file)
    #util.display_graph(image)
    #print image
    image_labeled, feature_count = identify.identify_features(image)
    print 'feature_count:', feature_count
    feature_types = identify.identify_feature_types(image, image_labeled, feature_count)
    axes_box = identify.identify_axes_box(image)
    filtered_image = identify.nongrayscale_raw(image)
    image_analyzer = interpret.analyzer(image, filtered_image, image_labeled, feature_types, axes_box)
    #determine feature types of identified features
    #object to perform analysis of features
    #util.write_array('image_labeled.txt',image_labeled)
    #a set of slices that comprise the objects in the image
    object_slices = image_analyzer.object_slices
    #Convert the input image into a PIL-friendly format


    #image_analyzer.save_bbox_index(20)
    #image_analyzer.pil_image.save('temp.png')

    #cropped_region = pil_image.crop(box)
    #cropped_region.save('temp.png')

    #print util.ocr_cropped(pil_image, box)
    #print util.ocr(pil_image)

    #print image_analyzer.get_objects()
    #print image_analyzer.get_data_centers()
