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
    #determine feature types of identified features
    feature_types = identify.identify_feature_types(image, image_labeled, feature_count)
    #object to perform analysis of features
    image_analyzer = interpret.analyzer(identify.nongrayscale_raw(image), image_labeled, feature_types)
    #a set of slices that comprise the objects in the image
    object_slices = image_analyzer.get_objects()
    #Convert the input image into a PIL-friendly format
    pil_image = util.numpy_to_pil(image)
    #Get a bounding box for the first slice
    box = interpret.slice_to_box(object_slices[0])

    #cropped_region = pil_image.crop(box)
    #cropped_region.save('temp.png')

    #print util.ocr_cropped(pil_image, box)
    print util.ocr(pil_image)

    #util.display_graph(image_analyzer.get_data_centers())
    #print image_analyzer.get_objects()
    #print image_analyzer.get_data_centers()
